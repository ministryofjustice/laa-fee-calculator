# -*- coding: utf-8 -*-
from django.conf import settings

from rest_framework import status
from rest_framework.test import APITestCase

from calculator.tests.lib.utils import prevent_request_warnings


class SchemeApiTestCase(APITestCase):
    endpoint = '/api/{api}/fee-schemes/'.format(api=settings.API_VERSION)

    def test_get_list_available(self):
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data['results']), 0)

    def test_get_detail_available(self):
        response = self.client.get('%s1/' % self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @prevent_request_warnings
    def test_returns_404_for_nonexistent_id(self):
        response = self.client.get('%s9999/' % self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @prevent_request_warnings
    def test_returns_404_for_invalid_id(self):
        response = self.client.get('%sburps/' % self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_by_date_available(self):
        response = self.client.get('%s?type=AGFS&case_date=2012-04-02' % self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['id'], 1)

    def test_get_by_date_available_agfs_12_no_hearing_date(self):
        response = self.client.get('%s?type=AGFS&case_date=2020-09-17' % self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['id'], 5)  # 5 = AGFS Fee Scheme 12 - CLAR accelerated measures

    def test_get_by_date_available_agfs_12_with_main_hearing_date(self):
        response = self.client.get('%s?type=AGFS&case_date=2020-09-17&main_hearing_date=2022-09-29' % self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['id'], 5)  # 5 = AGFS Fee Scheme 12 - CLAR accelerated measures

    def test_get_by_date_available_agfs_12a(self):
        response = self.client.get('%s?type=AGFS&case_date=2020-09-17&main_hearing_date=2022-09-30' % self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['id'], 9)  # 9 = AGFS Fee Scheme 12a - CLAIR contingency

    @prevent_request_warnings
    def test_400_on_invalid_date(self):
        response = self.client.get('%s?type=AGFS&case_date=4thJanuary2015' % self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
