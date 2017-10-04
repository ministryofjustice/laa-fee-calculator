# -*- coding: utf-8 -*-
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
    uplift_percent = models.DecimalField(max_digits=6, decimal_places=2)
    limit_from = models.SmallIntegerField(default=1)
    limit_to = models.SmallIntegerField(null=True)
