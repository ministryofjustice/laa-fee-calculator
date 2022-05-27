# -*- coding: utf-8 -*-

from django.urls import path

from . import views

app_name = 'viewer'
urlpatterns = [
    path('', views.index, name='index'),
    path('fee_schemes', views.fee_schemes, name='fee_schemes'),
    path('fee_schemes/<int:pk>', views.fee_scheme, name='fee_scheme')
]
