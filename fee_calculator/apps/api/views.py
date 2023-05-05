# -*- coding: utf-8 -*-
from decimal import Decimal
from api.utils import ModelParamFetcher, DecimalParamFetcher
import logging

from django.db.models import Q
from django_filters.rest_framework import backends
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_control
from rest_framework import viewsets, views
from rest_framework.generics import get_object_or_404
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from drf_spectacular.utils import (
    extend_schema_view, extend_schema, OpenApiParameter, OpenApiTypes
)

from calculator.models import (
    Scheme, FeeType, Scenario, OffenceClass, AdvocateType, Price, Unit,
    ModifierType, calculate_total
)

from .filters import (
    PriceFilter,
    FeeTypeFilter,
    SchemeFilter,
)

from .serializers import (
    SchemeListQuerySerializer,
    BasePriceFilteredQuerySerializer,
    CalculatorQuerySerializer,
    CalculatorResponseSerializer,
    SchemeSerializer,
    FeeTypeSerializer,
    UnitSerializer,
    ModifierTypeSerializer,
    ScenarioSerializer,
    OffenceClassSerializer,
    AdvocateTypeSerializer,
    PriceSerializer,
)

logger = logging.getLogger('laa-calc')

scheme_pk_parameter = OpenApiParameter('scheme_pk', OpenApiTypes.INT, OpenApiParameter.PATH)


class OrderedReadOnlyModelViewSet(viewsets.ReadOnlyModelViewSet):
    default_ordering = None

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        queryset = queryset.order_by(self.default_ordering or 'pk')
        return queryset


@method_decorator(cache_control(public=True, max_age=2*60*60), name='dispatch')
@extend_schema_view(
    list=extend_schema(
        description='Filterable list of graduated fee schemes',
        parameters=[SchemeListQuerySerializer],
    ),
    retrieve=extend_schema(
        description='Retrieve a single graduated fee scheme',
        parameters=[SchemeListQuerySerializer],
    )
)
class SchemeViewSet(OrderedReadOnlyModelViewSet):
    """
    Viewing fee scheme(s).
    """
    queryset = Scheme.objects.all()
    serializer_class = SchemeSerializer
    filter_backends = (backends.DjangoFilterBackend,)
    filterset_class = SchemeFilter


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

    def dispatch(self, request, *args, **kwargs):
        request.fee_scheme = get_object_or_404(Scheme, pk=kwargs['scheme_pk'])

        return super().dispatch(request, *args, **kwargs)


