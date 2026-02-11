# -*- coding: utf-8 -*-
import logging

from django.db.models import Q
import django_filters
from django_filters.constants import EMPTY_VALUES
from django_filters.fields import Lookup
from django_filters.rest_framework import filters
from django.conf import settings
import six

from calculator import models as calc_models
from calculator.constants import SchemeType
from calculator.models import AdvocateType

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
    london_rates_apply = django_filters.BooleanFilter(
        field_name='london_rates_apply',
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
        method='field_filter',
        help_text=(
            'Note the query will return prices '
            'with `advocate_type` either matching the value or null.'
        )
    )

    def field_filter(self, queryset, name, value):
        return queryset.filter(**self.clean_param(self.request, name, value))

    def clean_param(self, request, name, value):
        if name == 'advocate_type' and value.pk in ['QC', 'KC']:
            pk = 'KC' if request.fee_scheme.start_date >= settings.QC_KC_CHANGE_DATE else 'QC'
            value = AdvocateType.objects.get(pk=pk)

        return {name: value}

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
        choices=[(m.name, m.label) for m in SchemeType],
        method='type_filter'
    )
    case_date = django_filters.DateFilter(method='case_date_filter')
    main_hearing_date = django_filters.DateFilter(method='main_hearing_date_filter')

    def type_filter(self, queryset, name, value):
        type_code = SchemeType[value.upper()].value

        return queryset.filter(**{name: type_code})

    def case_date_filter(self, queryset, name, value):
        new_queryset = queryset.filter(
            Q(end_date__isnull=True) | Q(end_date__gte=value),
            start_date__lte=value
        )

        if self.form.cleaned_data['main_hearing_date'] is None:
            return new_queryset.filter(earliest_main_hearing_date=None)
        else:
            return new_queryset

    def main_hearing_date_filter(self, queryset, name, value):
        if self.form.cleaned_data['case_date'] is None:
            return queryset

        new_queryset = queryset.filter(earliest_main_hearing_date__lte=value)

        if len(new_queryset) == 0:
            return queryset.filter(earliest_main_hearing_date=None)
        else:
            return new_queryset
