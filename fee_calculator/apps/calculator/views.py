# -*- coding: utf-8 -*-
from datetime import datetime
import logging
import re

from django.db.models import Q
from django.http import Http404
from django_filters.rest_framework import backends
from rest_framework import viewsets, views, status
from rest_framework.compat import coreapi
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.schemas import AutoSchema, ManualSchema

from .constants import SUTY_BASE_TYPE
from .filters import (
    PriceFilter, OffenceClassFilter, AdvocateTypeFilter, ScenarioFilter,
    FeeTypeFilter
)
from .models import (
    Scheme, FeeType, Scenario, OffenceClass, AdvocateType, Price, Unit, Modifier
)
from .serializers import (
    SchemeSerializer, FeeTypeSerializer, ScenarioSerializer,
    OffenceClassSerializer, AdvocateTypeSerializer, PriceSerializer,
    UnitSerializer, ModifierSerializer
)

logger = logging.getLogger('laa-calc')


class OrderedReadOnlyModelViewSet(viewsets.ReadOnlyModelViewSet):
    default_ordering = None

    def filter_queryset(self, queryset):
        queryset = queryset.order_by(self.default_ordering or 'pk')
        return super().filter_queryset(queryset)


class SchemeViewSet(OrderedReadOnlyModelViewSet):
    """
    Viewing fee type(s).
    """
    schema = AutoSchema(manual_fields=[
        coreapi.Field('suty', **{
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

        suty = self.request.query_params.get('suty')
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

        if suty:
            try:
                suty = SUTY_BASE_TYPE.for_constant(suty.upper()).value
            except KeyError:
                raise ValidationError(
                    '`suty` should be one of: [%s]'
                    % ', '.join(SUTY_BASE_TYPE.constants)
                )
            queryset = queryset.filter(suty_base_type=suty)

        return queryset


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

    def get_queryset(self):
        queryset = super().get_queryset()

        scheme_id = self.request.query_params.get('scheme')
        scenario_id = self.request.query_params.get('scenario')
        advocate_type_id = self.request.query_params.get('advocate_type')
        offence_class_id = self.request.query_params.get('offence_class')
        fee_type_code = self.request.query_params.get('fee_type_code')

        filters = []
        if scheme_id:
            filters.append(Q(prices__scheme_id=scheme_id))
        if scenario_id:
            filters.append(Q(prices__scenario_id=scenario_id))
        if advocate_type_id:
            filters.append(
                Q(prices__advocate_type_id=advocate_type_id) |
                Q(prices__advocate_type_id__isnull=True)
            )
        if offence_class_id:
            filters.append(
                Q(prices__offence_class_id=offence_class_id) |
                Q(prices__offence_class_id__isnull=True)
            )
        if fee_type_code:
            filters.append(
                Q(prices__fee_type__code=fee_type_code)
            )

        if filters:
            queryset = queryset.filter(*filters).distinct()
        return queryset


class FeeTypeViewSet(BasePriceFilteredViewSet):
    """
    Viewing fee type(s).
    """
    queryset = FeeType.objects.all()
    serializer_class = FeeTypeSerializer
    filter_class = FeeTypeFilter


class ScenarioViewSet(OrderedReadOnlyModelViewSet):
    """
    Viewing scenario(s).
    """
    queryset = Scenario.objects.all()
    serializer_class = ScenarioSerializer
    filter_backends = (backends.DjangoFilterBackend,)
    filter_class = ScenarioFilter


class OffenceClassViewSet(OrderedReadOnlyModelViewSet):
    """
    Viewing offence class(es).
    """
    queryset = OffenceClass.objects.all()
    serializer_class = OffenceClassSerializer
    filter_backends = (backends.DjangoFilterBackend,)
    filter_class = OffenceClassFilter


class AdvocateTypeViewSet(OrderedReadOnlyModelViewSet):
    """
    Advocate types.
    """
    queryset = AdvocateType.objects.all()
    serializer_class = AdvocateTypeSerializer
    filter_backends = (backends.DjangoFilterBackend,)
    filter_class = AdvocateTypeFilter


class UnitViewSet(BasePriceFilteredViewSet):
    """
    Viewing fee type(s).
    """
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer


class ModifierViewSet(BasePriceFilteredViewSet):
    """
    Viewing fee type(s).
    """
    queryset = Modifier.objects.all()
    serializer_class = ModifierSerializer


class PriceViewSet(OrderedReadOnlyModelViewSet):
    """
    Prices.

    retrieve:
    get a price instance.

    list:
    get a list of prices.
    """
    queryset = Price.objects.all()
    serializer_class = PriceSerializer
    filter_backends = (backends.DjangoFilterBackend,)
    filter_class = PriceFilter


class CalculatorView(views.APIView):
    allowed_methods = ['GET']
    schema = ManualSchema(fields=[
        coreapi.Field('scheme', **{
            'required': True,
            'location': 'query',
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
        coreapi.Field('offence_class_id', **{
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

    def get_integer_param(self, param_name, required=False, default=None):
        number = self.get_param(param_name, required, default)
        try:
            if number is not None:
                number = int(number)
        except ValueError:
            raise ValidationError('`%s` must be an integer' % param_name)
        return number

    def get(self, *args, **kwargs):
        scheme = self.get_model_param('scheme', Scheme, required=True)
        fee_types = self.get_model_param(
            'fee_type_code', FeeType, required=True, lookup='code', many=True
        )
        scenario = self.get_model_param('scenario', Scenario, required=True)
        advocate_type = self.get_model_param('advocate_type', AdvocateType)
        offence_class = self.get_model_param('offence_class', OffenceClass)
        unit = self.get_model_param('unit', Unit, default='DAY')
        unit_count = self.get_integer_param('unit_count', default=1)

        modifier_counts = []
        for param in self.request.query_params:
            result = self.modifier_pattern.match(param)
            if result:
                try:
                    pk = result.group(1)
                    modifier = Modifier.objects.get(pk=pk)
                except Modifier.DoesNotExist:
                    raise ValidationError(
                        '`%s` is not a valid Modifier' % (pk)
                    )
                count = self.request.query_params[param]
                modifier_counts.append((modifier, count,))

        prices = Price.objects.filter(
            Q(advocate_type=advocate_type) | Q(advocate_type__isnull=True),
            Q(offence_class=offence_class) | Q(offence_class__isnull=True),
            scheme=scheme, fee_type__in=fee_types, unit=unit,
            scenario=scenario
        ).prefetch_related('modifiers', 'modifiers__values')

        if len(prices) == 0:
            return Response(
                'No prices exist for query', status=status.HTTP_400_BAD_REQUEST
            )

        # sum total from all prices whose range is covered by the unit_count
        return Response({
            'amount': sum((
                price.calculate_total(unit_count, modifier_counts)
                for price in prices
            ))
        })
