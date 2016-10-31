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
    fee_types = models.ManyToManyField('FeeType', related_name='scenarios')


class FeeType(models.Model):
    name = models.CharField(max_length=128)
    code = models.CharField(max_length=20)
    is_basic = models.BooleanField()


class AdvocateType(models.Model):
    name = models.CharField(max_length=64)


class OffenceClass(models.Model):
    name = models.CharField(max_length=64)


class Price(models.Model):
    scheme = models.ForeignKey(
        'Scheme', related_name='prices')
    advocate_type = models.ForeignKey(
        'AdvocateType', related_name='prices', null=True)
    offence_class = models.ForeignKey(
        'OffenceClass', related_name='prices', null=True)
    fee_type = models.ForeignKey(
        'FeeType', related_name='prices')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    max_count = models.SmallIntegerField(null=True)
