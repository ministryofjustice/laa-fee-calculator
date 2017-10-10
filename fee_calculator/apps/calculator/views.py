# -*- coding: utf-8 -*-
from collections import OrderedDict
from datetime import datetime
import logging

from django.db.models import Q
from django.http import Http404
from rest_framework import filters, viewsets, views, status
from rest_framework.decorators import detail_route
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from .constants import SUTY_BASE_TYPE
from .filters import (
    PriceFilter, OffenceClassFilter, AdvocateTypeFilter, ScenarioFilter,
    FeeTypeFilter, ViewSchemaFilterBackend
)
from .models import (
    Scheme, FeeType, Scenario, OffenceClass, AdvocateType, Price, Unit
)
from .serializers import (
    SchemeSerializer, FeeTypeSerializer, ScenarioSerializer,
    OffenceClassSerializer, AdvocateTypeSerializer, PriceSerializer
)

logger = logging.getLogger('laa-calc')


class OrderedReadOnlyModelViewSet(viewsets.ReadOnlyModelViewSet):
    default_ordering = None

    def filter_queryset(self, queryset):
        queryset = queryset.order_by(self.default_ordering or 'pk')
        return super().filter_queryset(queryset)


class SchemeViewSetMixin():
    model = Scheme
    serializer_class = SchemeSerializer

    def get_queryset(self):
        return self.model.objects.all()


class BaseSchemeViewSet(SchemeViewSetMixin, OrderedReadOnlyModelViewSet):
    """
    API endpoint that allows schemas to be viewed.

    retrieve:
    Return a scheme instance.

    list:
    Return all schemes, ordered by id
    """
    lookup_value_regex = '\d+'


class SchemeViewSet(SchemeViewSetMixin, viewsets.GenericViewSet):
    """
    API endpoint that returns single scheme for suty type for a given case
    start date in format YYYY-MM-DD

    /api/v1/fee-schemes/advocate/2016-12-07/
    """
    lookup_field = 'suty'
    lookup_value_regex = '|'.join(
        [t.lower() for t in SUTY_BASE_TYPE.constants])

    @detail_route(url_path='(?P<case_date>[0-9-]+)')
    def get_by_date(self, request, suty=None, case_date=None):
        try:
            case_date = datetime.strptime(case_date, '%Y-%m-%d')
        except ValueError:
            raise Http404

        queryset = self.filter_queryset(self.get_queryset()).filter(
            Q(end_date__isnull=True) | Q(end_date__gte=case_date),
            suty_base_type=SUTY_BASE_TYPE.for_constant(suty.upper()).value,
            start_date__lte=case_date,
        )

        try:
            scheme = queryset.get()
        except Scheme.DoesNotExist:
            raise Http404

        return Response(SchemeSerializer(scheme).data)


class FeeTypeViewSet(OrderedReadOnlyModelViewSet):
    """
    Viewing fee type(s).
    """
    schema = OrderedDict([
        ('scheme', {
            'name': 'scheme',
            'required': False,
            'location': 'query',
            'type': 'integer',
            'description': '',
            'validator': int
        }),
        ('scenario', {
            'name': 'scenario',
            'required': False,
            'location': 'query',
            'type': 'integer',
            'description': '',
            'validator': int
        }),
        ('advocate_type', {
            'name': 'advocate_type',
            'required': False,
            'location': 'query',
            'type': 'string',
            'description': (
                'Note the query will return prices with `advocate_type_id` '
                'either matching the value or null.'),
            'validator': str
        }),
        ('offence_class_id', {
            'name': 'offence_class',
            'required': False,
            'location': 'query',
            'type': 'string',
            'description': (
                'Note the query will return prices with `offence_class_id` '
                'either matching the value or null.'),
            'validator': str
        }),
    ])
    queryset = FeeType.objects.all()
    serializer_class = FeeTypeSerializer
    filter_backends = (ViewSchemaFilterBackend,)
    filter_class = FeeTypeFilter

    def get_queryset(self):
        queryset = super().get_queryset()

        scheme_id = self.request.query_params.get('scheme')
        scenario_id = self.request.query_params.get('scenario')
        advocate_type_id = self.request.query_params.get('advocate_type')
        offence_class_id = self.request.query_params.get('offence_class')

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

        if filters:
            queryset = queryset.filter(*filters).distinct()
        return queryset


class ScenarioViewSet(OrderedReadOnlyModelViewSet):
    """
    Viewing scenario(s).
    """
    queryset = Scenario.objects.all()
    serializer_class = ScenarioSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = ScenarioFilter


