# -*- coding: utf-8 -*-
from datetime import datetime
from decimal import Decimal
import logging

from django.db.models import Q
from django.http import Http404
from rest_framework import filters, viewsets, views
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from .constants import SUTY_BASE_TYPE
from .filters import (
    PriceFilter, OffenceClassFilter, AdvocateTypeFilter, ScenarioFilter,
    FeeTypeFilter
)
from .models import (
    Scheme, FeeType, Scenario, OffenceClass, AdvocateType, Price
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


class FeeTypeViewSet(OrderedReadOnlyModelViewSet):
    """
    Viewing fee type(s).
    """
    queryset = FeeType.objects.all()
    serializer_class = FeeTypeSerializer
    filter_backends = (filters.DjangoFilterBackend,)
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

    def get(self, *args, **kwargs):
        suty = self.request.query_params.get('suty')
        rep_order_date = self.request.query_params.get('rep_order_date')
        fee_type_code = self.request.query_params.get('fee_type_code')
        scenario_id = self.request.query_params.get('scenario')
        advocate_type_id = self.request.query_params.get('advocate_type')
        offence_class_id = self.request.query_params.get('offence_class')
        unit_count = self.request.query_params.get('unit_count')

        suty_code = SUTY_BASE_TYPE.for_constant(suty.upper()).value

        try:
            case_date = datetime.strptime(rep_order_date, '%Y-%m-%d')
        except ValueError:
            raise Http404

        try:
            scheme = Scheme.objects.get(
                Q(end_date__isnull=True) | Q(end_date__gte=case_date),
                suty_base_type=suty_code,
                start_date__lte=case_date,
            )
        except Scheme.DoesNotExist:
            logger.error('Scheme doesnt exist for %s: %s' % (suty_code, case_date))
            raise Http404

        prices = Price.objects.filter(
            Q(fee_type__code=fee_type_code) | Q(fee_type__code__isnull=True),
            Q(advocate_type_id=advocate_type_id) | Q(advocate_type_id__isnull=True),
            Q(offence_class_id=offence_class_id) | Q(offence_class_id__isnull=True),
            Q(limit_to__lte=unit_count) | Q(limit_to__isnull=True),
            limit_from__gte=unit_count,
            scheme_id=scheme.pk,
            scenario_id=scenario_id,
        )

        return Response({
            'amount': (prices.first().fee_per_unit*Decimal(unit_count)) if prices.first() else 0,
        })
