from django.core.management import BaseCommand

from calculator.models import (Scheme, Price)

import csv


def csv_to_json(csv_file_path):
    json_array = []

    with open(csv_file_path, encoding='utf-8-sig') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            json_array.append(row)
    return json_array


base_path = 'fee_calculator/apps/calculator/management/commands/agfs_2022_data'
basic_fees = csv_to_json(f'{base_path}/basic_fees.csv')
fixed_and_misc_fees = csv_to_json(f'{base_path}/fixed_and_misc_fees.csv')
advocate_codes = {'JUNIOR': 'J', 'LEADJR': 'L', 'QC': 'Q'}
scenario_codes = {
    'Guilty plea': 'P',
    'Cracked trial': 'C',
    'Trial': 'T',
    # TODO: Check the correct codes for these scenarios
    'Retrial': 'T',
    'Cracked before retrial': 'C',
    'Discontinuance': 'P',
    'Warrant issued - trial': 'P'
}


def fee_code_for(advocate_type, scenario, refresher=False):
    try:
        return f'{advocate_codes[advocate_type.id]} {"R" if refresher else scenario_codes[scenario.name]}'
    except KeyError:
        raise KeyError(f'Failed to find: {advocate_type.id}/{scenario.name}')


def basic_fixed_fee_for(offence_class, advocate_type, scenario, refresher=False):
    for fee in basic_fees:
        if offence_class.id == fee['Band']:
            return float(fee[fee_code_for(advocate_type, scenario, refresher)])


def fixed_and_misc_fee_for(fee_name, advocate_type):
    for fee in fixed_and_misc_fees:
        if fee_name == fee['Fee name']:
            return float(fee[advocate_type.name])

    raise KeyError(f'Failed to find: {fee_name}')


