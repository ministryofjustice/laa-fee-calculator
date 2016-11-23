# -*- coding: utf-8 -*-
from collections import OrderedDict
from datetime import datetime

from django.db.models import Q
from django.http import Http404
from rest_framework import viewsets, views
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from .constants import SUTY_BASE_TYPE
from .models import (
    Scheme, FeeType, Scenario, OffenceClass, AdvocateType, Price)
from .serializers import (
    SchemeSerializer, FeeTypeSerializer, ScenarioSerializer,
    OffenceClassSerializer, AdvocateTypeSerializer, PriceSerializer)
from .filters import swagger_filter_backend_class


class SchemeViewSetMixin():
    model = Scheme
    serializer_class = SchemeSerializer

    def get_queryset(self):
        return self.model.objects.all()


class BaseSchemeViewSet(SchemeViewSetMixin, viewsets.ReadOnlyModelViewSet):
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

    /api/v1/scheme/advocate/2016-12-07/
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


class FeeTypeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Viewing fee type(s).
    """
    queryset = FeeType.objects.all()
    serializer_class = FeeTypeSerializer


class ScenarioViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Viewing scenario(s).
    """
    queryset = Scenario.objects.all()
    serializer_class = ScenarioSerializer


class OffenceClassViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Viewing offence class(es).
    """
    queryset = OffenceClass.objects.all()
    serializer_class = OffenceClassSerializer


class AdvocateTypeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Advocate types.
    """
    queryset = AdvocateType.objects.all()
    serializer_class = AdvocateTypeSerializer


class PriceViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Prices.

    retrieve:
    get a price instance.

    list:
    get a list of prices.
    """

    schema = OrderedDict([
        ('scheme_id', {
            'name': 'scheme_id',
            'required': False,
            'location': 'query',
            'type': 'integer',
            'description': 'The id of fee scheme.',
            'validator': int
         }),
        ('scenario_id', {
            'name': 'scenario_id',
            'required': False,
            'location': 'query',
            'type': 'integer',
            'description': 'The id of scenario.',
            'validator': int
         }),
        ('fee_type_id', {
            'name': 'fee_type_id',
            'required': False,
            'location': 'query',
            'type': 'integer',
            'description': 'The id of fee type.',
            'validator': int
         }),
        ('advocate_type_id', {
            'name': 'advocate_type_id',
            'required': False,
            'location': 'query',
            'type': 'integer',
            'description': (
                'The id of advocate type. Note the query will return prices'
                ' with `advocate_type_id` either matching the value or null.'),
            'validator': str
         }),
        ('offence_class_id', {
            'name': 'offence_class_id',
            'required': False,
            'location': 'query',
            'type': 'integer',
            'description': (
                'The id of offence class. Note the query will return prices'
                ' with `offence_class_id` either matching the value or null.'),
            'validator': str
         }),
    ])
    serializer_class = PriceSerializer
    filter_backends = (swagger_filter_backend_class(schema.values()),)

    def sanitise_parameter(self, name):
        """
        sanitise query parameter
        :param name: name of the parameter
        :return: value of the sanitised parameter or None if name not found.
        :raise: ValidationError
        """
        field_schema = self.schema[name]
        try:
            value = self.request.query_params[name]
        except KeyError:
            if not field_schema['required']:
                return
            raise ValidationError('Missing required field {}'.format(name))
        try:
            return field_schema['validator'](value)
        except Exception:
            detail = "Invalid parameter {}='{}'.".format(name, value)
            raise ValidationError(detail)

    def get_queryset(self):
        scheme_id = self.sanitise_parameter('scheme_id')
        fee_type_id = self.sanitise_parameter('fee_type_id')
        scenario_id = self.sanitise_parameter('scenario_id')
        advocate_type_id = self.sanitise_parameter('advocate_type_id')
        offence_class_id = self.sanitise_parameter('offence_class_id')
        queryset = Price.objects.all()
        if scheme_id:
            queryset = queryset.filter(scheme_id=scheme_id)
        if fee_type_id:
            queryset = queryset.filter(fee_type_id=fee_type_id)
        if scenario_id:
            queryset = queryset.filter(scenario_id=scenario_id)
        if advocate_type_id:
            # for convenience of real usecase, either match or null
            # instead of just match
            queryset = queryset.filter(
                Q(advocate_type_id=advocate_type_id) |
                Q(advocate_type_id__isnull=True))
        if offence_class_id:
            # for convenience of real usecase, either match or null
            # instead of just match
            queryset = queryset.filter(
                Q(offence_class_id=offence_class_id) |
                Q(offence_class_id__isnull=True))
        return queryset


class CalculatorView(views.APIView):
    allowed_methods = ['GET']

    def get(self, *args, **kwargs):
        suty = self.request.query_params.get('suty')
        rep_order_date = self.request.query_params.get('rep_order_date')
        fee_type_code = self.request.query_params.get('fee_type_code')
        scenario_id = self.request.query_params.get('scenario_id')
        advocate_type_id = self.request.query_params.get('advocate_type_id')
        offence_class_id = self.request.query_params.get('offence_class_id')

        try:
            case_date = datetime.strptime(rep_order_date, '%Y-%m-%d')
        except ValueError:
            raise Http404

        try:
            scheme = Scheme.objects.get(
                Q(end_date__isnull=True) | Q(end_date__gte=case_date),
                suty_base_type=SUTY_BASE_TYPE.for_constant(suty.upper()).value,
                start_date__lte=case_date,
            )
        except Scheme.DoesNotExist:
            print('scheme doesnt exist for %s: %s' % (SUTY_BASE_TYPE.for_constant(suty.upper()).value, case_date))
            raise Http404

        queryset = Price.objects.filter(
            Q(fee_type__code=fee_type_code) | Q(fee_type__code__isnull=True),
            Q(advocate_type_id=advocate_type_id) | Q(advocate_type_id__isnull=True),
            Q(offence_class_id=offence_class_id) | Q(offence_class_id__isnull=True),
            scheme_id=scheme.pk,
            scenario_id=scenario_id,
        )

        return Response({
            'amount': 100,
            'price_count': queryset.count(),
        })
