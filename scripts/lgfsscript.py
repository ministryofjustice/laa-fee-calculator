from collections import defaultdict
import csv
from decimal import Decimal

from calculator.models import (
    Price, Scheme, Scenario, FeeType, OffenceClass, Unit, ModifierType, Modifier
)
from calculator.tests.lib.utils import scenario_clf_to_id


def listdict():
    from collections import defaultdict
    return defaultdict(list)


with open('lgfs_joined_ppe_data.csv') as data_export:
    reader = csv.DictReader(data_export)
    data = defaultdict(listdict)
    for line in reader:
        data[line['SCENARIO_ID']][line['OFTY_OFFENCE_TYPE']].append(line)

for scenario in data:
    for offence_type in data[scenario]:
        fees = sorted(data[scenario][offence_type], key=lambda f: int(f['EVIDENCE_PAGES']))
        previous_pages = 0
        previous_price = Decimal('0')
        for fee in fees:
            if fee['FORMULA'] == 'FIXED':
                continue

            discount = Decimal(fee['PERCENT'])/Decimal('100')
            fee_per_page = Decimal(fee['FEE_PER_PAGE'])*discount

            limit_from = previous_pages
            limit_to = int(fee['EVIDENCE_PAGES']) - 1

            price = Price.objects.create(
                scheme=Scheme.objects.get(pk=2),
                scenario=Scenario.objects.get(pk=scenario_clf_to_id(fee['SCENARIO_ID'])),
                fee_type=FeeType.objects.get(pk=100),
                advocate_type=None,
                offence_class=OffenceClass.objects.get(pk=fee['OFTY_OFFENCE_TYPE']),
                unit=Unit.objects.get(pk='PPE'),
                fee_per_unit=fee_per_page,
                fixed_fee=previous_price,
                limit_from=limit_from,
                limit_to=limit_to,
            )
            price.modifiers.add(Modifier.objects.get(pk=12))
            price.modifiers.add(Modifier.objects.get(pk=13))
            price.save()

            previous_pages = int(fee['EVIDENCE_PAGES'])
            previous_price = (Decimal(fee['TRIAL_FEE'])*discount) - previous_price


with open('lgfs_joined_day_data.csv') as data_export:
    reader = csv.DictReader(data_export)
    data = defaultdict(listdict)
    for line in reader:
        data[line['SCENARIO_ID']][line['OFTY_OFFENCE_TYPE']].append(line)

lgfs_scheme = Scheme.objects.get(pk=2),
lit_fee_type = FeeType.objects.get(pk=100),
day_unit = Unit.objects.get(pk='DAY')
ppe_unit = Unit.objects.get(pk='PPE')
day_modifier = ModifierType.objects.get(pk=3)
ppe_modifier = ModifierType.objects.get(pk=4)

for scenario in data:
    for offence_type in data[scenario]:
        fees = sorted(data[scenario][offence_type], key=lambda f: int(f['TRIAL_LENGTH']))
        previous_price = Decimal('0')
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
            step_fee = (total_fee - previous_price)*discount
            previous_price = total_fee

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

            price = Price.objects.create(
                scheme=Scheme.objects.get(pk=2),
                scenario=Scenario.objects.get(pk=scenario_clf_to_id(fee['SCENARIO_ID'])),
                fee_type=FeeType.objects.get(pk=100),
                advocate_type=None,
                offence_class=OffenceClass.objects.get(pk=fee['OFTY_OFFENCE_TYPE']),
                unit=Unit.objects.get(pk='DAY'),
                fee_per_unit=fee_per_unit,
                fixed_fee=fixed_fee,
                limit_from=limit_from,
                limit_to=limit_to,
            )

            # conditional, created = Modifier.objects.get_or_create(
            #     limit_from=0,
            #     limit_to=int(fee['PPE_CUTOFF_VALUE']),
            #     required=True,
            #     fixed_percent=Decimal(0),
            #     percent_per_unit=Decimal(0),
            #     strict_range=False,
            #     priority=0,
            #     modifier_type=ModifierType.objects.get(pk=4)
            # )
            # price.modifiers.add(conditional)

            if (fee['FORMULA'] in ['DAYS', 'PPE'] or
                    fee['TRBC_TRIAL_BASIS'] == 'ELECTED CASE NOT PROCEEDED'):
                price.modifiers.add(Modifier.objects.get(pk=12))
                price.modifiers.add(Modifier.objects.get(pk=13))

            price.save()
