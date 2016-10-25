# -*- coding: utf-8 -*-
from datetime import datetime

from django.db.models import Q
from django.http import Http404

from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from .constants import SUTY_BASE_TYPE
from .models import (
    Scheme, FeeType, Scenario, OffenceClass, AdvocateType, Price)
from .serializers import (
    SchemeSerializer, FeeTypeSerializer, ScenarioSerializer,
    OffenceClassSerializer, AdvocateTypeSerializer, PriceSerializer)


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
    ---
    list:
        parameters:
            - name: scenario_id
              description: scenario id
            - name: advocate_type_id
              description: advocate type id
            - name: fee_type_id
              description: fee type id
    """
    serializer_class = PriceSerializer

    def get_queryset(self):
        queryset = Price.objects.all()
        scenario_id = self.request.query_params.get('scenario_id', None)
        advocate_type_id = self.request.query_params.get(
            'advocate_type_id', None)
        fee_type_id = self.request.query_params.get('fee_type_id', None)
        if scenario_id:
            try:
                scenario = Scenario.objects.get(id=scenario_id)
            except Scenario.DoesNotExist:
                raise Http404
            fee_types = FeeType.objects.filter(scenarios__in=[scenario])
            queryset = queryset.filter(fee_type__in=fee_types)
        if advocate_type_id:
            queryset = queryset.filter(advocate_type_id=advocate_type_id)
        if fee_type_id:
            queryset = queryset.filter(fee_type_id=fee_type_id)
        return queryset
