# -*- coding: utf-8 -*-
from django.conf import settings

from rest_framework import status
from rest_framework.test import APITestCase


class OffenceClassApiTestCase(APITestCase):
    endpoint = '/api/{api}/fee-schemes/{{scheme}}/offence-classes/'.format(
        api=settings.API_VERSION
    )

    def test_get_list_available_1(self):
        response = self.client.get(self.endpoint.format(scheme=1))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data['results']), 0)

    def test_get_list_available_2(self):
        response = self.client.get(self.endpoint.format(scheme=2))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data['results']), 0)

    def test_get_detail_available_1(self):
        response = self.client.get(self.endpoint.format(scheme=1) + 'A/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_detail_available_2(self):
        response = self.client.get(self.endpoint.format(scheme=3) + '1.2/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_404_for_nonexistent_id(self):
        response = self.client.get(self.endpoint.format(scheme=1) + 'Z/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
