# -*- coding: utf-8 -*-
from django.conf import settings

from rest_framework import status
from rest_framework.test import APITestCase


class FeeTypeApiTestCase(APITestCase):
    endpoint = '/api/{api}/fee-schemes/{{scheme}}/fee-types/'.format(
        api=settings.API_VERSION
    )

    def test_get_list_available(self):
        response = self.client.get(self.endpoint.format(scheme=1))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data['results']), 0)

    def test_get_list_available_with_filters(self):
        response = self.client.get(
            self.endpoint.format(scheme=1) +
            '?offence_class=A&advocate_type=JRALONE&scenario=2'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data['results']), 0)

    def test_get_list_400_with_invalid_filter(self):
        response = self.client.get(
            self.endpoint.format(scheme=1) +
            '?offence_class=A&advocate_type=JRALONE&scenario=burps'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data[0], '\'burps\' is not a valid `scenario`')

    def test_get_list_400_with_nonexistent_filter(self):
        response = self.client.get(
            self.endpoint.format(scheme=1) +
            '?offence_class=Z&advocate_type=JRALONE&scenario=2'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data[0], '\'Z\' is not a valid `offence_class`')

    def test_get_detail_available(self):
        response = self.client.get(self.endpoint.format(scheme=1) + '7/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_404_for_fee_type_not_in_scheme(self):
        response = self.client.get(self.endpoint.format(scheme=2) + '7/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_404_for_nonexistent_id(self):
        response = self.client.get(self.endpoint.format(scheme=1) + '999999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
