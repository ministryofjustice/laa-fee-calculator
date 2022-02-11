# -*- coding: utf-8 -*-
from django.conf.urls import url, re_path, include

from rest_framework_nested import routers
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from api.views import (
    SchemeViewSet, FeeTypeViewSet, ScenarioViewSet,
    OffenceClassViewSet, AdvocateTypeViewSet, PriceViewSet, CalculatorView,
    UnitViewSet, ModifierTypeViewSet
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

schema_view = get_schema_view(
   openapi.Info(
      title="Fee calculator API",
      default_version='v1',
      description="API for calculating fees or retrieving prices for Advocate and Litigator Graduated Fee Schemes",
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
   validators=['ssv'],
)

# FROM dry-yasg docs
# urlpatterns = [
#    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
#    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
#    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
# ]

urlpatterns = (
    url(r'^fee-schemes/(?P<scheme_pk>[^/.]+)/calculate/$', CalculatorView.as_view(), name='calculator'),
    url(r'^', include(router.urls)),
    url(r'^', include(schemes_router.urls)),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    url(r'^docs/$', schema_view.with_ui('swagger', cache_timeout=0)),
)
