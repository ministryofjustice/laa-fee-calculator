import os
from collections import Counter
from decimal import Decimal

from django.core.management import call_command

from calculator.models import Price, ScenarioCode
from calculator.tests.base import Agfs10PlusCalculatorTestCase, Agfs10PlusWarrantFeeTestMixin, CalculatorTestCase


class Agfs18CalculatorTestCase(Agfs10PlusCalculatorTestCase, Agfs10PlusWarrantFeeTestMixin):
    scheme_id = 15
    csv_path = os.path.join(os.path.dirname(__file__), 'data/test_dataset_agfs_17.csv')


Agfs18CalculatorTestCase.create_tests()


class Agfs18HearingFeeTestCase(CalculatorTestCase):
    scheme_id = 15
    rates = {
        'AGFS_SENT_ADD': ('hour', ('48.02', '68.94', '91.11')),
        'AGFS_MITIG': ('day', ('166.00', '266.00', '400.00')),
        'AGFS_MIT_ADD': ('hour', ('48.02', '68.94', '91.11')),
        'AGFS_BAIL_APP': ('day', ('118.00', '176.00', '234.00')),
    }
    grades = {'JUNIOR': 0, 'LEADJR': 1, 'KC': 2}

    def test_rates_for_every_agfs_scenario_and_advocate_grade(self):
        scenarios = ScenarioCode.objects.filter(scheme_type=1).values_list('scenario_id', flat=True)
        for scenario in scenarios:
            for grade, rate_index in self.grades.items():
                for code, (unit, rates) in self.rates.items():
                    quantities = ('0', '0.5', '1', '1.5', '3.25') if unit == 'hour' else ('0', '1', '3')
                    for quantity in quantities:
                        with self.subTest(scenario=scenario, grade=grade, code=code, quantity=quantity):
                            count = Decimal(quantity)
                            rate = Decimal(rates[rate_index])
                            expected = rate * count if unit == 'hour' else rate
                            if count < 1:
                                expected = Decimal('0')
                            data = {
                                'scenario': scenario,
                                'advocate_type': grade,
                                'fee_type_code': code,
                                unit: quantity,
                                'number_of_defendants': 3,
                                'number_of_cases': 2,
                            }
                            self.check_result(data, expected.quantize(Decimal('0.01')))

    def test_prices_are_independent_of_offence_class_and_have_no_modifiers(self):
        for code in self.rates:
            prices = Price.objects.filter(scheme_id=15, fee_type__code=code)
            self.assertTrue(prices.exists())
            self.assertFalse(prices.filter(offence_class__isnull=False).exists())
            self.assertFalse(prices.filter(modifiers__isnull=False).exists())
            self.assertFalse(Price.objects.filter(scheme_id=14, fee_type__code=code).exists())

    def test_existing_prices_and_modifiers_are_identical_to_scheme_17(self):
        def signatures(prices):
            return Counter(
                (
                    price.scenario_id, price.advocate_type_id, price.offence_class_id,
                    price.fee_type_id, price.unit_id, price.fixed_fee, price.fee_per_unit,
                    price.limit_from, price.limit_to, price.strict_range,
                    tuple(sorted(modifier.pk for modifier in price.modifiers.all())),
                )
                for price in prices.prefetch_related('modifiers')
            )

        previous = Price.objects.filter(scheme_id=14)
        inherited = Price.objects.filter(scheme_id=15).exclude(fee_type__code__in=self.rates)
        self.assertTrue(previous.exists())
        self.assertEqual(signatures(previous), signatures(inherited))

    def test_generator_is_repeatable(self):
        before = Price.objects.filter(scheme_id=15).count()
        call_command('add_agfs_scheme_18', verbosity=0)
        self.assertEqual(Price.objects.filter(scheme_id=15).count(), before)
        self.test_existing_prices_and_modifiers_are_identical_to_scheme_17()
