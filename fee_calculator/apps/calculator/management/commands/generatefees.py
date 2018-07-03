# -*- coding: utf-8 -*-
import csv
from collections import defaultdict
from decimal import Decimal

from django.core.management import BaseCommand, CommandError
from django.db.transaction import atomic

from calculator.models import (
    Price, Scheme, Scenario, FeeType, OffenceClass, Unit, Modifier, AdvocateType
)
from calculator.tests.lib.utils import scenario_clf_to_id, scenario_ccr_to_id


def listdict():
    from collections import defaultdict
    return defaultdict(list)


class Command(BaseCommand):
    help = 'Generate fees from data exported from CCR/CCLF'

    def add_arguments(self, parser):
        parser.add_argument(
            'scheme', type=str, choices=['AGFS10', 'LGFS8', 'LGFS9'],
            help='Type of scheme fees being generated for'
        )
        parser.add_argument(
            '--lgfs_ppe_fees', type=str,
            help=('''
                Path of CSV file containing LGFS PPE fees.
                Run the following query on CCLF DB to generate:

                select bs.scenario, bs.trbc_trial_basis, bs.percent, bs.formula,
                    bs.min_trial_length, bs.min_evidence_pages,
                    ep.ofty_offence_type, ep.evidence_pages, ep.trial_fee, ep.fee_per_page
                    from bill_scenarios bs join
                        evidence_pages_uplifts ep on bs.trbc_trial_basis=ep.trbc_trial_basis
                        where bs.fsth_fee_structure_id=X and ep.fsth_fee_structure_id=X;
            ''')
        )
        parser.add_argument(
            '--lgfs_daily_fees', type=str,
            help=('''
                Path of CSV file containing LGFS daily fees.
                Run the following query on CCLF DB to generate:

                select bs.scenario, bs.trbc_trial_basis, bs.percent, bs.formula,
                    bs.min_trial_length, bs.min_evidence_pages, bf.ofty_offence_type,
                    bf.basic_fee_value, bf.basic_evidence_pages_value,
                    tup.trial_length, tup. trial_uplift_value, tup.ppe_cutoff_value
                    from bill_scenarios bs join
                        basic_fees bf on bs.trbc_trial_basis=bf.trbc_trial_basis join
                        trial_uplifts_ppe_cut_offs tup on bf.ofty_offence_type=tup.ofty_offence_type
                        where bs.fsth_fee_structure_id=X and
                        bf.fsth_fee_structure_id=X and tup.fsth_fee_structure_id=X;
            ''')
        )
        parser.add_argument(
            '--agfs_10_basic_fees', type=str,
            help=('''
                Path of CSV file containing AGFS 10 basic fees.
                Run the following query on CCR DB to generate:

                select bs.id as scenario_id, bs.trbc_trial_basis, bf.basic_fee_value,
                    bf.psty_person_type, bf.trial_day_from, bf.trial_day_to, bf.unit,
                    bf.offence_band, bf.third
                    from bill_scenarios bs
                        join basic_fees bf on bs.trbc_trial_basis=bf.trbc_trial_basis
                        where bs.fsth_fee_structure_id=X and bf.fsth_fee_structure_id=X;
            ''')
        )
        parser.add_argument(
            '--agfs_10_misc_fees', type=str,
            help=('''
                Path of CSV file containing AGFS 10 misc fees.
                Run the following query on CCR DB to generate:

                select mf.psty_person_type, mf.limit_from, mf.limit_to, mf.fee_per_unit,
                mf.unit, mf.bist_bill_sub_type, mf.bisc_bill_scenario_id,
                bst.defendant_uplift_allowed, bst.case_uplift_allowed
                    from misc_fees mf
                        join bill_scenarios bs on bs.id=mf.bisc_bill_scenario_id
                        join bill_sub_types bst on mf.bist_bill_sub_type=bst.bill_sub_type
                        where bs.fsth_fee_structure_id=X;
            ''')
        )

    def handle(self, *args, **options):
        scheme_name = options['scheme']

        if scheme_name in ['LGFS8', 'LGFS9']:
            if not options['lgfs_ppe_fees']:
                raise CommandError(
                    "'lgfs_ppe_fees' is required for scheme {}".format(scheme_name)
                )
            if not options['lgfs_daily_fees']:
                raise CommandError(
                    "'lgfs_daily_fees' is required for scheme {}".format(scheme_name)
                )
            scheme_id = {'LGFS8': 2, 'LGFS9': 4}[scheme_name]
            generate_lgfs_fees(
                Scheme.objects.get(pk=scheme_id),
                options['lgfs_ppe_fees'],
                options['lgfs_daily_fees']
            )
        elif scheme_name == 'AGFS10':
            if not options['agfs_10_basic_fees']:
                raise CommandError(
                    "'agfs_10_basic_fees' is required for scheme {}".format(scheme_name)
                )
            if not options['agfs_10_misc_fees']:
                raise CommandError(
                    "'agfs_10_misc_fees' is required for scheme {}".format(scheme_name)
                )
            generate_agfs10_fees(
                Scheme.objects.get(pk=1),
                options['agfs_10_basic_fees'],
                options['agfs_10_misc_fees']
            )


