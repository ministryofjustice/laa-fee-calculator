# -*- coding: utf-8 -*-
from decimal import Decimal

from django.db import models

from .constants import SUPPLIER_BASE_TYPE
from .exceptions import RequiredModifierMissingException


class Scheme(models.Model):
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    suty_base_type = models.PositiveSmallIntegerField(choices=SUPPLIER_BASE_TYPE)
    description = models.CharField(max_length=150)

    def supplier_type(self):
        return SUPPLIER_BASE_TYPE.for_value(self.suty_base_type).constant

    def __str__(self):
        return self.description


class Scenario(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class FeeType(models.Model):
    name = models.CharField(max_length=128)
    code = models.CharField(max_length=20, db_index=True)
    is_basic = models.BooleanField()

    def __str__(self):
        return self.name


class AdvocateType(models.Model):
    id = models.CharField(max_length=12, primary_key=True)
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class OffenceClass(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class Unit(models.Model):
    id = models.CharField(max_length=12, primary_key=True)
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class ModifierType(models.Model):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=150)
    unit = models.ForeignKey(Unit)

    def __str__(self):
        return self.name


def get_value_covered_by_range(value, limit_from, limit_to):
    value_covered = value
    if limit_from:
        if value < limit_from:
            return Decimal('0')
        value_covered -= (limit_from - 1)
    if limit_to and value > limit_to:
        value_covered -= (value - limit_to)
    return max(value_covered, Decimal('0'))


class Modifier(models.Model):
    limit_from = models.IntegerField()
    limit_to = models.IntegerField(null=True)
    fixed_percent = models.DecimalField(max_digits=6, decimal_places=2)
    percent_per_unit = models.DecimalField(max_digits=6, decimal_places=2)
    modifier_type = models.ForeignKey(ModifierType, related_name='values')
    required = models.BooleanField(default=False)
    priority = models.SmallIntegerField(default=0)

    def get_applicable_unit_count(self, unit_count):
        '''
        Get the number of units that fall within the range specified
        by limit_from and limit_to
        '''
        return get_value_covered_by_range(
            unit_count, self.limit_from, self.limit_to
        )

    def is_applicable(self, modifier_type, count):
        if self.modifier_type == modifier_type:
            if self.fixed_percent and self.percent_per_unit:
                return (
                    self.is_applicable_for_fixed_percent(count) and
                    self.is_applicable_for_percent_per_unit(count)
                )
            elif self.fixed_percent:
                return self.is_applicable_for_fixed_percent(count)
            else:
                return self.is_applicable_for_percent_per_unit(count)
        return False

    def is_applicable_for_percent_per_unit(self, count):
        return count >= self.limit_from

    def is_applicable_for_fixed_percent(self, count):
        return (
            count >= self.limit_from and
            (self.limit_to is None or count <= self.limit_to)
        )

    def apply(self, count, total):
        if self.is_applicable_for_fixed_percent(count):
            fixed_modifier = total*self.fixed_percent/Decimal('100.00')
        else:
            fixed_modifier = Decimal('0')

        if self.is_applicable_for_percent_per_unit(count):
            per_unit_modifier = (total*(
                self.percent_per_unit/Decimal('100.00')
            ))*self.get_applicable_unit_count(count)
        else:
            per_unit_modifier = Decimal('0')

        return fixed_modifier + per_unit_modifier

    def __str__(self):
        return '{modifier_type}, {limit_from}-{limit_to}, {percent}%'.format(
            modifier_type=self.modifier_type.name,
            limit_from=self.limit_from,
            limit_to=self.limit_to,
            percent=self.percent_per_unit
        )


class Price(models.Model):
    scenario = models.ForeignKey(
        'Scenario', related_name='prices')
    scheme = models.ForeignKey(
        'Scheme', related_name='prices')
    advocate_type = models.ForeignKey(
        'AdvocateType', related_name='prices', null=True)
    offence_class = models.ForeignKey(
        'OffenceClass', related_name='prices', null=True)
    fee_type = models.ForeignKey(
        'FeeType', related_name='prices')
    unit = models.ForeignKey('Unit', related_name='prices')
    fixed_fee = models.DecimalField(max_digits=10, decimal_places=3)
    fee_per_unit = models.DecimalField(max_digits=10, decimal_places=3)
    limit_from = models.SmallIntegerField(default=1)
    limit_to = models.SmallIntegerField(null=True)
    modifiers = models.ManyToManyField(Modifier, related_name='prices')

    def calculate_total(self, unit_count, modifier_counts):
        '''
        Calculate the total from any fixed_fee, fee_per_unit and modifiers
        '''
        total = self.fixed_fee + (
            self.get_applicable_unit_count(unit_count)*self.fee_per_unit
        )
        try:
            modifiers = self.get_applicable_modifiers(total, modifier_counts)
        except RequiredModifierMissingException:
            return Decimal('0.00')

        fees = []
        current_priority = 0
        for modifier, count in modifiers:
            if modifier.priority != current_priority:
                total += sum(fees)
                fees = []
                current_priority = modifier.priority
            fees.append(modifier.apply(count, total))
        return total + sum(fees)

    def get_applicable_modifiers(self, calculated_price, modifier_counts):
        '''
        Get a list of extra fees from associated modifiers for the given
        modifier and count
        '''
        applicable_modifiers = []
        # applicability is checked in python on the assumption that the
        # query for prices will use:
        # `.prefetch_related('modifiers')`
        for modifier in self.modifiers.all():
            modifier_applicable = False
            for modifier_type, count in modifier_counts:
                modifier_applicable = modifier.is_applicable(modifier_type, count)
                if modifier_applicable:
                    applicable_modifiers.append((modifier, count,))
            if modifier.required and not modifier_applicable:
                raise RequiredModifierMissingException
        return sorted(applicable_modifiers, key=lambda m: m[0].priority)

    def get_applicable_unit_count(self, unit_count):
        '''
        Get the number of units that fall within the range specified
        by limit_from and limit_to
        '''
        return get_value_covered_by_range(
            unit_count, self.limit_from, self.limit_to
        )
