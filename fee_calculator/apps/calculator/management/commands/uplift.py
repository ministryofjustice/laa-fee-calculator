from django.core.management import BaseCommand

from calculator.models import (Scheme, Price)


class Command(BaseCommand):
    help = '''
        Uplift all fees in a scheme
    '''

    def add_arguments(self, parser):
        parser.add_argument(
            'scheme_id', type=int,
            help='ID of fee scheme'
        )
        parser.add_argument(
            'percentage', type=float,
            help='Percentage to increase'
        )

    def handle(self, *args, **options):
        scheme = Scheme.objects.get(pk=options['scheme_id'])
        multiplier = 1 + options['percentage'] / 100
        prices = Price.objects.filter(scheme=scheme)

        for price in prices:
            if price.fee_type is not None:
                print('Fee type: {:s} ({:s})'.format(price.fee_type.name, price.fee_type.code))
            else:
                print('Fee type: UNKNOWN')

            print('Scenario: {:s}'.format(price.scenario.name))
            print('Advocate type: {:s}'.format(price.advocate_type.name if price.advocate_type is not None else '-'))

            print('  Fixed fee: £{:.2f}'.format(price.fixed_fee))
            price.fixed_fee = float(price.fixed_fee) * multiplier
            print('  New fixed fee: £{:.2f}'.format(price.fixed_fee))
            print('  Fee per unit: £{:.2f}'.format(price.fee_per_unit))
            price.fee_per_unit = float(price.fee_per_unit) * multiplier
            print('  New fee per unit: £{:.2f}'.format(price.fee_per_unit))
            price.save()
