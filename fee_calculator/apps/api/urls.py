# -*- coding: utf-8 -*-
from django.conf.urls import url, include

from rest_framework import routers
from rest_framework_swagger.views import get_swagger_view

from calculator.views import BaseSchemeViewSet, SchemeViewSet


router = routers.DefaultRouter()
router.register(r'fee-schemes', BaseSchemeViewSet, base_name='fee-schemes')
router.register(r'fee-schemes', SchemeViewSet, base_name='fee-schemes')

schema_view = get_swagger_view(title='Calculator API')

urlpatterns = (
    url(r'^', include(router.urls)),
    url(r'^docs/$', schema_view)
)
