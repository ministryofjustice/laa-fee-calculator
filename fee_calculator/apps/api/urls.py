# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from django.urls import path

from rest_framework_nested import routers
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from api.views import (
    SchemeViewSet,
    FeeTypeViewSet,
    UnitViewSet,
    ModifierTypeViewSet,
    ScenarioViewSet,
    OffenceClassViewSet,
    AdvocateTypeViewSet,
    PriceViewSet,
    CalculatorView,
)

router = routers.DefaultRouter()
router.register(r'fee-schemes', SchemeViewSet, basename='fee-schemes')

schemes_router = routers.NestedSimpleRouter(router, r'fee-schemes', lookup='scheme')
schemes_router.register(r'fee-types', FeeTypeViewSet, basename='fee-types')
schemes_router.register(r'scenarios', ScenarioViewSet, basename='scenarios')
schemes_router.register(r'advocate-types', AdvocateTypeViewSet,
                        basename='advocate-types')
schemes_router.register(r'offence-classes', OffenceClassViewSet,
                        basename='offence-classes')
schemes_router.register(r'units', UnitViewSet, basename='units')
schemes_router.register(r'modifier-types', ModifierTypeViewSet,
                        basename='modifier-types')
schemes_router.register(r'prices', PriceViewSet, basename='prices')

urlpatterns = (
    url(r'^fee-schemes/(?P<scheme_pk>[^/.]+)/calculate/$', CalculatorView.as_view(), name='calculator'),
    url(r'^', include(router.urls)),
    url(r'^', include(schemes_router.urls)),

    # drf-spectacular = OpenAPI3
    path('oa3/schema/', SpectacularAPIView.as_view(), name='oa3_schema'),
    path('oa3/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='oa3_schema'), name='oa3_swagger-ui'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='oa3_schema')),
)

