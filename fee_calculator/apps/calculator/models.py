# -*- coding: utf-8 -*-
from decimal import Decimal

from django.db import models
from django.db.models import Q

from .constants import SCHEME_TYPE, AGGREGATION_TYPE
from .exceptions import RequiredModifierMissingException


class Scheme(models.Model):
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    earliest_main_hearing_date = models.DateField(null=True, blank=True)
    base_type = models.PositiveSmallIntegerField(choices=SCHEME_TYPE)
    description = models.CharField(max_length=255)

    def type(self) -> str:
        return SCHEME_TYPE.for_value(self.base_type).constant

    def __str__(self):
        return self.description


class Scenario(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class ScenarioCode(models.Model):
    scenario = models.ForeignKey('Scenario', related_name='codes', on_delete=models.CASCADE)
    scheme_type = models.PositiveSmallIntegerField(choices=SCHEME_TYPE)
    code = models.CharField(max_length=64, db_index=True)

    class Meta:
        unique_together = (('scenario', 'scheme_type',),)

    def __str__(self):
        return self.code


class FeeType(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=64, db_index=True)
    is_basic = models.BooleanField()
    aggregation = models.CharField(
        max_length=20, choices=AGGREGATION_TYPE, default=AGGREGATION_TYPE.SUM,
        help_text=(
            'Specifies how multiple prices for this fee type will be combined.'
        )
    )

    def __str__(self):
        return self.name


class AdvocateType(models.Model):
    id = models.CharField(max_length=32, primary_key=True)
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class OffenceClass(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=1000)

    def __str__(self):
        return self.name


class Unit(models.Model):
    id = models.CharField(max_length=32, primary_key=True)
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class ModifierType(models.Model):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=255)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)

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
    fixed_percent = models.DecimalField(
        max_digits=6, decimal_places=2, help_text=(
            'Adds this percent to the fee if this modifier is applicable.'
        )
    )
    percent_per_unit = models.DecimalField(
        max_digits=6, decimal_places=2, help_text=(
            'Adds this percent to the fee for each unit within the range '
            'covered by `limit_from` and `limit_to` if this modifier is '
            'applicable.'
        )
    )
    modifier_type = models.ForeignKey(ModifierType, related_name='values', on_delete=models.CASCADE)
    required = models.BooleanField(default=False, help_text=(
        'If `True`, prices with this modifier will not be applicable unless '
        'this modifier is applicable.'
    ))
    priority = models.SmallIntegerField(default=0, help_text=(
        'When applying modifiers to to the value of the fee, those with the '
        'lowest value of `priority` will be applied first. A `priority` of 0 '
        'will mean that the modifier will only provide an increase on the '
        'base fee.'
    ))
    strict_range = models.BooleanField(default=False, help_text=(
        'If `True`, this modifier will only be applicable if the unit count '
        'is >= `limit_from` and <= `limit_to`. If `False`, it will apply as '
        'long as the unit count is >= `limit_from`.'
    ))

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
            if self.strict_range:
                return (
                    count >= self.limit_from and
                    (self.limit_to is None or count <= self.limit_to)
                )
            else:
                return count >= self.limit_from
        return False

    def apply(self, count, total):
        fixed_modifier = total*self.fixed_percent/Decimal('100.00')
        per_unit_modifier = (
            total*(self.percent_per_unit/Decimal('100.00'))
        )*self.get_applicable_unit_count(count)
        return fixed_modifier + per_unit_modifier

    def __str__(self):
        return '{modifier_type}, {limit_from}-{limit_to}, {pu}% pu, {fixed}% fixed'.format(
            modifier_type=self.modifier_type.name,
            limit_from=self.limit_from,
            limit_to=self.limit_to,
            pu=self.percent_per_unit,
            fixed=self.fixed_percent
        )


class Price(models.Model):
    scenario = models.ForeignKey('Scenario', related_name='prices', on_delete=models.CASCADE)
    scheme = models.ForeignKey('Scheme', related_name='prices', on_delete=models.CASCADE)
    advocate_type = models.ForeignKey(
        'AdvocateType', related_name='prices', null=True, on_delete=models.CASCADE)
    offence_class = models.ForeignKey(
        'OffenceClass', related_name='prices', null=True, on_delete=models.CASCADE)
    fee_type = models.ForeignKey('FeeType', related_name='prices', on_delete=models.CASCADE)
    unit = models.ForeignKey('Unit', related_name='prices', on_delete=models.CASCADE)
    london_rates_apply = models.BooleanField(null=True)
    fixed_fee = models.DecimalField(
        max_digits=12, decimal_places=5, help_text=(
            'Adds this value to the fee if this price is applicable.'
        )
    )
    fee_per_unit = models.DecimalField(
        max_digits=12, decimal_places=5, help_text=(
            'Adds this value to the fee for each unit within the range '
            'covered by `limit_from` and `limit_to` if this price is '
            'applicable.'
        )
    )
    limit_from = models.SmallIntegerField(default=1)
    limit_to = models.SmallIntegerField(null=True)
    strict_range = models.BooleanField(default=False, help_text=(
        'If `True`, this price will only be applicable if the unit count '
        'is >= `limit_from` and <= `limit_to`. If `False`, it will apply as '
        'long as the unit count is >= `limit_from`.'
    ))
    modifiers = models.ManyToManyField(Modifier, related_name='prices')

    def calculate_total(self, unit_count, modifier_counts):
        '''
        Calculate the total from any fixed_fee, fee_per_unit and modifiers
        '''
        if not self.is_applicable(unit_count):
            return Decimal(0)

        if self.fixed_fee and self.strict_range:
            # first unit is included in fixed fee
            total = self.fixed_fee + (
                (self.get_applicable_unit_count(unit_count) - 1)*self.fee_per_unit
            )
        else:
            total = self.fixed_fee + (
                (self.get_applicable_unit_count(unit_count))*self.fee_per_unit
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

    def is_applicable(self, count):
        if self.strict_range:
            return (
                count >= self.limit_from and
                (self.limit_to is None or count <= self.limit_to)
            )
        else:
            return count >= self.limit_from

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
            modifier_applied = False
            for modifier_type, count in modifier_counts:
                modifier_applicable = modifier.is_applicable(modifier_type, count)
                if modifier_applicable:
                    modifier_applied = True
                    applicable_modifiers.append((modifier, count,))
            if modifier.required and not modifier_applied:
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


def calculate_total(
    scheme, scenario, fee_type, offence_class, advocate_type, unit_counts,
    modifier_counts, london_rates_apply=None
):
    amounts = []
    for unit, unit_count in unit_counts:
        prices = Price.objects.filter(
            Q(advocate_type=advocate_type) | Q(advocate_type__isnull=True),
            Q(offence_class=offence_class) | Q(offence_class__isnull=True),
            scheme=scheme, fee_type=fee_type, unit=unit,
            scenario=scenario, london_rates_apply=london_rates_apply
        ).prefetch_related('modifiers')

        if len(prices) > 0:
            # sum total from all prices whose range is covered by the unit_count
            amounts.append(sum((
                price.calculate_total(unit_count, modifier_counts)
                for price in prices
            )))

    if len(amounts) > 0:
        if fee_type.aggregation == AGGREGATION_TYPE.MAX:
            return max(amounts)
        else:
            return sum(amounts)
    else:
        return Decimal('0')
