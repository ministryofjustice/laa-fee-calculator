# -*- coding: utf-8 -*-
from decimal import Decimal

from django.test import TestCase


from calculator.models import (
    Scheme, Scenario, OffenceClass, FeeType, AdvocateType, Price, Unit,
    Modifier, ModifierValue
)


def create_test_price(
    scheme=None, scenario=None, fee_type=None, offence_class=None,
    advocate_type=None, unit=None, fixed_fee=Decimal('0.00'),
    fee_per_unit=Decimal('1.00'), limit_from=0, limit_to=None, modifiers=[]
):
    test_price = Price.objects.create(
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
    test_price.modifiers = modifiers
    test_price.save()
    return test_price


def create_test_modifier(
    name='Test modifier', description='Test modifier', unit=None, values=[]
):
    modifier = Modifier.objects.create(
        name=name, description=description, unit=unit
    )
    for value in values:
        ModifierValue.objects.create(
            limit_from=value['limit_from'], limit_to=value['limit_to'],
            modifier_percent=value['modifier_percent'], modifier=modifier
        )
    return modifier


class PriceTestCase(TestCase):
    fixtures = [
        'advocatetype', 'feetype', 'offenceclass', 'price', 'scenario',
        'scheme', 'unit', 'modifier', 'modifiervalue',
    ]

    def test_get_applicable_unit_count_with_limit_from(self):
        test_price = create_test_price(limit_from=5, limit_to=None)

        self.assertEqual(test_price.get_applicable_unit_count(4), 0)
        self.assertEqual(test_price.get_applicable_unit_count(5), 1)
        self.assertEqual(test_price.get_applicable_unit_count(8), 4)
        self.assertEqual(test_price.get_applicable_unit_count(12), 8)
        self.assertEqual(test_price.get_applicable_unit_count(15), 11)

    def test_get_applicable_unit_count_with_limit_to(self):
        test_price = create_test_price(limit_from=0, limit_to=12)

        self.assertEqual(test_price.get_applicable_unit_count(4), 4)
        self.assertEqual(test_price.get_applicable_unit_count(5), 5)
        self.assertEqual(test_price.get_applicable_unit_count(8), 8)
        self.assertEqual(test_price.get_applicable_unit_count(12), 12)
        self.assertEqual(test_price.get_applicable_unit_count(15), 12)

    def test_get_applicable_unit_count_with_range(self):
        test_price = create_test_price(limit_from=5, limit_to=12)

        self.assertEqual(test_price.get_applicable_unit_count(4), 0)
        self.assertEqual(test_price.get_applicable_unit_count(5), 1)
        self.assertEqual(test_price.get_applicable_unit_count(8), 4)
        self.assertEqual(test_price.get_applicable_unit_count(12), 8)
        self.assertEqual(test_price.get_applicable_unit_count(15), 8)

    def test_get_modifier_fees_with_single_qualifying(self):
        case_unit = Unit.objects.get(id='CASE')
        modifier = create_test_modifier(
            unit=case_unit, values=[
                dict(limit_from=2, limit_to=None, modifier_percent=Decimal('15.00'))
            ]
        )

        test_price = create_test_price(modifiers=[modifier])

        self.assertEqual(
            test_price.get_modifier_fees(Decimal('10.00'), modifier, 2),
            [Decimal('1.50')]
        )

    def test_get_modifier_fees_with_multiple_qualifying(self):
        case_unit = Unit.objects.get(id='CASE')
        case_modifier = create_test_modifier(
            unit=case_unit, values=[
                dict(limit_from=2, limit_to=None, modifier_percent=Decimal('15.00'))
            ]
        )
        defendant_unit = Unit.objects.get(id='DEFENDANT')
        defendant_modifier = create_test_modifier(
            unit=defendant_unit, values=[
                dict(limit_from=2, limit_to=None, modifier_percent=Decimal('25.00'))
            ]
        )

        test_price = create_test_price(
            modifiers=[case_modifier, defendant_modifier]
        )

        self.assertEqual(
            test_price.get_modifier_fees(Decimal('10.00'), case_modifier, 2),
            [Decimal('1.50')]
        )
        self.assertEqual(
            test_price.get_modifier_fees(Decimal('10.00'), defendant_modifier, 2),
            [Decimal('2.50')]
        )

    def test_get_modifier_fees_with_some_not_qualifying(self):
        case_unit = Unit.objects.get(id='CASE')
        case_modifier = create_test_modifier(
            unit=case_unit, values=[
                dict(limit_from=2, limit_to=None, modifier_percent=Decimal('15.00')),
                dict(limit_from=1, limit_to=1, modifier_percent=Decimal('25.00'))
            ]
        )

        test_price = create_test_price(
            modifiers=[case_modifier]
        )

        self.assertEqual(
            test_price.get_modifier_fees(Decimal('10.00'), case_modifier, 1),
            [Decimal('2.50')]
        )

    def test_calculate_total_1(self):
        day_unit = Unit.objects.get(id='DAY')
        case_unit = Unit.objects.get(id='CASE')
        case_modifier = create_test_modifier(
            unit=case_unit, values=[
                dict(limit_from=2, limit_to=None, modifier_percent=Decimal('15.00'))
            ]
        )

        test_price = create_test_price(
            unit=day_unit,
            fixed_fee=Decimal('10.00'),
            fee_per_unit=Decimal('1.00'),
            modifiers=[case_modifier],
            limit_from=5,
            limit_to=12
        )

        self.assertEqual(
            test_price.calculate_total(12, [(case_modifier, 2)]),
            Decimal('20.70')
        )

    def test_calculate_total_2(self):
        day_unit = Unit.objects.get(id='DAY')
        case_unit = Unit.objects.get(id='CASE')
        case_modifier = create_test_modifier(
            unit=case_unit, values=[
                dict(limit_from=2, limit_to=None, modifier_percent=Decimal('15.00'))
            ]
        )
        defendant_unit = Unit.objects.get(id='DEFENDANT')
        defendant_modifier = create_test_modifier(
            unit=defendant_unit, values=[
                dict(limit_from=2, limit_to=None, modifier_percent=Decimal('25.00'))
            ]
        )

        test_price = create_test_price(
            unit=day_unit,
            fixed_fee=Decimal('10.00'),
            fee_per_unit=Decimal('1.00'),
            modifiers=[case_modifier, defendant_modifier],
            limit_from=5,
            limit_to=12
        )

        self.assertEqual(
            test_price.calculate_total(
                12, [(case_modifier, 2), (defendant_modifier, 3)]
            ),
            Decimal('25.20')
        )

    def test_calculate_total_3(self):
        day_unit = Unit.objects.get(id='DAY')
        case_unit = Unit.objects.get(id='CASE')
        case_modifier = create_test_modifier(
            unit=case_unit, values=[
                dict(limit_from=2, limit_to=None, modifier_percent=Decimal('15.00'))
            ]
        )

        test_price = create_test_price(
            unit=day_unit,
            fixed_fee=Decimal('0.00'),
            fee_per_unit=Decimal('1.00'),
            modifiers=[],
            limit_from=0,
            limit_to=None
        )

        self.assertEqual(
            test_price.calculate_total(12, [(case_modifier, 2)]),
            Decimal('12.00')
        )
