# -*- coding: utf-8 -*-
from datetime import datetime
from decimal import Decimal, InvalidOperation
import logging

from django.db.models import Q
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import backends
from rest_framework import viewsets, views
from rest_framework.compat import coreapi
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.schemas import AutoSchema

from .constants import SUPPLIER_BASE_TYPE
from .filters import (
    PriceFilter, FeeTypeFilter, CalculatorSchema
)
from .models import (
    Scheme, FeeType, Scenario, OffenceClass, AdvocateType, Price, Unit,
    ModifierType, calculate_total
)
from .serializers import (
    SchemeSerializer, FeeTypeSerializer, ScenarioSerializer,
    OffenceClassSerializer, AdvocateTypeSerializer, PriceSerializer,
    UnitSerializer, ModifierTypeSerializer
)

logger = logging.getLogger('laa-calc')


class OrderedReadOnlyModelViewSet(viewsets.ReadOnlyModelViewSet):
    default_ordering = None

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        queryset = queryset.order_by(self.default_ordering or 'pk')
        return queryset


class SchemeViewSet(OrderedReadOnlyModelViewSet):
    """
    Viewing fee scheme(s).
    """
    schema = AutoSchema(manual_fields=[
        coreapi.Field('supplier_type', **{
            'required': False,
            'location': 'query',
            'type': 'string',
            'description': '',
        }),
        coreapi.Field('case_date', **{
            'required': False,
            'location': 'query',
            'type': 'string',
            'description': '',
        }),
    ])
    queryset = Scheme.objects.all()
    serializer_class = SchemeSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        supplier_type = self.request.query_params.get('supplier_type')
        case_date = self.request.query_params.get('case_date')

        if case_date:
            try:
                case_date = datetime.strptime(case_date, '%Y-%m-%d')
            except ValueError:
                raise ValidationError(
                    '`case_date` should be in the format YYYY-MM-DD'
                )
            queryset = queryset.filter(
                Q(end_date__isnull=True) | Q(end_date__gte=case_date),
                start_date__lte=case_date
            )

        if supplier_type:
            try:
                supplier_type = SUPPLIER_BASE_TYPE.for_constant(supplier_type.upper()).value
            except KeyError:
                raise ValidationError(
                    '`supplier_type` should be one of: [%s]'
                    % ', '.join(SUPPLIER_BASE_TYPE.constants)
                )
            queryset = queryset.filter(suty_base_type=supplier_type)

        return queryset


class NestedSchemeMixin():
    scheme_relation_name = 'prices__scheme'

    def get_scheme_queryset(self, scheme_pk):
        scheme = get_object_or_404(Scheme, pk=scheme_pk)
        queryset = self.get_queryset().filter(
            **{'{relation}'.format(relation=self.scheme_relation_name): scheme}
        ).distinct()
        return self.filter_queryset(queryset)

    def list(self, request, scheme_pk=None):
        queryset = self.get_scheme_queryset(scheme_pk)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, scheme_pk=None, pk=None):
        queryset = self.get_scheme_queryset(scheme_pk)
        obj = get_object_or_404(queryset, pk=pk)

        self.check_object_permissions(self.request, obj)

        serializer = self.get_serializer(obj)
        return Response(serializer.data)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['scheme_pk'] = self.kwargs.get('scheme_pk')
        return context


class BasePriceFilteredViewSet(NestedSchemeMixin, OrderedReadOnlyModelViewSet):
    schema = AutoSchema(manual_fields=[
        coreapi.Field('scenario', **{
            'required': False,
            'location': 'query',
            'type': 'integer',
            'description': '',
        }),
        coreapi.Field('advocate_type', **{
            'required': False,
            'location': 'query',
            'type': 'string',
            'description': (
                'Note the query will return prices with `advocate_type_id` '
                'either matching the value or null.'),
        }),
        coreapi.Field('offence_class', **{
            'required': False,
            'location': 'query',
            'type': 'string',
            'description': (
                'Note the query will return prices with `offence_class_id` '
                'either matching the value or null.'),
        }),
        coreapi.Field('fee_type_code', **{
            'required': False,
            'location': 'query',
            'type': 'string',
            'description': '',
        }),
    ])
    relation_name = NotImplemented
    lookup_attr = 'pk'

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)

        scenario_id = self.request.query_params.get('scenario')
        advocate_type_id = self.request.query_params.get('advocate_type')
        offence_class_id = self.request.query_params.get('offence_class')
        fee_type_code = self.request.query_params.get('fee_type_code')

        filters = []
        if scenario_id:
            filters.append(Q(scenario_id=scenario_id))
        if advocate_type_id:
            filters.append(
                Q(advocate_type_id=advocate_type_id) |
                Q(advocate_type_id__isnull=True)
            )
        if offence_class_id:
            filters.append(
                Q(offence_class_id=offence_class_id) |
                Q(offence_class_id__isnull=True)
            )
        if fee_type_code:
            filters.append(
                Q(fee_type__code=fee_type_code)
            )

        if filters:
            filters.append(Q(scheme_id=self.kwargs['scheme_pk']))
            applicable_prices = Price.objects.filter(*filters)
            relevant_values = applicable_prices.values_list(
                self.relation_name, flat=True
            ).distinct()
            queryset = queryset.filter(
                **{'{lookup_attr}__in'.format(
                    lookup_attr=self.lookup_attr
                ): relevant_values}
            )
        return queryset


class FeeTypeViewSet(BasePriceFilteredViewSet):
    """
    Viewing fee type(s).
    """
    queryset = FeeType.objects.all()
    serializer_class = FeeTypeSerializer
    filter_backends = (backends.DjangoFilterBackend,)
    filter_class = FeeTypeFilter
    relation_name = 'fee_type'


