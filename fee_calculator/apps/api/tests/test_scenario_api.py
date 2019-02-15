# -*- coding: utf-8 -*-
from django.conf import settings

from rest_framework import status
from rest_framework.test import APITestCase

from calculator.models import Scheme
from calculator.tests.lib.utils import prevent_request_warnings


class ScenarioApiTestCase(APITestCase):
    endpoint = '/api/{api}/fee-schemes/{{scheme}}/scenarios/'.format(
        api=settings.API_VERSION
    )

    def test_get_list_available(self):
        for scheme_id in Scheme.objects.all().values_list('id', flat=True):
            response = self.client.get(self.endpoint.format(scheme=scheme_id))
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertGreater(len(response.data['results']), 0)

    def test_get_detail_available(self):
        response = self.client.get(self.endpoint.format(scheme=1) + '3/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @prevent_request_warnings
    def test_404_for_invalid_id(self):
        response = self.client.get(self.endpoint.format(scheme=1) + 'AS00001/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @prevent_request_warnings
    def test_404_for_nonexistent_id(self):
        response = self.client.get(self.endpoint.format(scheme=1) + '999999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
