# -*- coding: utf-8 -*-
from django.conf.urls import url, include

from rest_framework import routers

from scheme.views import BaseSchemeViewSet


router = routers.DefaultRouter()
router.register(r'scheme', BaseSchemeViewSet, base_name='scheme')

urlpatterns = (
    url(r'^', include(router.urls)),
)
