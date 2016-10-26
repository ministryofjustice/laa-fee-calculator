# -*- coding: utf-8 -*-
"""
filters
"""
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.compat import coreapi


def swagger_filter_backend_class(api_doc):

    class SwaggerFilterBackend(DjangoFilterBackend):

        def get_schema_fields(self, view):
            # Field definition
            # Field = namedtuple(
            # 'Field', ['name', 'required', 'location', 'type', 'description']
            # )
            keys = ('name', 'required', 'location', 'type', 'description')
            return [coreapi.Field(**{name: value for name, value
                                     in field.items() if name in keys})
                    for field in api_doc]

    return SwaggerFilterBackend
