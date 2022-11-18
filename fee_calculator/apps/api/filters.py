# -*- coding: utf-8 -*-
import logging

from django.db.models import Q
import django_filters
from django_filters.constants import EMPTY_VALUES
from django_filters.fields import Lookup
from django_filters.rest_framework import filters
import six

from calculator import models as calc_models
from calculator.constants import SCHEME_TYPE

logger = logging.getLogger('laa-calc')


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
            Q(**{'%s__isnull' % self.field_name: True}) |
            Q(**{'%s__%s' % (self.field_name, lookup): value})
        )
        return qs


class FeeTypeFilter(django_filters.FilterSet):
    is_basic = filters.BooleanFilter()

    class Meta:
        model = calc_models.FeeType
        fields = (
            'is_basic',
        )


class PriceFilter(django_filters.FilterSet):
    fee_type_code = django_filters.CharFilter(
        field_name='fee_type__code',
    )
    offence_class = ModelOrNoneChoiceFilter(
        field_name='offence_class',
        queryset=calc_models.OffenceClass.objects.all(),
        help_text=(
            'Note the query will return prices '
            'with `offence_class` either matching the value or null.'
        )
    )
    advocate_type = ModelOrNoneChoiceFilter(
        field_name='advocate_type',
        queryset=calc_models.AdvocateType.objects.all(),
        help_text=(
            'Note the query will return prices '
            'with `advocate_type` either matching the value or null.'
        )
    )

    class Meta:
        model = calc_models.Price
        fields = {
            'scenario': ['exact'],
            'unit': ['exact'],
            'limit_from': ['exact', 'gte'],
            'limit_to': ['exact', 'lte'],
            'fixed_fee': ['lte', 'gte'],
            'fee_per_unit': ['lte', 'gte'],
        }


class SchemeFilter(django_filters.FilterSet):
    type = django_filters.ChoiceFilter(
        field_name='base_type',
        choices=tuple(map(lambda st: (st[0], st[1].value), SCHEME_TYPE.constants.items())),
        method='type_filter'
    )
    case_date = django_filters.DateFilter(method='case_date_filter')

    def type_filter(self, queryset, name, value):
        type_code = SCHEME_TYPE.for_constant(value.upper()).value

        return queryset.filter(**{name: type_code})

    def case_date_filter(self, queryset, name, value):
        return queryset.filter(
            Q(end_date__isnull=True) | Q(end_date__gte=value),
            start_date__lte=value,
            earliest_main_hearing_date=None
        )