class UnitViewSet(BasePriceFilteredViewSet):
    """
    Viewing unit(s).
    """
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer
    relation_name = 'unit'


class ModifierTypeViewSet(BasePriceFilteredViewSet):
    """
    Viewing modifier type(s).
    """
    queryset = ModifierType.objects.all()
    serializer_class = ModifierTypeSerializer
    relation_name = 'modifiers'
    lookup_attr = 'values__pk'
    scheme_relation_name = 'values__prices__scheme'


class ScenarioViewSet(NestedSchemeMixin, OrderedReadOnlyModelViewSet):
    """
    Viewing scenario(s).
    """
    queryset = Scenario.objects.all()
    serializer_class = ScenarioSerializer


class OffenceClassViewSet(NestedSchemeMixin, OrderedReadOnlyModelViewSet):
    """
    Viewing offence class(es).
    """
    queryset = OffenceClass.objects.all()
    serializer_class = OffenceClassSerializer


class AdvocateTypeViewSet(NestedSchemeMixin, OrderedReadOnlyModelViewSet):
    """
    Viewing advocate type(s).
    """
    queryset = AdvocateType.objects.all()
    serializer_class = AdvocateTypeSerializer


class PriceViewSet(NestedSchemeMixin, OrderedReadOnlyModelViewSet):
    """
    Viewing price(s).
    """
    queryset = Price.objects.all()
    serializer_class = PriceSerializer
    filter_backends = (backends.DjangoFilterBackend,)
    filter_class = PriceFilter
    scheme_relation_name = 'scheme'


class cached_class_property:
    def __init__(self, getter):
        self.getter = getter
        self.cached = None

    def __get__(self, instance, clazz):
        if self.cached is None:
            self.cached = self.getter(clazz)
        return self.cached


class CalculatorView(views.APIView):
    """
    Calculate total fee amount
    """

    allowed_methods = ['GET']
    filter_backends = (backends.DjangoFilterBackend,)

    @cached_class_property
    def schema(cls):
        return CalculatorSchema(fields=[
            coreapi.Field('scheme_pk', **{
                'required': True,
                'location': 'path',
                'type': 'integer',
                'description': '',
            }),
            coreapi.Field('fee_type_code', **{
                'required': True,
                'location': 'query',
                'type': 'string',
                'description': '',
            }),
            coreapi.Field('scenario', **{
                'required': True,
                'location': 'query',
                'type': 'integer',
                'description': '',
            }),
            coreapi.Field('advocate_type', **{
                'required': False,
                'location': 'query',
                'type': 'string',
                'description': (
                    'Note the query will return prices with `advocate_type_id` '
                    'either matching the value or null.'),
            }),
            coreapi.Field('offence_class', **{
                'required': False,
                'location': 'query',
                'type': 'string',
                'description': (
                    'Note the query will return prices with `offence_class_id` '
                    'either matching the value or null.'),
            })
        ])

    def get_param(self, param_name, required=False, default=None):
        value = self.request.query_params.get(param_name, default)
        if value is None:
            if required:
                raise ValidationError('`%s` is a required field' % param_name)
        return value

    def get_model_param(
        self, param_name, model_class, required=False, lookup='pk', many=False,
        default=None
    ):
        instance = self.get_param(param_name, required, default)
        try:
            if instance is not None:
                if many:
                    instance = model_class.objects.filter(**{lookup: instance})
                else:
                    instance = model_class.objects.get(**{lookup: instance})
        except model_class.DoesNotExist:
            raise ValidationError(
                '`%s` is not a valid %s' % (instance, model_class.__name__)
            )
        return instance

    def get_decimal_param(self, param_name, required=False, default=None):
        number = self.get_param(param_name, required, default)
        try:
            if number is not None:
                number = Decimal(number)
        except InvalidOperation:
            raise ValidationError('`%s` must be a number' % param_name)
        return number

    def get(self, *args, **kwargs):
        scheme = get_object_or_404(Scheme, pk=kwargs['scheme_pk'])
        fee_types = self.get_model_param(
            'fee_type_code', FeeType, required=True, lookup='code', many=True
        )
        scenario = self.get_model_param('scenario', Scenario, required=True)
        advocate_type = self.get_model_param('advocate_type', AdvocateType)
        offence_class = self.get_model_param('offence_class', OffenceClass)

        units = Unit.objects.values_list('pk', flat=True)
        modifiers = ModifierType.objects.values_list('name', flat=True)
        unit_counts = []
        modifier_counts = []
        for param in self.request.query_params:
            if param.upper() in units:
                unit_counts.append((
                    Unit.objects.get(pk=param.upper()),
                    self.get_decimal_param(param),
                ))

            if param.upper() in modifiers:
                modifier_counts.append((
                    ModifierType.objects.get(name=param.upper()),
                    self.get_decimal_param(param),
                ))

        matching_fee_types = Price.objects.filter(
            scheme=scheme, fee_type__in=fee_types
        ).values_list('fee_type', flat=True).distinct()

        if len(matching_fee_types) != 1:
            raise ValidationError((
                'fee_type_code must match a unique fee type for the scheme; '
                '{} were found'
            ).format(len(matching_fee_types)))

        unique_fee_type = FeeType.objects.get(pk=matching_fee_types[0])

        amount = calculate_total(
            scheme, scenario, unique_fee_type, offence_class, advocate_type,
            unit_counts, modifier_counts
        )

        return Response({
            'amount': amount.quantize(Decimal('0.01'))
        })
