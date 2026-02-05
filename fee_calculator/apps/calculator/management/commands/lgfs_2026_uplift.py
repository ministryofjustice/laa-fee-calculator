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


base_path = 'fee_calculator/apps/calculator/management/commands/lgfs_2026_data'
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


GRADUATED_FEE_SCENARIOS = [1, 2, 3, 4, 10, 11, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28,
                           29, 30, 31, 33, 34, 35, 36, 43, 44, 45, 46, 48, 49, 50, 55, 56]  # All graduated fees
FIXED_FEE_SCENARIOS = [5, 6]  # Appeal against conviction, Appeal against sentence


class Command(BaseCommand):
    help = 'Uplift fees in the 2026 LGFS Fee Scheme'

    def handle(self, *args, **options):
        scheme = Scheme.objects.get(pk=13)  # New LGFS Scheme 11 Feb 2026
        prices = Price.objects.filter(scheme=scheme)

        fees_to_be_processed = prices.count()
        fixed_fee_count = 0
        grad_fee_count = 0
        skipped_fee_count = 0

        for price in prices:
            if price.unit.id == 'DAY' and price.fixed_fee == 0:
                # print(f'Skipping trial day proxy {price.pk}')
                skipped_fee_count += 1
                continue

            # evidence provision fees. these are not being increased and so no action is taken
            if price.fee_type.id == 47:
                # print(f'Skipping evidence provision fee {price.pk}')
                skipped_fee_count += 1
                continue

            # Fixed fees - update
            if price.scenario.id in FIXED_FEE_SCENARIOS:
                new_fee = fixed_fee_for(price.scenario.id)
                if new_fee:
                    print(f'Scenario: {price.scenario.name}')
                    print('  Current fixed fee: £{:.2f}'.format(price.fixed_fee))
                    print('  New fixed fee: £{:.2f}'.format(new_fee))
                    print('')
                    price.fixed_fee = new_fee
                    price.save()
                    fixed_fee_count += 1
                    continue

            # Graduated fees - update
            if price.scenario.id in GRADUATED_FEE_SCENARIOS:
                scenario, price_modifier = map_scenario(price.scenario.id)
                new_fee = graduated_fee_for(scenario, price.offence_class.id, price.limit_from) * price_modifier
                if new_fee:
                    print(f'Scenario: {price.scenario.name}')
                    print(f'Offence: {price.offence_class.id}')
                    print(f' Unit: {price.unit.id}')
                    print('  Limit from: {}'.format(price.limit_from))
                    print('  Limit to: {}'.format(price.limit_to))
                    print('  Current fee: £{:.2f}'.format(price.fixed_fee))
                    print('  New fee: £{:.2f}'.format(new_fee))
                    print('')
                    price.fixed_fee = new_fee
                    price.save()
                    grad_fee_count += 1
                    continue

            # Skip all other scenarios
            # print(f'Skipping scenario: {price.scenario.name} (ID: {price.scenario.id})')
            skipped_fee_count += 1

        print('\n=== Summary ===')
        print(f'{fixed_fee_count} fixed fees were updated')
        print(f'{grad_fee_count} graduated fees were updated')
        print(f'{skipped_fee_count} fees were left unchanged')

        total = fixed_fee_count + grad_fee_count + skipped_fee_count
        print(f'{total} out of {fees_to_be_processed} fees were processed')
