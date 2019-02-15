# -*- coding: utf-8 -*-
from django.conf import settings

from rest_framework import status
from rest_framework.test import APITestCase

from calculator.models import Scheme
from calculator.tests.lib.utils import prevent_request_warnings


class UnitApiTestCase(APITestCase):
    endpoint = '/api/{api}/fee-schemes/{{scheme}}/units/'.format(
        api=settings.API_VERSION
    )

    def test_get_list_available(self):
        for scheme_id in Scheme.objects.all().values_list('id', flat=True):
            response = self.client.get(self.endpoint.format(scheme=scheme_id))
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertGreater(len(response.data['results']), 0)

    def test_get_list_available_with_filters(self):
        response = self.client.get(
            self.endpoint.format(scheme=1) +
            '?offence_class=A&advocate_type=JRALONE&scenario=2&fee_type_code=AGFS_FEE'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data['results']), 0)

    @prevent_request_warnings
    def test_get_list_400_with_invalid_scenario(self):
        response = self.client.get(
            self.endpoint.format(scheme=1) +
            '?offence_class=A&advocate_type=JRALONE&scenario=burps&fee_type_code=AGFS_FEE'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data[0], '\'burps\' is not a valid `scenario`')

    @prevent_request_warnings
    def test_get_list_400_with_nonexistent_offence_class(self):
        response = self.client.get(
            self.endpoint.format(scheme=1) +
            '?offence_class=Z&advocate_type=JRALONE&scenario=2&fee_type_code=AGFS_FEE'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data[0], '\'Z\' is not a valid `offence_class`')

    @prevent_request_warnings
    def test_get_list_400_with_nonexistent_fee_type(self):
        response = self.client.get(
            self.endpoint.format(scheme=1) +
            '?offence_class=A&advocate_type=JRALONE&scenario=2&fee_type_code=AGFS_BURP'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data[0], '\'AGFS_BURP\' is not a valid `fee_type_code`')

    def test_get_detail_available(self):
        response = self.client.get(self.endpoint.format(scheme=1) + 'DAY/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @prevent_request_warnings
    def test_404_for_fee_type_not_in_scheme(self):
        response = self.client.get(self.endpoint.format(scheme=2) + 'PW/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @prevent_request_warnings
    def test_404_for_nonexistent_id(self):
        response = self.client.get(self.endpoint.format(scheme=1) + 'AEON/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
