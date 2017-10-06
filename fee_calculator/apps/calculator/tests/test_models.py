# -*- coding: utf-8 -*-
from decimal import Decimal

from django.test import TestCase


from calculator.models import (
    Scheme, Scenario, OffenceClass, FeeType, AdvocateType, Price, Unit, Uplift
)


class PriceTestCase(TestCase):
    fixtures = [
        'advocatetype', 'feetype', 'offenceclass', 'price', 'scenario',
        'scheme', 'unit', 'uplift',
    ]

    def get_test_price(
        self, scheme=None, scenario=None, fee_type=None, offence_class=None,
        advocate_type=None, unit=None, fixed_fee=Decimal('0.00'),
        fee_per_unit=Decimal('1.00'), limit_from=0, limit_to=None, uplifts=[]
    ):
        test_price = Price(
            scheme=scheme or Scheme.objects.all().first(),
            scenario=scenario or Scenario.objects.all().first(),
            fee_type=fee_type or FeeType.objects.all().first(),
            offence_class=offence_class or OffenceClass.objects.all().first(),
            advocate_type=advocate_type or AdvocateType.objects.all().first(),
            unit=unit or Unit.objects.all().first(),
            fixed_fee=fixed_fee,
            fee_per_unit=fee_per_unit,
            limit_from=limit_from,
            limit_to=limit_to
        )
        test_price.save()
        test_price.uplifts = uplifts
        test_price.save()
        return test_price

    def test_get_applicable_unit_count_with_limit_from(self):
        test_price = self.get_test_price(limit_from=5, limit_to=None)

        self.assertEqual(test_price.get_applicable_unit_count(4), 0)
        self.assertEqual(test_price.get_applicable_unit_count(5), 1)
        self.assertEqual(test_price.get_applicable_unit_count(8), 4)
        self.assertEqual(test_price.get_applicable_unit_count(12), 8)
        self.assertEqual(test_price.get_applicable_unit_count(15), 11)

    def test_get_applicable_unit_count_with_limit_to(self):
        test_price = self.get_test_price(limit_from=0, limit_to=12)

        self.assertEqual(test_price.get_applicable_unit_count(4), 4)
        self.assertEqual(test_price.get_applicable_unit_count(5), 5)
        self.assertEqual(test_price.get_applicable_unit_count(8), 8)
        self.assertEqual(test_price.get_applicable_unit_count(12), 12)
        self.assertEqual(test_price.get_applicable_unit_count(15), 12)

    def test_get_applicable_unit_count_with_range(self):
        test_price = self.get_test_price(limit_from=5, limit_to=12)

        self.assertEqual(test_price.get_applicable_unit_count(4), 0)
        self.assertEqual(test_price.get_applicable_unit_count(5), 1)
        self.assertEqual(test_price.get_applicable_unit_count(8), 4)
        self.assertEqual(test_price.get_applicable_unit_count(12), 8)
        self.assertEqual(test_price.get_applicable_unit_count(15), 8)

    def test_get_uplift_fees_with_single_qualifying(self):
        case_unit = Unit.objects.get(id='CASE')
        uplift = Uplift(
            unit=case_unit, limit_from=2, limit_to=None,
            uplift_percent=Decimal('15.00')
        )
        uplift.save()

        test_price = self.get_test_price(uplifts=[uplift])

        self.assertEqual(
            test_price.get_uplift_fees(Decimal('10.00'), case_unit, 2),
            [Decimal('1.50')]
        )

    def test_get_uplift_fees_with_multiple_qualifying(self):
        case_unit = Unit.objects.get(id='CASE')
        case_uplift = Uplift(
            unit=case_unit, limit_from=2, limit_to=None,
            uplift_percent=Decimal('15.00')
        )
        case_uplift.save()
        defendant_unit = Unit.objects.get(id='DEFENDANT')
        defendant_uplift = Uplift(
            unit=defendant_unit, limit_from=2, limit_to=None,
            uplift_percent=Decimal('25.00')
        )
        defendant_uplift.save()

        test_price = self.get_test_price(
            uplifts=[case_uplift, defendant_uplift]
        )

        self.assertEqual(
            test_price.get_uplift_fees(Decimal('10.00'), case_unit, 2),
            [Decimal('1.50')]
        )
        self.assertEqual(
            test_price.get_uplift_fees(Decimal('10.00'), defendant_unit, 2),
            [Decimal('2.50')]
        )

    def test_get_uplift_fees_with_some_not_qualifying(self):
        case_unit = Unit.objects.get(id='CASE')
        case_uplift1 = Uplift(
            unit=case_unit, limit_from=2, limit_to=None,
            uplift_percent=Decimal('15.00')
        )
        case_uplift1.save()
        case_uplift2 = Uplift(
            unit=case_unit, limit_from=0, limit_to=1,
            uplift_percent=Decimal('25.00')
        )
        case_uplift2.save()

        test_price = self.get_test_price(
            uplifts=[case_uplift1, case_uplift2]
        )

        self.assertEqual(
            test_price.get_uplift_fees(Decimal('10.00'), case_unit, 1),
            [Decimal('2.50')]
        )

    def test_calculate_total_1(self):
        day_unit = Unit.objects.get(id='DAY')
        case_unit = Unit.objects.get(id='CASE')
        case_uplift = Uplift(
            unit=case_unit, limit_from=2, limit_to=None,
            uplift_percent=Decimal('15.00')
        )
        case_uplift.save()

        test_price = self.get_test_price(
            unit=day_unit,
            fixed_fee=Decimal('10.00'),
            fee_per_unit=Decimal('1.00'),
            uplifts=[case_uplift],
            limit_from=5,
            limit_to=12
        )

        self.assertEqual(
            test_price.calculate_total(12, [(case_unit, 2)]),
            Decimal('20.70')
        )

    def test_calculate_total_2(self):
        day_unit = Unit.objects.get(id='DAY')
        case_unit = Unit.objects.get(id='CASE')
        case_uplift = Uplift(
            unit=case_unit, limit_from=2, limit_to=None,
            uplift_percent=Decimal('15.00')
        )
        case_uplift.save()
        defendant_unit = Unit.objects.get(id='DEFENDANT')
        defendant_uplift = Uplift(
            unit=defendant_unit, limit_from=2, limit_to=None,
            uplift_percent=Decimal('25.00')
        )
        defendant_uplift.save()

        test_price = self.get_test_price(
            unit=day_unit,
            fixed_fee=Decimal('10.00'),
            fee_per_unit=Decimal('1.00'),
            uplifts=[case_uplift, defendant_uplift],
            limit_from=5,
            limit_to=12
        )

        self.assertEqual(
            test_price.calculate_total(
                12, [(case_unit, 2), (defendant_unit, 3)]
            ),
            Decimal('25.20')
        )

    def test_calculate_total_3(self):
        day_unit = Unit.objects.get(id='DAY')
        case_unit = Unit.objects.get(id='CASE')

        test_price = self.get_test_price(
            unit=day_unit,
            fixed_fee=Decimal('0.00'),
            fee_per_unit=Decimal('1.00'),
            uplifts=[],
            limit_from=0,
            limit_to=None
        )

        self.assertEqual(
            test_price.calculate_total(12, [(case_unit, 2)]),
            Decimal('12.00')
        )
