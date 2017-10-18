# -*- coding: utf-8 -*-
from decimal import Decimal

from django.test import TestCase


from calculator.models import (
    Scheme, Scenario, OffenceClass, FeeType, AdvocateType, Price, Unit,
    ModifierType, Modifier
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


def create_test_modifiers(
    name='Test modifier', description='Test modifier', unit=None, modifiers=[]
):
    modifier_type = ModifierType.objects.create(
        name=name, description=description, unit=unit
    )
    created_modifiers = []
    for modifier in modifiers:
        created_modifiers.append(Modifier.objects.create(
            modifier_type=modifier_type, **modifier
        ))
    return (modifier_type, created_modifiers)


class PriceTestCase(TestCase):
    fixtures = [
        'advocatetype', 'feetype', 'offenceclass', 'price', 'scenario',
        'scheme', 'unit', 'modifiertype', 'modifier',
    ]

    def assertSortedListEqual(self, list1, list2, msg=None):
        self.assertEqual(sorted(list1), sorted(list2), msg)

    def test_get_applicable_unit_count_with_limit_from(self):
        test_price = create_test_price(limit_from=5, limit_to=None)

        self.assertEqual(test_price.get_applicable_unit_count(4), 0)
        self.assertEqual(test_price.get_applicable_unit_count(5), 1)
        self.assertEqual(test_price.get_applicable_unit_count(8), 4)
        self.assertEqual(test_price.get_applicable_unit_count(12), 8)
        self.assertEqual(test_price.get_applicable_unit_count(15), 11)

    def test_get_applicable_unit_count_with_non_integers(self):
        test_price = create_test_price(limit_from=1, limit_to=30)

        self.assertEqual(test_price.get_applicable_unit_count(Decimal('0.5')), 0)
        self.assertEqual(test_price.get_applicable_unit_count(1), 1)
        self.assertEqual(test_price.get_applicable_unit_count(Decimal('4.5')), 4.5)

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

    def test_get_modifiers_with_single_qualifying(self):
        case_unit = Unit.objects.get(id='CASE')
        modifier_type, modifiers = create_test_modifiers(
            unit=case_unit, modifiers=[
                dict(limit_from=2, limit_to=None, percent_per_unit=Decimal('15.00'),
                     fixed_percent=Decimal('0.00'))
            ]
        )

        test_price = create_test_price(modifiers=modifiers)

        self.assertEqual(
            test_price.get_applicable_modifiers(Decimal('10.00'), [(modifier_type, 2,)]),
            [(modifiers[0], 2)]
        )

    def test_get_modifiers_with_multiple_qualifying(self):
        case_unit = Unit.objects.get(id='CASE')
        case_modifier_type, case_modifiers = create_test_modifiers(
            unit=case_unit, modifiers=[
                dict(limit_from=2, limit_to=None, percent_per_unit=Decimal('15.00'),
                     fixed_percent=Decimal('0.00'))
            ]
        )
        defendant_unit = Unit.objects.get(id='DEFENDANT')
        defendant_modifier_type, defendant_modifiers = create_test_modifiers(
            unit=defendant_unit, modifiers=[
                dict(limit_from=2, limit_to=None, percent_per_unit=Decimal('25.00'),
                     fixed_percent=Decimal('0.00'))
            ]
        )

        test_price = create_test_price(
            modifiers=case_modifiers + defendant_modifiers
        )

        self.assertSortedListEqual(
            test_price.get_applicable_modifiers(Decimal('10.00'), [(case_modifier_type, 2,)]),
            [(case_modifiers[0], 2)]
        )
        self.assertSortedListEqual(
            test_price.get_applicable_modifiers(Decimal('10.00'), [(defendant_modifier_type, 2,)]),
            [(defendant_modifiers[0], 2)]
        )

    def test_get_modifiers_with_some_not_qualifying(self):
        case_unit = Unit.objects.get(id='CASE')
        case_modifier_type, case_modifiers = create_test_modifiers(
            unit=case_unit, modifiers=[
                dict(limit_from=2, limit_to=None, percent_per_unit=Decimal('15.00'),
                     fixed_percent=Decimal('0.00')),
                dict(limit_from=1, limit_to=1, percent_per_unit=Decimal('25.00'),
                     fixed_percent=Decimal('0.00'))
            ]
        )

        test_price = create_test_price(
            modifiers=case_modifiers
        )

        self.assertSortedListEqual(
            test_price.get_applicable_modifiers(Decimal('10.00'), [(case_modifier_type, 1,)]),
            [(case_modifiers[1], 1)]
        )

    def test_calculate_total_1(self):
        day_unit = Unit.objects.get(id='DAY')
        case_unit = Unit.objects.get(id='CASE')
        case_modifier_type, case_modifiers = create_test_modifiers(
            unit=case_unit, modifiers=[
                dict(limit_from=2, limit_to=None, percent_per_unit=Decimal('15.00'),
                     fixed_percent=Decimal('0.00'))
            ]
        )

        test_price = create_test_price(
            unit=day_unit,
            fixed_fee=Decimal('10.00'),
            fee_per_unit=Decimal('1.00'),
            modifiers=case_modifiers,
            limit_from=5,
            limit_to=12
        )

        self.assertEqual(
            test_price.calculate_total(12, [(case_modifier_type, 2)]),
            Decimal('20.70')
        )

    def test_calculate_total_2(self):
        day_unit = Unit.objects.get(id='DAY')
        case_unit = Unit.objects.get(id='CASE')
        case_modifier_type, case_modifiers = create_test_modifiers(
            unit=case_unit, modifiers=[
                dict(limit_from=2, limit_to=None, percent_per_unit=Decimal('15.00'),
                     fixed_percent=Decimal('0.00'))
            ]
        )
        defendant_unit = Unit.objects.get(id='DEFENDANT')
        defendant_modifier_type, defendant_modifiers = create_test_modifiers(
            unit=defendant_unit, modifiers=[
                dict(limit_from=2, limit_to=None, percent_per_unit=Decimal('25.00'),
                     fixed_percent=Decimal('0.00'))
            ]
        )

        test_price = create_test_price(
            unit=day_unit,
            fixed_fee=Decimal('10.00'),
            fee_per_unit=Decimal('1.00'),
            modifiers=case_modifiers + defendant_modifiers,
            limit_from=5,
            limit_to=12
        )

        self.assertEqual(
            test_price.calculate_total(
                12, [(case_modifier_type, 2), (defendant_modifier_type, 3)]
            ),
            Decimal('29.70')
        )

    def test_calculate_total_3(self):
        day_unit = Unit.objects.get(id='DAY')
        case_unit = Unit.objects.get(id='CASE')
        case_modifier_type, case_modifiers = create_test_modifiers(
            unit=case_unit, modifiers=[
                dict(limit_from=2, limit_to=None, percent_per_unit=Decimal('15.00'),
                     fixed_percent=Decimal('0.00'))
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
            test_price.calculate_total(12, [(case_modifier_type, 2)]),
            Decimal('12.00')
        )

    def test_calculate_total_with_required_modifier_missing(self):
        day_unit = Unit.objects.get(id='DAY')
        trial_length_modifier_type, trial_length_modifiers = create_test_modifiers(
            unit=day_unit, modifiers=[
                dict(
                    limit_from=2, limit_to=None, required=True,
                    percent_per_unit=Decimal('0.00'), fixed_percent=Decimal('0.00')
                )
            ]
        )

        test_price = create_test_price(
            unit=day_unit,
            fixed_fee=Decimal('0.00'),
            fee_per_unit=Decimal('1.00'),
            modifiers=trial_length_modifiers,
            limit_from=1,
            limit_to=None
        )

        self.assertEqual(
            test_price.calculate_total(12, []),
            Decimal('0.00')
        )

    def test_calculate_total_with_required_modifier_not_met(self):
        day_unit = Unit.objects.get(id='DAY')
        trial_length_modifier_type, trial_length_modifiers = create_test_modifiers(
            unit=day_unit, modifiers=[
                dict(
                    limit_from=2, limit_to=None, required=True,
                    percent_per_unit=Decimal('0.00'), fixed_percent=Decimal('0.00')
                )
            ]
        )

        test_price = create_test_price(
            unit=day_unit,
            fixed_fee=Decimal('0.00'),
            fee_per_unit=Decimal('1.00'),
            modifiers=trial_length_modifiers,
            limit_from=1,
            limit_to=None
        )

        self.assertEqual(
            test_price.calculate_total(12, [(trial_length_modifier_type, 1,)]),
            Decimal('0.00')
        )

    def test_calculate_total_with_required_modifier_met(self):
        day_unit = Unit.objects.get(id='DAY')
        trial_length_modifier_type, trial_length_modifiers = create_test_modifiers(
            unit=day_unit, modifiers=[
                dict(
                    limit_from=2, limit_to=None, required=True,
                    percent_per_unit=Decimal('0.00'), fixed_percent=Decimal('0.00')
                )
            ]
        )

        test_price = create_test_price(
            unit=day_unit,
            fixed_fee=Decimal('0.00'),
            fee_per_unit=Decimal('1.00'),
            modifiers=trial_length_modifiers,
            limit_from=1,
            limit_to=None
        )

        self.assertEqual(
            test_price.calculate_total(12, [(trial_length_modifier_type, 2,)]),
            Decimal('12.00')
        )

    def test_calculate_total_with_fixed_modifier(self):
        day_unit = Unit.objects.get(id='DAY')
        trial_length_modifier_type, trial_length_modifiers = create_test_modifiers(
            unit=day_unit, modifiers=[
                dict(
                    limit_from=1, limit_to=None, percent_per_unit=Decimal('0.00'),
                    fixed_percent=Decimal('20.00')
                )
            ]
        )

        test_price = create_test_price(
            unit=day_unit,
            fixed_fee=Decimal('0.00'),
            fee_per_unit=Decimal('1.00'),
            modifiers=trial_length_modifiers,
            limit_from=1,
            limit_to=None
        )

        self.assertEqual(
            test_price.calculate_total(12, [(trial_length_modifier_type, 5,)]),
            Decimal('14.40')
        )

    def test_calculate_total_with_fixed_modifier_not_applied_outside_range(self):
        day_unit = Unit.objects.get(id='DAY')
        trial_length_modifier_type, trial_length_modifiers = create_test_modifiers(
            unit=day_unit, modifiers=[
                dict(
                    limit_from=1, limit_to=3, percent_per_unit=Decimal('0.00'),
                    fixed_percent=Decimal('20.00')
                )
            ]
        )

        test_price = create_test_price(
            unit=day_unit,
            fixed_fee=Decimal('0.00'),
            fee_per_unit=Decimal('1.00'),
            modifiers=trial_length_modifiers,
            limit_from=1,
            limit_to=None
        )

        self.assertEqual(
            test_price.calculate_total(12, [(trial_length_modifier_type, 5,)]),
            Decimal('12.00')
        )

    def test_calculate_total_priorities_observed(self):
        day_unit = Unit.objects.get(id='DAY')
        trial_length_modifier_type, trial_length_modifiers = create_test_modifiers(
            unit=day_unit, modifiers=[
                dict(
                    limit_from=1, limit_to=None, percent_per_unit=Decimal('0.00'),
                    fixed_percent=Decimal('20.00'), priority=0
                )
            ]
        )
        case_unit = Unit.objects.get(id='CASE')
        case_modifier_type, case_modifiers = create_test_modifiers(
            unit=case_unit, modifiers=[
                dict(
                    limit_from=2, limit_to=None, percent_per_unit=Decimal('15.00'),
                    fixed_percent=Decimal('0.00'), priority=1
                )
            ]
        )

        test_price = create_test_price(
            unit=day_unit,
            fixed_fee=Decimal('0.00'),
            fee_per_unit=Decimal('1.00'),
            modifiers=trial_length_modifiers + case_modifiers,
            limit_from=1,
            limit_to=None
        )

        self.assertEqual(
            test_price.calculate_total(
                12, [(trial_length_modifier_type, 5,), (case_modifier_type, 3,)]
            ),
            Decimal('18.72')
        )
