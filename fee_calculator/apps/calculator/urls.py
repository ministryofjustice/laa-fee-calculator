# -*- coding: utf-8 -*-
from django.conf.urls import url, include

from rest_framework import routers
from rest_framework_swagger.views import get_swagger_view

from scheme.views import BaseSchemeViewSet, SchemeViewSet


router = routers.DefaultRouter()
router.register(r'schemes', BaseSchemeViewSet, base_name='schemes')
router.register(r'schemes', SchemeViewSet, base_name='schemes-by-date')

schema_view = get_swagger_view(title='Calculator API')

urlpatterns = (
    url(r'^', include(router.urls)),
    url(r'^docs/$', schema_view)
)
