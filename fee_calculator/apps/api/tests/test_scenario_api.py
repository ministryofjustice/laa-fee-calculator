# -*- coding: utf-8 -*-
from django.conf import settings

from rest_framework import status
from rest_framework.test import APITestCase


class ScenarioApiTestCase(APITestCase):
    endpoint = '/api/{api}/fee-schemes/{{scheme}}/scenarios/'.format(
        api=settings.API_VERSION
    )

    def test_get_list_available(self):
        response = self.client.get(self.endpoint.format(scheme=1))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data['results']), 0)

    def test_get_detail_available(self):
        response = self.client.get(self.endpoint.format(scheme=1) + '3/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_404_for_invalid_id(self):
        response = self.client.get(self.endpoint.format(scheme=1) + 'AS00001/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_404_for_nonexistent_id(self):
        response = self.client.get(self.endpoint.format(scheme=1) + '999999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
