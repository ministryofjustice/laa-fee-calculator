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
    'Retrial': 'T',  # Percentage of basic fee
    'Cracked before retrial': 'C',  # Percentage of basic fee
    'Discontinuance': 'P',
    # Mapping for 'warrant issued' depends on when the warrant was issued
    # Not clear where 'trial' is the only scenario
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


def check_uplift(old_price, new_price, limit=1):
    return abs(float(old_price)*1.15 - float(new_price)) < limit


class Command(BaseCommand):
    help = '''
        Uplift fees in the 2022 LGFS Fee Scheme
    '''

    def handle(self, *args, **options):
        scheme = Scheme.objects.get(pk=7)
        prices = Price.objects.filter(scheme=scheme)

        fees_to_be_processed = prices.count()
        counters = {
            'elected_case_count': 0,
            'basic_fee_count': 0,
            'basic_fee_skip_count': 0,
            'fixed_and_misc_fee_count': 0,
            'fixed_and_misc_fee_zero_count': 0,
            'fixed_and_misc_fee_skip_count': 0
        }

        for price in prices:
            # elected cases not proceeded. these are no longer included in the fee scheme and so are deleted
            if price.scenario.id in [12]:
                print(f'Deleting elected case fee {price.pk}')
                price.delete()
                counters['elected_case_count'] += 1
                continue

            # fixed and misc fees
            if price.offence_class is None:
                print('Offence Class: NONE')
                print(f'  Advocate: {price.advocate_type.name}')
                print(f'  Fee type: {price.fee_type.name}')
                print(f'  Fee per unit: {price.fee_per_unit}')

                if price.fee_per_unit == 0:
                    counters['fixed_and_misc_fee_zero_count'] += 1
                    continue

                new_price = fixed_and_misc_fee_for(price.fee_type.name, price.advocate_type)
                print(f'  New fee: {new_price}')

                if float(price.fee_per_unit) == float(new_price):
                    counters['fixed_and_misc_fee_count'] += 1
                    continue

                if check_uplift(price.fee_per_unit, new_price):
                    price.fee_per_unit = new_price
                    price.save()
                    counters['fixed_and_misc_fee_count'] += 1
                    continue
                else:
                    counters['fixed_and_misc_fee_skip_count'] += 1
                    print('  MORE THAN £1 DIFFERENCT FROM 15% UPLIFT - NOT CHANGING')
                    continue

            # basic fees. updated based on values held in agfs_2022_data/basic_fees.csv
            else:
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
                        counters['basic_fee_count'] += 1
                        continue

                    if check_uplift(price.fixed_fee, new_price * 0.5, 10):
                        print('  Setting to 50%% of new basic fee')
                        price.fixed_fee = new_price * 0.5
                        price.save()
                        counters['basic_fee_count'] += 1
                        continue
                    if check_uplift(price.fixed_fee, new_price * 0.85, 10):
                        print('  Setting to 50%% of new basic fee')
                        price.fixed_fee = new_price * 0.85
                        price.save()
                        counters['basic_fee_count'] += 1
                        continue
                    else:
                        print('  FAILED TO SET NEW PRICE')
                        continue

                new_price = basic_fixed_fee_for(price.offence_class, price.advocate_type,
                                                price.scenario, price.fixed_fee == 0)
                print(f'Offence Class: {price.offence_class.id} - {price.offence_class.name}')
                print(f'               {price.offence_class.description}')
                print(f'  {price.id}')
                print(f'  Advocate type: {price.advocate_type.name}')
                print(f'  Scenario: {price.scenario.name}')
                print('  Fixed fee:     £{:.2f}'.format(price.fixed_fee))
                print('  Fee per unit:  £{:.2f}'.format(price.fee_per_unit))
                print('  New basic fee: £{:.2f}'.format(new_price))

                fee_field = 'fixed_fee' if price.fixed_fee > 0 else 'fee_per_unit'
                old_price = getattr(price, fee_field)

                if old_price == new_price:
                    counters['basic_fee_count'] += 1
                    continue

                # if price.fixed_fee == new_price or price.fee_per_unit == new_price:
                #     counters['basic_fee_count'] += 1
                #     continue

                # old_price = price.fixed_fee if price.fixed_fee > 0 else price.fee_per_unit

                if check_uplift(old_price, new_price):
                    setattr(price, fee_field, new_price)
                    price.save()
                    counters['basic_fee_count'] += 1
                    continue
                else:
                    print('  MORE THAN £1 DIFFERENCT FROM 15% UPLIFT - NOT CHANGING')
                    counters['basic_fee_skip_count'] += 1
                    continue

        print(f"{counters['elected_case_count']} elected case fees were deleted")
        print(f"{counters['basic_fee_count']} basic fees were updated")
        print(f"{counters['basic_fee_skip_count']} basic fees were SKIPPED")
        print(f"{counters['fixed_and_misc_fee_count']} fixed and misc fees were updated")
        print(f"{counters['fixed_and_misc_fee_zero_count']} fixed and misc fees were not changed (£0)")
        print(f"{counters['fixed_and_misc_fee_skip_count']} fixed and misc fees were SKIPPED")

        total = counters['elected_case_count'] + counters['basic_fee_count'] + \
            counters['fixed_and_misc_fee_count'] + counters['fixed_and_misc_fee_zero_count']

        print(f'{total} out of {fees_to_be_processed} fees were processed')
