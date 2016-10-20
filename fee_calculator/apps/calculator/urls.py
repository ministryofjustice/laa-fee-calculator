# -*- coding: utf-8 -*-
from django.conf.urls import url, include

from rest_framework import routers

from scheme.views import BaseSchemeViewSet, SchemeViewSet


router = routers.DefaultRouter()
router.register(r'scheme', BaseSchemeViewSet, base_name='scheme')
router.register(r'scheme', SchemeViewSet, base_name='scheme-by-date')

urlpatterns = (
    url(r'^', include(router.urls)),
)
