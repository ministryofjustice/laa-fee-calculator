# -*- coding: utf-8 -*-
from django.db import models

from .constants import SUTY_BASE_TYPE


class Scheme(models.Model):
    effective_date = models.DateField()
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    suty_base_type = models.PositiveSmallIntegerField(choices=SUTY_BASE_TYPE)
    description = models.CharField(max_length=150)


class Scenario(models.Model):
    name = models.CharField(max_length=64)


class FeeType(models.Model):
    name = models.CharField(max_length=128)
    code = models.CharField(max_length=20)
    is_basic = models.BooleanField()


class AdvocateType(models.Model):
    id = models.CharField(max_length=12, primary_key=True)
    name = models.CharField(max_length=64)


class OffenceClass(models.Model):
    name = models.CharField(max_length=64, primary_key=True)
    description = models.CharField(max_length=150)


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
    fee_per_unit = models.DecimalField(max_digits=10, decimal_places=3)
    limit_from = models.SmallIntegerField(default=1)
    limit_to = models.SmallIntegerField(null=True)
