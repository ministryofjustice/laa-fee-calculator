# -*- coding: utf-8 -*-
from datetime import datetime
from decimal import Decimal, InvalidOperation
import logging
import re

from django.db.models import Q
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import backends
from rest_framework import viewsets, views
from rest_framework.compat import coreapi
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.schemas import AutoSchema, ManualSchema

from .constants import SUPPLIER_BASE_TYPE
from .filters import (
    PriceFilter, OffenceClassFilter, AdvocateTypeFilter, ScenarioFilter,
    FeeTypeFilter
)
from .models import (
    Scheme, FeeType, Scenario, OffenceClass, AdvocateType, Price, Unit,
    ModifierType
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
        queryset = queryset.order_by(self.default_ordering or 'pk')
        return super().filter_queryset(queryset)


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
    scheme_relation_name = 'prices'

    def get_scheme_queryset(self, scheme_pk):
        scheme = get_object_or_404(Scheme, pk=scheme_pk)
        queryset = self.get_queryset().filter(
            **{'{relation}__scheme'.format(relation=self.scheme_relation_name): scheme}
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


class BasePriceFilteredViewSet(OrderedReadOnlyModelViewSet):
    schema = AutoSchema(manual_fields=[
        coreapi.Field('scheme', **{
            'required': False,
            'location': 'query',
            'type': 'integer',
            'description': '',
        }),
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
    filter_backends = (backends.DjangoFilterBackend,)
    relation_name = 'prices'

    def get_queryset(self):
        queryset = super().get_queryset()

        scheme_id = self.request.query_params.get('scheme')
        scenario_id = self.request.query_params.get('scenario')
        advocate_type_id = self.request.query_params.get('advocate_type')
        offence_class_id = self.request.query_params.get('offence_class')
        fee_type_code = self.request.query_params.get('fee_type_code')

        filters = []
        if scheme_id:
            filters.append(Q(**{'{lookup}__scheme_id'.format(lookup=self.relation_name): scheme_id}))
        if scenario_id:
            filters.append(Q(**{'{lookup}__scenario_id'.format(lookup=self.relation_name): scenario_id}))
        if advocate_type_id:
            filters.append(
                Q(**{'{lookup}__advocate_type_id'.format(lookup=self.relation_name): advocate_type_id}) |
                Q(**{'{lookup}__advocate_type_id__isnull'.format(lookup=self.relation_name): True})
            )
        if offence_class_id:
            filters.append(
                Q(**{'{lookup}__offence_class_id'.format(lookup=self.relation_name): offence_class_id}) |
                Q(**{'{lookup}__offence_class_id__isnull'.format(lookup=self.relation_name): True})
            )
        if fee_type_code:
            filters.append(
                Q(**{'{lookup}__fee_type__code'.format(lookup=self.relation_name): fee_type_code})
            )

        if filters:
            queryset = queryset.filter(*filters).distinct()
        return queryset


class FeeTypeViewSet(NestedSchemeMixin, BasePriceFilteredViewSet):
    """
    Viewing fee type(s).
    """
    queryset = FeeType.objects.all()
    serializer_class = FeeTypeSerializer
    filter_class = FeeTypeFilter


class ScenarioViewSet(NestedSchemeMixin, OrderedReadOnlyModelViewSet):
    """
    Viewing scenario(s).
    """
    queryset = Scenario.objects.all()
    serializer_class = ScenarioSerializer
    filter_backends = (backends.DjangoFilterBackend,)
    filter_class = ScenarioFilter


class OffenceClassViewSet(NestedSchemeMixin, OrderedReadOnlyModelViewSet):
    """
    Viewing offence class(es).
    """
    queryset = OffenceClass.objects.all()
    serializer_class = OffenceClassSerializer
    filter_backends = (backends.DjangoFilterBackend,)
    filter_class = OffenceClassFilter


class AdvocateTypeViewSet(NestedSchemeMixin, OrderedReadOnlyModelViewSet):
    """
    Viewing advocate type(s).
    """
    queryset = AdvocateType.objects.all()
    serializer_class = AdvocateTypeSerializer
    filter_backends = (backends.DjangoFilterBackend,)
    filter_class = AdvocateTypeFilter


class UnitViewSet(NestedSchemeMixin, BasePriceFilteredViewSet):
    """
    Viewing unit(s).
    """
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer


class ModifierTypeViewSet(NestedSchemeMixin, BasePriceFilteredViewSet):
    """
    Viewing modifier type(s).
    """
    queryset = ModifierType.objects.all()
    serializer_class = ModifierTypeSerializer
    relation_name = 'values__prices'
    scheme_relation_name = 'values__prices'


class PriceViewSet(NestedSchemeMixin, OrderedReadOnlyModelViewSet):
    """
    Viewing price(s).
    """
    queryset = Price.objects.all()
    serializer_class = PriceSerializer
    filter_backends = (backends.DjangoFilterBackend,)
    filter_class = PriceFilter


class CalculatorView(views.APIView):
    """
    Calculate total fee amount
    """

    allowed_methods = ['GET']
    schema = ManualSchema(fields=[
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
        }),
        coreapi.Field('unit', **{
            'required': False,
            'location': 'query',
            'type': 'string',
            'description': (
                'The code of the unit to calculate the price for. Default is `DAY`.'
            ),
        }),
        coreapi.Field('unit_count', **{
            'required': False,
            'location': 'query',
            'type': 'integer',
            'description': (
                'The number of units to calculate the price for. Default is 1.'
            ),
        }),
        coreapi.Field('modifier_%n', **{
            'required': False,
            'location': 'query',
            'type': 'integer',
            'description': (
                'The number of units of an applicable modifier. Paramater name is '
                'of the format `modifier_%n` where `%n` should be the integer '
                '`id` of the relevant modifier.'
            ),
        }),
    ])
    filter_backends = (backends.DjangoFilterBackend,)
    modifier_pattern = re.compile(r'modifier_(\d+)')

    def get_param(self, param_name, required=False, default=None):
        number = self.request.query_params.get(param_name, default)
        if number is None:
            if required:
                raise ValidationError('`%s` is a required field' % param_name)
        return number

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
                '`%s` is not a valid %s' % (param_name, model_class.__name__)
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
        unit = self.get_model_param('unit', Unit, default='DAY')
        unit_count = self.get_decimal_param('unit_count', default=Decimal('1'))

        modifier_counts = []
        for param in self.request.query_params:
            result = self.modifier_pattern.match(param)
            if result:
                try:
                    pk = result.group(1)
                    modifier_type = ModifierType.objects.get(pk=pk)
                except ModifierType.DoesNotExist:
                    raise ValidationError(
                        '`%s` is not a valid Modifier' % (pk)
                    )
                count = self.get_decimal_param(param)
                modifier_counts.append((modifier_type, count,))

        prices = Price.objects.filter(
            Q(advocate_type=advocate_type) | Q(advocate_type__isnull=True),
            Q(offence_class=offence_class) | Q(offence_class__isnull=True),
            scheme=scheme, fee_type__in=fee_types, unit=unit,
            scenario=scenario
        ).prefetch_related('modifiers')

        if len(prices) == 0:
            amount = 0
        else:
            # sum total from all prices whose range is covered by the unit_count
            amount = sum((
                price.calculate_total(unit_count, modifier_counts)
                for price in prices
            ))

        return Response({
            'amount': amount
        })
