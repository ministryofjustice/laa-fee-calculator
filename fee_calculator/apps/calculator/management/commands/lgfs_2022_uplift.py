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


base_path = 'fee_calculator/apps/calculator/management/commands/lgfs_2022_data'
fixed_fees = csv_to_json(f'{base_path}/fixed_fees.csv')
graduated_fees = csv_to_json(f'{base_path}/graduated_fees.csv')
scenario_mappings = csv_to_json(f'{base_path}/scenario_mappings.csv')


def fixed_fee_for(scenario):
    for fee in fixed_fees:
        if scenario == int(fee['scenario']):
            return float(fee['fee'])


def graduated_fee_for(scenario, offence, limit_from):
    for fee in graduated_fees:
        if scenario == int(fee['scenario']) and offence == fee['offence'] and limit_from == int(fee['limit_from']):
            return float(fee['fee'])


# all graduated fees are a percentage of the fee for the trial, cracked trial or guilty plea scenarios.
# this function maps the scenario being updated to the correct base scenario and percentage modifier
def map_scenario(scenario):
    for mapped_scenario in scenario_mappings:
        if scenario == int(mapped_scenario['scenario']):
            return int(mapped_scenario['mapped_scenario']), float(mapped_scenario['price_modifier'])


class Command(BaseCommand):
    help = '''
        Uplift fees in the 2022 LGFS Fee Scheme
    '''

    def handle(self, *args, **options):
        scheme = Scheme.objects.get(pk=6)
        prices = Price.objects.filter(scheme=scheme)

        fees_to_be_processed = prices.count()
        trial_day_count = 0
        evidence_provision_fee_count = 0
        elected_case_count = 0
        fixed_fee_count = 0
        grad_fee_count = 0

        for price in prices:
            # trial day proxy values. these are not being increased and so no action is taken
            if price.unit.id == 'DAY' and price.fixed_fee == 0:
                print(f'Skipping trial day proxy {price.pk}')
                trial_day_count += 1
                continue

            # evidence provision fees. these are not being increased and so no action is taken
            if price.fee_type.id == 47:
                print(f'Skipping evidence provision fee {price.pk}')
                evidence_provision_fee_count += 1
                continue

            # elected cases not proceeded. these are no longer included in the fee scheme and so are deleted
            if price.scenario.id in [12, 37, 38, 39, 40, 41, 42]:
                print(f'Deleting elected case fee {price.pk}')
                price.delete()
                elected_case_count += 1
                continue

            # fixed fees. updated based on values held in lgfs_2022_data/fixed_fees.csv
            if price.scenario.id in [5, 6, 7, 8, 9, 32, 51, 52, 53, 54]:
                print(f'Scenario: {price.scenario.name}')
                print('  Fixed fee: £{:.2f}'.format(price.fixed_fee))
                price.fixed_fee = fixed_fee_for(price.scenario.id)
                price.save()
                print('  New fixed fee: £{:.2f}'.format(price.fixed_fee))
                fixed_fee_count += 1
                continue

            # all other fees are graduated fees. update based on values held in lgfs_2022_data/graduated_fees.csv
            print(f'Scenario: {price.scenario.name}')
            print(f'Offence: {price.offence_class.id}')
            print('  Existing fee: £{:.2f}'.format(price.fixed_fee))
            scenario, price_modifier = map_scenario(price.scenario.id)
            price.fixed_fee = graduated_fee_for(scenario, price.offence_class.id, price.limit_from) * price_modifier
            price.save()
            print('  New fee: £{:.2f}'.format(price.fixed_fee))
            grad_fee_count += 1

        print(f'{trial_day_count} trial day proxies were skipped')
        print(f'{evidence_provision_fee_count} evidence provision fees were skipped')
        print(f'{elected_case_count} elected case fees were deleted')
        print(f'{fixed_fee_count} fixed fees were updated')
        print(f'{grad_fee_count} graduated fees were updated')

        total = trial_day_count + evidence_provision_fee_count + elected_case_count + fixed_fee_count + grad_fee_count
        print(f'{total} out of {fees_to_be_processed} fees were processed')