class OffenceClassViewSet(OrderedReadOnlyModelViewSet):
    """
    Viewing offence class(es).
    """
    queryset = OffenceClass.objects.all()
    serializer_class = OffenceClassSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = OffenceClassFilter


class AdvocateTypeViewSet(OrderedReadOnlyModelViewSet):
    """
    Advocate types.
    """
    queryset = AdvocateType.objects.all()
    serializer_class = AdvocateTypeSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = AdvocateTypeFilter


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
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = PriceFilter


class CalculatorView(views.APIView):
    allowed_methods = ['GET']
    schema = OrderedDict([
        ('scheme', {
            'name': 'scheme',
            'required': True,
            'location': 'query',
            'type': 'integer',
            'description': '',
            'validator': int
        }),
        ('fee_type_code', {
            'name': 'fee_type_code',
            'required': True,
            'location': 'query',
            'type': 'string',
            'description': '',
            'validator': str
        }),
        ('scenario', {
            'name': 'scenario',
            'required': True,
            'location': 'query',
            'type': 'integer',
            'description': '',
            'validator': int
        }),
        ('advocate_type', {
            'name': 'advocate_type',
            'required': False,
            'location': 'query',
            'type': 'string',
            'description': (
                'Note the query will return prices with `advocate_type_id` '
                'either matching the value or null.'),
            'validator': str
        }),
        ('offence_class_id', {
            'name': 'offence_class',
            'required': False,
            'location': 'query',
            'type': 'string',
            'description': (
                'Note the query will return prices with `offence_class_id` '
                'either matching the value or null.'),
            'validator': str
        }),
        ('unit', {
            'name': 'unit',
            'required': False,
            'location': 'query',
            'type': 'string',
            'description': (
                'The code of the unit to calculate the price for. Default is `DAY`.'
            ),
            'validator': str
        }),
        ('unit_count', {
            'name': 'unit_count',
            'required': False,
            'location': 'query',
            'type': 'integer',
            'description': (
                'The number of units to calculate the price for. Default is 1.'
            ),
            'validator': int
        }),
        ('uplift_unit_%n', {
            'name': 'uplift_unit_%n',
            'required': False,
            'location': 'query',
            'type': 'string',
            'description': (
                'A unit of an applicable uplift. Paramater name is of the format '
                '`uplift_unit_%n` where `%n` should be an integer. There should be '
                'a corresponding `uplift_unit_count_%n` for the same `%n`.'
            ),
            'validator': str
        }),
        ('uplift_unit_count_%n', {
            'name': 'uplift_unit_count_%n',
            'required': False,
            'location': 'query',
            'type': 'integer',
            'description': (
                'The number of units of an applicable uplift. Paramater name is '
                'of the format `uplift_unit_count_%n` where `%n` should be an '
                'integer. There should be a corresponding `uplift_unit_%n` for '
                'the same `%n`.'
            ),
            'validator': int
        }),
    ])
    filter_backends = (ViewSchemaFilterBackend,)

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

        i = 1
        uplift_unit_counts = []
        while True:
            uplift_unit = self.get_model_param('uplift_unit_%s' % i, Unit)
            unit_present = uplift_unit is not None

            uplift_unit_count = self.get_integer_param('uplift_unit_count_%s' % i)
            count_present = uplift_unit_count is not None

            if unit_present and count_present:
                uplift_unit_counts.append((uplift_unit, uplift_unit_count,))
                i += 1
            elif unit_present and not count_present:
                return Response(
                    '`uplift_unit_%s` provided but '
                    '`uplift_unit_count_%s` is missing' % (i, i),
                    status=status.HTTP_400_BAD_REQUEST
                )
            elif not unit_present and count_present:
                return Response(
                    '`uplift_unit_count_%s` provided but '
                    '`uplift_unit_%s` is missing' % (i, i),
                    status=status.HTTP_400_BAD_REQUEST
                )
            else:
                break

        prices = Price.objects.filter(
            Q(advocate_type=advocate_type) | Q(advocate_type__isnull=True),
            Q(offence_class=offence_class) | Q(offence_class__isnull=True),
            scheme=scheme, fee_type__in=fee_types, unit=unit,
            scenario=scenario
        ).prefetch_related('uplifts')

        if len(prices) == 0:
            return Response(
                'No prices exist for query', status=status.HTTP_400_BAD_REQUEST
            )

        # sum total from all prices whose range is covered by the unit_count
        return Response({
            'amount': sum((
                price.calculate_total(unit_count, uplift_unit_counts)
                for price in prices
            ))
        })
