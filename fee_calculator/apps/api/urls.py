# -*- coding: utf-8 -*-
from django.conf.urls import url, include

from rest_framework import routers
from rest_framework_swagger.views import get_swagger_view

from calculator.views import (
    BaseSchemeViewSet, SchemeViewSet, FeeTypeViewSet, ScenarioViewSet,
    OffenceClassViewSet, AdvocateTypeViewSet, PriceViewSet, CalculatorView
)


router = routers.DefaultRouter()
router.register(r'fee-schemes', BaseSchemeViewSet, base_name='fee-schemes')
router.register(r'fee-schemes', SchemeViewSet, base_name='fee-schemes')
router.register(r'fee-types', FeeTypeViewSet, base_name='fee-types')
router.register(r'scenarios', ScenarioViewSet, base_name='scenarios')
router.register(r'advocate-types', AdvocateTypeViewSet,
                base_name='advocate-types')
router.register(r'offence-classes', OffenceClassViewSet,
                base_name='offence-classes')
router.register(r'prices', PriceViewSet, base_name='prices')

schema_view = get_swagger_view(title='Calculator API')

urlpatterns = (
    url(r'^', include(router.urls)),
    url(r'^docs/$', schema_view),
    url(r'^calculate/$', CalculatorView.as_view(), name='calculator'),
)
