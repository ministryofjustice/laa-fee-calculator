'''
This script, using data exported using the commented SQL statements, will create
the required prices for the advocate fee scheme 10.
'''
import csv
from decimal import Decimal

from calculator.models import (
    Price, Scheme, Scenario, FeeType, OffenceClass, Unit, Modifier, AdvocateType
)
from calculator.tests.lib.utils import scenario_ccr_to_id

agfs_scheme = Scheme.objects.get(pk=3)
basic_agfs_fee = FeeType.objects.get(pk=34)

day_unit = Unit.objects.get(pk='DAY')

case_modifier = Modifier.objects.get(pk=1)
defendant_modifier = Modifier.objects.get(pk=2)
retrial_0_month_modifier = Modifier.objects.get(pk=8)
retrial_1_month_modifier = Modifier.objects.get(pk=9)
retrial_cracked_0_month_modifier = Modifier.objects.get(pk=10)
retrial_cracked_1_month_modifier = Modifier.objects.get(pk=11)


'''
select bs.id as scenario_id, bs.trbc_trial_basis, bf.basic_fee_value,
    bf.psty_person_type, bf.trial_day_from, bf.trial_day_to, bf.unit,
    bf.offence_band, bf.third
    from bill_scenarios bs
        join basic_fees bf on bs.trbc_trial_basis=bf.trbc_trial_basis
        where bs.fsth_fee_structure_id=11 and bf.fsth_fee_structure_id=11;
'''
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

        scenario_id = scenario_ccr_to_id(fee['SCENARIO_ID'], fee['THIRD'], scheme=10)
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

        price.save()


'''
select mf.psty_person_type, mf.limit_from, mf.limit_to, mf.fee_per_unit,
    mf.unit, mf.bist_bill_sub_type, mf.bisc_bill_scenario_id,
    bst.defendant_uplift_allowed, bst.case_uplift_allowed
        from misc_fees mf
            join bill_scenarios bs on bs.id=mf.bisc_bill_scenario_id
            join bill_sub_types bst on mf.bist_bill_sub_type=bst.bill_sub_type
            where bs.fsth_fee_structure_id=11;
'''
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

        try:
            scenario_ids = [scenario_ccr_to_id(fee['BISC_BILL_SCENARIO_ID'], None, scheme=10)]
        except ValueError:
            scenario_ids = []
            for third in range(1, 4):
                scenario_ids.append(scenario_ccr_to_id(fee['BISC_BILL_SCENARIO_ID'], third, scheme=10))

        for scenario_id in scenario_ids:
            price = Price.objects.create(
                scheme=agfs_scheme,
                scenario=Scenario.objects.get(pk=scenario_id),
                fee_type=FeeType.objects.get(code=fee['BIST_BILL_SUB_TYPE']),
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
