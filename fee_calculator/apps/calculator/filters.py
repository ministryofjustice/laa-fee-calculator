# -*- coding: utf-8 -*-
import logging

from django.db.models import Q
import django_filters
from django_filters.constants import EMPTY_VALUES
from django_filters.fields import Lookup
from django_filters.rest_framework import filters
from rest_framework.compat import coreapi
from rest_framework.schemas import ManualSchema
import six

from . import models

logger = logging.getLogger('laa-calc')


class CalculatorSchema(ManualSchema):

    def __init__(self, fields, *args, **kwargs):
        for unit in models.Unit.objects.all():
            fields.append(
                coreapi.Field(unit.pk.lower(), **{
                    'required': False,
                    'location': 'query',
                    'type': 'number',
                    'description': (
                        'The number of units of the named unit'
                    ),
                }),
            )

        for modifier in models.ModifierType.objects.all():
            fields.append(
                coreapi.Field(modifier.name.lower(), **{
                    'required': False,
                    'location': 'query',
                    'type': 'number',
                    'description': (
                        'The number of units of the named modifier type'
                    ),
                }),
            )
        super().__init__(fields, *args, **kwargs)


class ModelOrNoneChoiceFilter(django_filters.ModelChoiceFilter):

    def filter(self, qs, value):
        if isinstance(value, Lookup):
            lookup = six.text_type(value.lookup_type)
            value = value.value
        else:
            lookup = self.lookup_expr
        if value in EMPTY_VALUES:
            return qs
        if self.distinct:
            qs = qs.distinct()
        qs = self.get_method(qs)(
            Q(**{'%s__isnull' % self.name: True}) |
            Q(**{'%s__%s' % (self.name, lookup): value})
        )
        return qs


class FeeTypeFilter(django_filters.FilterSet):
    is_basic = filters.BooleanFilter()

    class Meta:
        model = models.FeeType
        fields = (
            'is_basic',
        )


class PriceFilter(django_filters.FilterSet):
    fee_type_code = django_filters.CharFilter(
        name='fee_type__code',
    )
    offence_class = ModelOrNoneChoiceFilter(
        name='offence_class',
        queryset=models.OffenceClass.objects.all(),
        help_text=(
            'Note the query will return prices '
            'with `offence_class` either matching the value or null.'
        )
    )
    advocate_type = ModelOrNoneChoiceFilter(
        name='advocate_type',
        queryset=models.AdvocateType.objects.all(),
        help_text=(
            'Note the query will return prices '
            'with `advocate_type` either matching the value or null.'
        )
    )

    class Meta:
        model = models.Price
        fields = {
            'scenario': ['exact'],
            'unit': ['exact'],
            'limit_from': ['exact', 'gte'],
            'limit_to': ['exact', 'lte'],
            'fixed_fee': ['lte', 'gte'],
            'fee_per_unit': ['lte', 'gte'],
        }
