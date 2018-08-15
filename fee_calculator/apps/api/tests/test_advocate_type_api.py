# -*- coding: utf-8 -*-
from django.conf import settings

from rest_framework import status
from rest_framework.test import APITestCase

from calculator.constants import SCHEME_TYPE
from calculator.models import Scheme


class AdvocateTypeApiTestCase(APITestCase):
    endpoint = '/api/{api}/fee-schemes/{{scheme}}/advocate-types/'.format(
        api=settings.API_VERSION
    )

    def test_get_list_available(self):
        for scheme_id in Scheme.objects.filter(
            base_type=SCHEME_TYPE.AGFS
        ).values_list('id', flat=True):
            response = self.client.get(self.endpoint.format(scheme=scheme_id))
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertGreater(len(response.data['results']), 0)

    def test_get_list_empty_for_lgfs(self):
        for scheme_id in Scheme.objects.filter(
            base_type=SCHEME_TYPE.LGFS
        ).values_list('id', flat=True):
            response = self.client.get(self.endpoint.format(scheme=scheme_id))
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(len(response.data['results']), 0)

    def test_get_detail_available(self):
        response = self.client.get(self.endpoint.format(scheme=1) + 'JRALONE/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_404_for_nonexistent_id(self):
        response = self.client.get(self.endpoint.format(scheme=1) + 'LAWMAN/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