@method_decorator(cache_control(public=True, max_age=2*60*60), name='dispatch')
@extend_schema_view(
    list=extend_schema(
        parameters=[BasePriceFilteredQuerySerializer],
    ),
    retrieve=extend_schema(
        parameters=[BasePriceFilteredQuerySerializer],
    )
)
class BasePriceFilteredViewSet(NestedSchemeMixin, OrderedReadOnlyModelViewSet):
    relation_name = NotImplemented
    lookup_attr = 'pk'

    def filter_queryset(self, queryset):
        scheme = get_object_or_404(Scheme, pk=self.kwargs['scheme_pk'])
        queryset = super().filter_queryset(queryset)

        fee_types = ModelParamFetcher(
            self.request, 'fee_type_code', FeeType, scheme, lookup='code', many=True
        ).call()
        scenario = ModelParamFetcher(self.request, 'scenario', Scenario, scheme)
        advocate_type = ModelParamFetcher(self.request, 'advocate_type', AdvocateType, scheme).call()
        offence_class = ModelParamFetcher(self.request, 'offence_class', OffenceClass, scheme).call()

        filters = []
        if scenario.present:
            filters.append(scenario.as_q)
        if advocate_type:
            filters.append(
                Q(advocate_type=advocate_type) |
                Q(advocate_type__isnull=True)
            )
        if offence_class:
            filters.append(
                Q(offence_class=offence_class) |
                Q(offence_class__isnull=True)
            )
        if fee_types:
            filters.append(
                Q(fee_type__in=fee_types)
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


@method_decorator(cache_control(public=True, max_age=2*60*60), name='dispatch')
@extend_schema(parameters=[scheme_pk_parameter, ],)
@extend_schema_view(
    list=extend_schema(
        description='Filterable list of fee types',
    ),
    retrieve=extend_schema(
        description='Retrieve a single fee type',
        parameters=[
            OpenApiParameter("is_basic", OpenApiTypes.BOOL, OpenApiParameter.QUERY),
        ],
    )
)
class FeeTypeViewSet(BasePriceFilteredViewSet):
    """
    Viewing fee type(s).
    """
    queryset = FeeType.objects.all()
    serializer_class = FeeTypeSerializer
    filter_backends = (backends.DjangoFilterBackend,)
    filterset_class = FeeTypeFilter
    relation_name = 'fee_type'


@method_decorator(cache_control(public=True, max_age=2*60*60), name='dispatch')
@extend_schema(parameters=[scheme_pk_parameter, ],)
@extend_schema_view(
    list=extend_schema(
        description='Filterable list of unit types',
    ),
    retrieve=extend_schema(
        description='Retrieve a single unit type',
    )
)
class UnitViewSet(BasePriceFilteredViewSet):
    """
    Viewing unit(s).
    """
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer
    relation_name = 'unit'


@method_decorator(cache_control(public=True, max_age=2*60*60), name='dispatch')
@extend_schema(parameters=[scheme_pk_parameter, ],)
@extend_schema_view(
    list=extend_schema(
        description='Filterable list of modifier types',
    ),
    retrieve=extend_schema(
        description='Retrieve a single modifier type',
    )
)
class ModifierTypeViewSet(BasePriceFilteredViewSet):
    """
    Viewing modifier type(s).
    """
    queryset = ModifierType.objects.all()
    serializer_class = ModifierTypeSerializer
    relation_name = 'modifiers'
    lookup_attr = 'values__pk'
    scheme_relation_name = 'values__prices__scheme'


@method_decorator(cache_control(public=True, max_age=2*60*60), name='dispatch')
@extend_schema(parameters=[scheme_pk_parameter, ],)
@extend_schema_view(
    list=extend_schema(
        description='Filterable list of scenarios',
    ),
    retrieve=extend_schema(
        description='Retrieve a single scenario',
    )
)
class ScenarioViewSet(NestedSchemeMixin, OrderedReadOnlyModelViewSet):
    """
    Viewing scenario(s).
    """
    queryset = Scenario.objects.all()
    serializer_class = ScenarioSerializer


@method_decorator(cache_control(public=True, max_age=2*60*60), name='dispatch')
@extend_schema(parameters=[scheme_pk_parameter, ],)
@extend_schema_view(
    list=extend_schema(
        description='Filterable list of offence classes',
    ),
    retrieve=extend_schema(
        description='Retrieve a single offence class',
    )
)
class OffenceClassViewSet(NestedSchemeMixin, OrderedReadOnlyModelViewSet):
    """
    Viewing offence class(es).
    """
    queryset = OffenceClass.objects.all()
    serializer_class = OffenceClassSerializer
    lookup_value_regex = '[^/]+'


@method_decorator(cache_control(public=True, max_age=2*60*60), name='dispatch')
@extend_schema(parameters=[scheme_pk_parameter, ],)
@extend_schema_view(
    list=extend_schema(
        description='Filterable list of advocate types',
    ),
    retrieve=extend_schema(
        description='Retrieve a single advocate type',
    ),
)
class AdvocateTypeViewSet(NestedSchemeMixin, OrderedReadOnlyModelViewSet):
    """
    Viewing advocate type(s).
    """
    queryset = AdvocateType.objects.all()
    serializer_class = AdvocateTypeSerializer


@method_decorator(cache_control(public=True, max_age=2*60*60), name='dispatch')
@extend_schema(parameters=[scheme_pk_parameter, ],)
@extend_schema_view(
    list=extend_schema(
        description='Filterable list of prices',
    ),
    retrieve=extend_schema(
        description='Retrieve a single price',
        parameters=[BasePriceFilteredQuerySerializer],
    )
)
class PriceViewSet(NestedSchemeMixin, OrderedReadOnlyModelViewSet):
    """
    Viewing price(s).
    """
    queryset = Price.objects.all()
    serializer_class = PriceSerializer
    filter_backends = (backends.DjangoFilterBackend,)
    filterset_class = PriceFilter
    scheme_relation_name = 'scheme'


@method_decorator(cache_control(public=True, max_age=2*60*60), name='dispatch')
@extend_schema(parameters=[scheme_pk_parameter, ],)
@extend_schema_view(
    get=extend_schema(
        parameters=[CalculatorQuerySerializer],
        responses=CalculatorResponseSerializer
    )
)
class CalculatorView(views.APIView):
    """
    Calculate total fee amount
    """
    allowed_methods = ['GET']
    filter_backends = (backends.DjangoFilterBackend,)

    def get(self, *args, **kwargs):
        scheme = get_object_or_404(Scheme, pk=kwargs['scheme_pk'])
        fee_types = ModelParamFetcher(
            self.request, 'fee_type_code', FeeType, scheme, required=True, lookup='code', many=True
        ).call()
        scenario = ModelParamFetcher(self.request, 'scenario', Scenario, scheme, required=True)
        advocate_type = ModelParamFetcher(self.request, 'advocate_type', AdvocateType, scheme).call()
        offence_class = ModelParamFetcher(self.request, 'offence_class', OffenceClass, scheme).call()

        units = Unit.objects.values_list('pk', flat=True)
        modifiers = ModifierType.objects.values_list('name', flat=True)
        unit_counts = []
        modifier_counts = []
        for param in self.request.query_params:
            if param.upper() in units:
                unit_counts.append((
                    Unit.objects.get(pk=param.upper()),
                    DecimalParamFetcher(self.request, param).call(),
                ))

            if param.upper() in modifiers:
                modifier_counts.append((
                    ModifierType.objects.get(name=param.upper()),
                    DecimalParamFetcher(self.request, param).call(),
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
