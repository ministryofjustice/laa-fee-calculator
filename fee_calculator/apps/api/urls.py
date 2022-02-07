# -*- coding: utf-8 -*-
from django.conf.urls import url, include

from rest_framework_nested import routers
from rest_framework_swagger.views import get_swagger_view

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

schema_view = get_swagger_view(title='Calculator API')

urlpatterns = (
    url(r'^fee-schemes/(?P<scheme_pk>[^/.]+)/calculate/$', CalculatorView.as_view(), name='calculator'),
    url(r'^', include(router.urls)),
    url(r'^', include(schemes_router.urls)),
    url(r'^docs/$', schema_view),
)