@atomic
def generate_lgfs_fees(lgfs_scheme, ppe_fees_path, daily_fees_path):
    lit_fee_type = FeeType.objects.get(pk=54)
    day_unit = Unit.objects.get(pk='DAY')
    ppe_unit = Unit.objects.get(pk='PPE')
    lgfs_modifier_1 = Modifier.objects.get(pk=12)
    lgfs_modifier_2 = Modifier.objects.get(pk=13)

    with open(ppe_fees_path) as data_export:
        reader = csv.DictReader(data_export)
        ppe_data = defaultdict(listdict)
        for line in reader:
            ppe_data[line['SCENARIO']][line['OFTY_OFFENCE_TYPE']].append(line)

    with open(daily_fees_path) as data_export:
        reader = csv.DictReader(data_export)
        daily_data = defaultdict(listdict)
        for line in reader:
            daily_data[line['SCENARIO']][line['OFTY_OFFENCE_TYPE']].append(line)

    for scenario in ppe_data:
        for offence_type in ppe_data[scenario]:
            fees = sorted(ppe_data[scenario][offence_type], key=lambda f: int(f['EVIDENCE_PAGES']))
            previous_pages = 0
            fixed_fee = Decimal(0)
            for fee in fees:
                if fee['FORMULA'] == 'FIXED':
                    continue

                discount = Decimal(fee['PERCENT'])/Decimal('100')

                limit_from = previous_pages
                limit_to = int(fee['EVIDENCE_PAGES']) - 1

                if limit_from == 0:
                    fee_per_page = Decimal(0)
                else:
                    fee_per_page = Decimal(fee['FEE_PER_PAGE'])

                price = Price.objects.create(
                    scheme=lgfs_scheme,
                    scenario=Scenario.objects.get(pk=scenario_clf_to_id(fee['SCENARIO'])),
                    fee_type=lit_fee_type,
                    advocate_type=None,
                    offence_class=OffenceClass.objects.get(pk=fee['OFTY_OFFENCE_TYPE']),
                    unit=ppe_unit,
                    fee_per_unit=fee_per_page*discount,
                    fixed_fee=(fixed_fee or Decimal(fee['TRIAL_FEE']))*discount,
                    limit_from=limit_from,
                    limit_to=limit_to,
                    strict_range=True
                )
                price.modifiers.add(lgfs_modifier_1)
                price.modifiers.add(lgfs_modifier_2)
                price.save()

                previous_pages = int(fee['EVIDENCE_PAGES'])
                fixed_fee = Decimal(fee['TRIAL_FEE'])

            discount = Decimal(fee['PERCENT'])/Decimal('100')

            limit_from = previous_pages
            limit_to = None

            price = Price.objects.create(
                scheme=lgfs_scheme,
                scenario=Scenario.objects.get(pk=scenario_clf_to_id(fee['SCENARIO'])),
                fee_type=lit_fee_type,
                advocate_type=None,
                offence_class=OffenceClass.objects.get(pk=fee['OFTY_OFFENCE_TYPE']),
                unit=ppe_unit,
                fee_per_unit=Decimal(0),
                fixed_fee=Decimal(fee['TRIAL_FEE'])*discount,
                limit_from=limit_from,
                limit_to=limit_to,
                strict_range=True
            )
            price.modifiers.add(lgfs_modifier_1)
            price.modifiers.add(lgfs_modifier_2)
            price.save()

    for scenario in daily_data:
        for offence_type in daily_data[scenario]:
            fees = sorted(daily_data[scenario][offence_type], key=lambda f: int(f['TRIAL_LENGTH']))
            previous_total = Decimal('0')
            last_created_price = None
            for fee in fees:
                trial_length = int(fee['TRIAL_LENGTH'])
                # basic fee applies for length 1-2
                if trial_length > 1 and (
                        trial_length == 2 or
                        fee['FORMULA'] == 'FIXED' or
                        fee['TRBC_TRIAL_BASIS'] in ('GUILTY PLEA', 'CRACKED TRIAL')
                ):
                    continue

                discount = Decimal(fee['PERCENT'])/Decimal('100')
                total_fee = Decimal(fee['BASIC_FEE_VALUE']) + Decimal(fee['TRIAL_UPLIFT_VALUE'])
                step_fee = (total_fee - previous_total)*discount
                previous_total = total_fee

                if fee['FORMULA'] == 'FIXED':
                    limit_from = int(fee['MIN_TRIAL_LENGTH'])
                    limit_to = None
                    fixed_fee = step_fee
                    fee_per_unit = Decimal(0)
                elif trial_length == 1:
                    limit_from = int(fee['MIN_TRIAL_LENGTH'])
                    limit_to = 2
                    fixed_fee = step_fee
                    fee_per_unit = Decimal(0)
                else:
                    limit_from = trial_length
                    limit_to = trial_length
                    fixed_fee = Decimal(0)
                    fee_per_unit = step_fee

                if last_created_price and last_created_price.fee_per_unit == fee_per_unit:
                    last_created_price.limit_to = limit_to
                    last_created_price.save()
                else:
                    price = Price.objects.create(
                        scheme=lgfs_scheme,
                        scenario=Scenario.objects.get(pk=scenario_clf_to_id(fee['SCENARIO'])),
                        fee_type=lit_fee_type,
                        advocate_type=None,
                        offence_class=OffenceClass.objects.get(pk=fee['OFTY_OFFENCE_TYPE']),
                        unit=day_unit,
                        fee_per_unit=fee_per_unit,
                        fixed_fee=fixed_fee,
                        limit_from=limit_from,
                        limit_to=limit_to,
                    )

                    if (fee['FORMULA'] in ['DAYS', 'PPE'] or
                            fee['TRBC_TRIAL_BASIS'] == 'ELECTED CASE NOT PROCEEDED'):
                        price.modifiers.add(lgfs_modifier_1)
                        price.modifiers.add(lgfs_modifier_2)

                    price.save()
                    last_created_price = price