class Command(BaseCommand):
    help = '''
        Uplift fees in the 2022 LGFS Fee Scheme
    '''

    def handle(self, *args, **options):
        scheme = Scheme.objects.get(pk=7)
        prices = Price.objects.filter(scheme=scheme)

        fees_to_be_processed = prices.count()
        elected_case_count = 0
        basic_fee_count = 0
        basic_fee_skip_count = 0
        fixed_and_misc_fee_count = 0
        fixed_and_misc_fee_zero_count = 0
        fixed_and_misc_fee_skip_count = 0

        for price in prices:
            # elected cases not proceeded. these are no longer included in the fee scheme and so are deleted
            if price.scenario.id in [12]:
                print(f'Deleting elected case fee {price.pk}')
                price.delete()
                elected_case_count += 1
                continue

            # basic fees. updated based on values held in agfs_2022_data/basic_fees.csv
            if price.offence_class is not None:
                if price.scenario.name == 'Cracked before retrial':
                    new_price = basic_fixed_fee_for(price.offence_class, price.advocate_type, price.scenario)
                    print(f'Offence Class: {price.offence_class.id} - {price.offence_class.name}')
                    print(f'               {price.offence_class.description}')
                    print(f'  {price.id}')
                    print(f'  Advocate type: {price.advocate_type.name}')
                    print(f'  Scenario: {price.scenario.name}')
                    print('  Fixed fee:     £{:.2f}'.format(price.fixed_fee))
                    print('  New basic fee: £{:.2f}'.format(new_price))
                    if price.fixed_fee == new_price * 0.5 or price.fixed_fee == new_price * 0.85:
                        basic_fee_count += 1
                        continue

                    if (abs(float(price.fixed_fee)*1.15 - new_price * 0.5) < 10):
                        print('  Setting to 50%% of new basic fee')
                        price.fixed_fee = new_price * 0.5
                        price.save()
                        basic_fee_count += 1
                        continue
                    elif (abs(float(price.fixed_fee)*1.15 - new_price * 0.85) < 10):
                        print('  Setting to 50%% of new basic fee')
                        price.fixed_fee = new_price * 0.85
                        price.save()
                        basic_fee_count += 1
                        continue
                    else:
                        print('  FAILED TO SET NEW PRICE')
                        continue

                if price.fixed_fee > 0:
                    new_price = basic_fixed_fee_for(price.offence_class, price.advocate_type, price.scenario)
                    print(f'Offence Class: {price.offence_class.id} - {price.offence_class.name}')
                    print(f'               {price.offence_class.description}')
                    print(f'  {price.id}')
                    print(f'  Advocate type: {price.advocate_type.name}')
                    print(f'  Scenario: {price.scenario.name}')
                    print('  Fixed fee:     £{:.2f}'.format(price.fixed_fee))
                    print('  New basic fee: £{:.2f}'.format(new_price))
                    if price.fixed_fee == new_price:
                        basic_fee_count += 1
                        continue

                    if (abs(float(price.fixed_fee)*1.15 - new_price) > 1):
                        print('  MORE THAN £1 DIFFERENCT FROM 15% UPLIFT - NOT CHANGING')
                        basic_fee_skip_count += 1
                        continue
                    else:
                        price.fixed_fee = new_price
                        price.save()
                        basic_fee_count += 1
                        continue
                else:
                    new_price = basic_fixed_fee_for(price.offence_class, price.advocate_type, price.scenario, True)
                    print(f'Offence Class: {price.offence_class.id} - {price.offence_class.name}')
                    print(f'               {price.offence_class.description}')
                    print(f'  {price.id}')
                    print(f'  Advocate type: {price.advocate_type.name}')
                    print(f'  Scenario: {price.scenario.name}')
                    print(f'  Fee per unit: {price.fee_per_unit}')
                    print(f'  Unit: {price.unit}')

                    if price.fee_per_unit == new_price:
                        basic_fee_count += 1
                        continue

                    if (abs(float(price.fee_per_unit)*1.15 - new_price) > 1):
                        print('  MORE THAN £1 DIFFERENCT FROM 15% UPLIFT - NOT CHANGING')
                        basic_fee_skip_count += 1
                        continue
                    else:
                        price.fee_per_unit = new_price
                        price.save()
                        basic_fee_count += 1
                        continue

            # if price.fee_type.name not in ['Paper heavy case']:
            if True:
                print('Offence Class: NONE')
                print(f'  Advocate: {price.advocate_type.name}')
                print(f'  Fee type: {price.fee_type.name}')
                print(f'  Fee per unit: {price.fee_per_unit}')

                if price.fee_per_unit == 0:
                    fixed_and_misc_fee_zero_count += 1
                    continue

                new_price = fixed_and_misc_fee_for(price.fee_type.name, price.advocate_type)
                print(f'  New fee: {new_price}')

                if float(price.fee_per_unit) == float(new_price):
                    fixed_and_misc_fee_count += 1
                    continue

                if (abs(float(price.fee_per_unit)*1.15 - new_price) > 1):
                    fixed_and_misc_fee_skip_count += 1
                    print('  MORE THAN £1 DIFFERENCT FROM 15% UPLIFT - NOT CHANGING')
                    continue
                else:
                    price.fee_per_unit = new_price
                    price.save()
                    fixed_and_misc_fee_count += 1
                    continue

        print(f'{elected_case_count} elected case fees were deleted')
        print(f'{basic_fee_count} basic fees were updated')
        print(f'{basic_fee_skip_count} basic fees were SKIPPED')
        print(f'{fixed_and_misc_fee_count} fixed and misc fees were updated')
        print(f'{fixed_and_misc_fee_zero_count} fixed and misc fees were not changed (£0)')
        print(f'{fixed_and_misc_fee_skip_count} fixed and misc fees were SKIPPED')

        total = elected_case_count + basic_fee_count + fixed_and_misc_fee_count + fixed_and_misc_fee_zero_count

        print(f'{total} out of {fees_to_be_processed} fees were processed')
