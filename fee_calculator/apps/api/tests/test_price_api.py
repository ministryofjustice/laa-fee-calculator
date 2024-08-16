# -*- coding: utf-8 -*-
from django.conf import settings

from rest_framework import status
from rest_framework.test import APITestCase

from calculator.tests.lib.utils import prevent_request_warnings


class PriceApiTestCase(APITestCase):
    endpoint = '/api/{api}/fee-schemes/{{scheme}}/prices/'.format(
        api=settings.API_VERSION
    )

    def test_get_list_available_with_filters(self):
        response = self.client.get(
            self.endpoint.format(scheme=1) +
            '?offence_class=A&advocate_type=JRALONE&scenario=2&fee_type_code=AGFS_FEE&day=1'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data['results']), 0)

    def test_get_list_available_with_london_rates_apply_true(self):
        response = self.client.get(
            self.endpoint.format(scheme=2) +
            '?london_rates_apply=true'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data['results']), 0)

    def test_get_list_available_with_london_rates_apply_false(self):
        response = self.client.get(
            self.endpoint.format(scheme=2) +
            '?london_rates_apply=false'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data['results']), 0)

    @prevent_request_warnings
    def test_get_list_400_with_invalid_scenario(self):
        response = self.client.get(
            self.endpoint.format(scheme=1) +
            '?offence_class=A&advocate_type=JRALONE&scenario=burps&fee_type_code=AGFS_FEE&day=1'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @prevent_request_warnings
    def test_get_list_400_with_nonexistent_offence_class(self):
        response = self.client.get(
            self.endpoint.format(scheme=1) +
            '?offence_class=Z&advocate_type=JRALONE&scenario=2&fee_type_code=AGFS_FEE&day=1'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