@atomic
def generate_agfs10_fees(agfs_scheme, basic_fees_path, misc_fees_path):
    basic_agfs_fee = FeeType.objects.get(pk=34)

    day_unit = Unit.objects.get(pk='DAY')

    case_modifier = Modifier.objects.get(pk=1)
    defendant_modifier = Modifier.objects.get(pk=2)
    discontinuance_discount_modifier = Modifier.objects.get(pk=7)
    retrial_0_month_modifier = Modifier.objects.get(pk=8)
    retrial_1_month_modifier = Modifier.objects.get(pk=9)
    retrial_cracked_0_month_modifier = Modifier.objects.get(pk=10)
    retrial_cracked_1_month_modifier = Modifier.objects.get(pk=11)

    before_final_third = Modifier.objects.get(pk=16)
    final_third = Modifier.objects.get(pk=17)

    with open('agfs_10_basic_fees.csv') as data_export:
        reader = csv.DictReader(data_export)
        for fee in reader:
            try:
                limit_from = int(fee['TRIAL_DAY_FROM'])
            except ValueError:
                limit_from = 1

            try:
                limit_to = int(fee['TRIAL_DAY_TO'])
            except ValueError:
                limit_to = None

            if fee['UNIT'] == 'FIXED':
                fee_per_unit = Decimal(0)
                fixed_fee = Decimal(fee['BASIC_FEE_VALUE'])
            else:
                fee_per_unit = Decimal(fee['BASIC_FEE_VALUE'])
                fixed_fee = Decimal(0)

            scenario_id = scenario_ccr_to_id(fee['SCENARIO_ID'], scheme=10)
            price = Price.objects.create(
                scheme=agfs_scheme,
                scenario=Scenario.objects.get(pk=scenario_id),
                fee_type=basic_agfs_fee,
                advocate_type=AdvocateType.objects.get(pk=fee['PSTY_PERSON_TYPE']),
                offence_class=OffenceClass.objects.get(pk=fee['OFFENCE_BAND']),
                unit=day_unit,
                fee_per_unit=fee_per_unit,
                fixed_fee=fixed_fee,
                limit_from=limit_from,
                limit_to=limit_to,
            )
            price.modifiers.add(defendant_modifier)
            price.modifiers.add(case_modifier)

            if scenario_id == 11:
                price.modifiers.add(retrial_0_month_modifier)
                price.modifiers.add(retrial_1_month_modifier)
            if scenario_id == 16:
                price.modifiers.add(retrial_cracked_0_month_modifier)
                price.modifiers.add(retrial_cracked_1_month_modifier)
            if scenario_id == 1:
                price.modifiers.add(discontinuance_discount_modifier)

            if fee['THIRD'] and int(fee['THIRD']) == 3:
                price.modifiers.add(final_third)
            elif fee['THIRD'] and int(fee['THIRD']) in [1, 2]:
                price.modifiers.add(before_final_third)

            price.save()

    with open('agfs_10_misc_fees.csv') as data_export:
        reader = csv.DictReader(data_export)
        for fee in reader:
            try:
                limit_from = int(fee['LIMIT_FROM'])
            except ValueError:
                limit_from = 1

            try:
                limit_to = int(fee['LIMIT_TO'])
            except ValueError:
                limit_to = None

            if fee['UNIT'] == 'FIXED':
                fee_per_unit = Decimal(0)
                fixed_fee = Decimal(fee['FEE_PER_UNIT'])
            else:
                fee_per_unit = Decimal(fee['FEE_PER_UNIT'])
                fixed_fee = Decimal(0)

            scenario_ids = [scenario_ccr_to_id(fee['BISC_BILL_SCENARIO_ID'], scheme=10)]

            if fee['BIST_BILL_SUB_TYPE'] == 'AGFS_PLEA':
                # non-unique code, different name for different schemes
                fee_type = FeeType.objects.get(id=103)
            else:
                fee_type = FeeType.objects.get(code=fee['BIST_BILL_SUB_TYPE'])

            for scenario_id in scenario_ids:
                price = Price.objects.create(
                    scheme=agfs_scheme,
                    scenario=Scenario.objects.get(pk=scenario_id),
                    fee_type=fee_type,
                    advocate_type=AdvocateType.objects.get(pk=fee['PSTY_PERSON_TYPE']),
                    offence_class=None,
                    unit=Unit.objects.get(pk=fee['UNIT']),
                    fee_per_unit=fee_per_unit,
                    fixed_fee=fixed_fee,
                    limit_from=limit_from,
                    limit_to=limit_to,
                )
                if fee['DEFENDANT_UPLIFT_ALLOWED'] == 'Y':
                    price.modifiers.add(defendant_modifier)
                if fee['CASE_UPLIFT_ALLOWED'] == 'Y':
                    price.modifiers.add(case_modifier)

                price.save()
