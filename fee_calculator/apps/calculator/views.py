# -*- coding: utf-8 -*-
from datetime import datetime

from django.db.models import Q
from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.exceptions import NotFound
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework.compat import coreapi

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

    api_doc = [
        {
            'name': 'scheme_id',
            'required': True,
            'location': 'query',
            'type': 'integer',
            'description': 'The id of fee scheme.'
         },
        {
            'name': 'scenario_id',
            'required': False,
            'location': 'query',
            'type': 'integer',
            'description': 'The id of scenario.'
         },
        {
            'name': 'fee_type_id',
            'required': False,
            'location': 'query',
            'type': 'integer',
            'description': 'The id of fee type.'
         },
        {
            'name': 'advocate_type_id',
            'required': False,
            'location': 'query',
            'type': 'integer',
            'description': (
                'The id of advocate type. Note the query will return prices'
                ' with `advocate_type_id` either matching the value or null.')
         },
        {
            'name': 'offence_class_id',
            'required': False,
            'location': 'query',
            'type': 'integer',
            'description': (
                'The id of offence class. Note the query will return prices'
                ' with `offence_class_id` either matching the value or null.')
         },
    ]
    serializer_class = PriceSerializer
    filter_backends = (swagger_filter_backend_class(api_doc),)
    filter_fields = ('scheme_id', 'fee_type_id')

    def sanitise_parameter(self, name, sanitise):
        """
        sanitise query parameter
        :param name: name of the parameter
        :param sanitise: a function for validating the value. it should return
        the sanitised value or raise an exception if not valid.
        :return: value of the sanitised parameter or None if name not found.
        :raise: NotFound
        """
        try:
            value = self.request.query_params[name]
        except KeyError:
            return
        try:
            return sanitise(value)
        except Exception:
            detail = "Invalid parameter {}='{}'.".format(name, value)
            raise NotFound(detail)

    def get_queryset(self):
        scenario_id = self.sanitise_parameter('scenario_id', int)
        advocate_type_id = self.sanitise_parameter('advocate_type_id', int)
        offence_class_id = self.sanitise_parameter('offence_class_id', int)
        queryset = Price.objects.all()
        if scenario_id:
            try:
                scenario = Scenario.objects.get(id=scenario_id)
            except Scenario.DoesNotExist:
                detail = "Cannot find a scenario with id='{}'.".format(
                    scenario_id)
                raise NotFound(detail)
            fee_types = FeeType.objects.filter(scenarios__in=[scenario])
            queryset = queryset.filter(fee_type__in=fee_types)
        if advocate_type_id:
            # for convenience of real usecase, either match or null
            # instead of just match
            queryset = queryset.filter(
                Q(advocate_type_id=advocate_type_id) |
                Q(advocate_type_id__isnull=True))
        if offence_class_id:
            # for convenience of real usecase, either match or None
            # instead of just match
            queryset = queryset.filter(
                Q(offence_class_id=offence_class_id) |
                Q(offence_class_id__isnull=True))
        return queryset
