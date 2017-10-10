# -*- coding: utf-8 -*-
from decimal import Decimal

from django.db import models

from .constants import SUTY_BASE_TYPE


class Scheme(models.Model):
    effective_date = models.DateField()
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    suty_base_type = models.PositiveSmallIntegerField(choices=SUTY_BASE_TYPE)
    description = models.CharField(max_length=150)

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

    def units(self):
        return self.prices.values_list('unit').distinct()

    def uplift_units(self):
        return self.prices.values_list(
            'uplifts__unit').distinct().exclude(uplifts__unit__isnull=True)

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


class Uplift(models.Model):
    unit = models.ForeignKey(Unit)
    limit_from = models.IntegerField()
    limit_to = models.IntegerField(null=True)
    uplift_percent = models.DecimalField(max_digits=6, decimal_places=2)

    def is_applicable(self, unit_id, count):
        return (
            unit_id == self.unit and
            count >= self.limit_from and
            (self.limit_to is None or count <= self.limit_to)
        )

    def apply(self, total):
        return total*(self.uplift_percent/Decimal('100.00'))


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
    uplifts = models.ManyToManyField(Uplift)

    def calculate_total(self, unit_count, uplift_unit_counts):
        '''
        Calculate the total from any fixed_fee, fee_per_unit and uplifts
        '''
        total = self.fixed_fee + (
            self.get_applicable_unit_count(unit_count)*self.fee_per_unit
        )
        uplift_fees = []
        for uplift_unit, count in uplift_unit_counts:
            uplift_fees += self.get_uplift_fees(total, uplift_unit, count)
        return total + sum(uplift_fees)

    def get_uplift_fees(self, calculated_price, uplift_unit, count):
        '''
        Get a list of extra fees from associated uplifts for the given
        uplift_unit and count
        '''
        uplift_fees = []
        # applicability is checked in python on the assumption that the
        # query for prices will use `.prefetch_related('uplifts')`
        for uplift in self.uplifts.all():
            if uplift.is_applicable(uplift_unit, count):
                uplift_fees.append(uplift.apply(calculated_price))
        return uplift_fees

    def get_applicable_unit_count(self, unit_count):
        '''
        Get the number of units that fall within the range specified
        by limit_from and limit_to
        '''
        applicable_unit_count = unit_count
        if self.limit_from:
            applicable_unit_count -= (self.limit_from - 1)
        if self.limit_to and unit_count >= self.limit_to:
            applicable_unit_count -= (unit_count - self.limit_to)
        return max(applicable_unit_count, 0)
