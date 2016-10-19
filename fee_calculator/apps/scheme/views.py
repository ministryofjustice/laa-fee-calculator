# -*- coding: utf-8 -*-
from datetime import datetime

from django.db.models import Q
from django.http import Http404

from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from .constants import SUTY_BASE_TYPE
from .models import Scheme
from .serializers import SchemeSerializer


class BaseSchemeViewSet(viewsets.ReadOnlyModelViewSet):
    model = Scheme
    serializer_class = SchemeSerializer
    lookup_field = 'suty'

    def get_queryset(self):
        return self.model.objects.all()

    @detail_route(url_path='(?P<case_date>[0-9-]+)')
    def get_by_date(self, request, suty=None, case_date=None):
        try:
            case_date = datetime.strptime(case_date, '%Y-%m-%d')
        except ValueError:
            raise Http404

        queryset = self.filter_queryset(self.get_queryset()).filter(
            Q(end_date__isnull=True) | Q(end_date__gte=case_date),
            suty_base_type=SUTY_BASE_TYPE.for_constant(suty.upper()).value,
            start_date__lte=case_date,
        )

        try:
            scheme = queryset.get()
        except Scheme.DoesNotExist:
            raise Http404

        return Response(scheme)
