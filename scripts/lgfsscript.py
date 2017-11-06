'''
This script, using data exported using the commented SQL statements, will create
the required prices for the litigator fee scheme.
'''

from collections import defaultdict
import csv
from decimal import Decimal

from calculator.models import (
    Price, Scheme, Scenario, FeeType, OffenceClass, Unit, Modifier
)
from calculator.tests.lib.utils import scenario_clf_to_id


def listdict():
    from collections import defaultdict
    return defaultdict(list)


lgfs_scheme = Scheme.objects.get(pk=2)
lit_fee_type = FeeType.objects.get(pk=54)
day_unit = Unit.objects.get(pk='DAY')
ppe_unit = Unit.objects.get(pk='PPE')
lgfs_modifier_1 = Modifier.objects.get(pk=12)
lgfs_modifier_2 = Modifier.objects.get(pk=13)


'''
select bs.scenario, bs.trbc_trial_basis, bs.percent, bs.formula,
    bs.min_trial_length, bs.min_evidence_pages,
    ep.ofty_offence_type, ep.evidence_pages, ep.trial_fee, ep.fee_per_page
    from bill_scenarios bs join
      evidence_pages_uplifts ep on bs.trbc_trial_basis=ep.trbc_trial_basis
      where bs.fsth_fee_structure_id=7 and ep.fsth_fee_structure_id=7;
'''
with open('lgfs_joined_ppe_data.csv') as data_export:
    reader = csv.DictReader(data_export)
    data = defaultdict(listdict)
    for line in reader:
        data[line['SCENARIO']][line['OFTY_OFFENCE_TYPE']].append(line)

for scenario in data:
    for offence_type in data[scenario]:
        fees = sorted(data[scenario][offence_type], key=lambda f: int(f['EVIDENCE_PAGES']))
        previous_pages = 0
        previous_price = Decimal('0')
        for fee in fees:
            if fee['FORMULA'] == 'FIXED':
                continue

            discount = Decimal(fee['PERCENT'])/Decimal('100')

            page_difference = int(fee['EVIDENCE_PAGES']) - previous_pages
            fee_difference = Decimal(fee['TRIAL_FEE'])*discount - previous_price

            fee_per_page = fee_difference/page_difference

            limit_from = previous_pages + 1
            limit_to = int(fee['EVIDENCE_PAGES'])

            price = Price.objects.create(
                scheme=lgfs_scheme,
                scenario=Scenario.objects.get(pk=scenario_clf_to_id(fee['SCENARIO'])),
                fee_type=lit_fee_type,
                advocate_type=None,
                offence_class=OffenceClass.objects.get(pk=fee['OFTY_OFFENCE_TYPE']),
                unit=ppe_unit,
                fee_per_unit=fee_per_page,
                fixed_fee=Decimal(0),
                limit_from=limit_from,
                limit_to=limit_to,
            )
            price.modifiers.add(lgfs_modifier_1)
            price.modifiers.add(lgfs_modifier_2)
            price.save()

            previous_pages = int(fee['EVIDENCE_PAGES'])
            previous_price = Decimal(fee['TRIAL_FEE'])*discount


'''
select bs.scenario, bs.trbc_trial_basis, bs.percent, bs.formula, bs.min_trial_length, bs.min_evidence_pages,
    bf.ofty_offence_type, bf.basic_fee_value, bf.basic_evidence_pages_value, tup.trial_length, tup. trial_uplift_value,
    tup.ppe_cutoff_value
    from bill_scenarios bs join
      basic_fees bf on bs.trbc_trial_basis=bf.trbc_trial_basis join
      trial_uplifts_ppe_cut_offs tup on bf.ofty_offence_type=tup.ofty_offence_type
      where bs.fsth_fee_structure_id=7 and bf.fsth_fee_structure_id=7 and tup.fsth_fee_structure_id=7;
'''
with open('lgfs_joined_day_data.csv') as data_export:
    reader = csv.DictReader(data_export)
    data = defaultdict(listdict)
    for line in reader:
        data[line['SCENARIO']][line['OFTY_OFFENCE_TYPE']].append(line)

for scenario in data:
    for offence_type in data[scenario]:
        fees = sorted(data[scenario][offence_type], key=lambda f: int(f['TRIAL_LENGTH']))
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
