# -*- coding: utf-8 -*-
"""
filters
"""
from django.db.models import Q
import django_filters
from django_filters.constants import EMPTY_VALUES
from django_filters.fields import Lookup
import six

from . import models


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
    class Meta:
        model = models.FeeType
        fields = (
            'is_basic',
        )


class PriceFilter(django_filters.FilterSet):
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
        fields = '__all__'
