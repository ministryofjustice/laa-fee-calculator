# -*- coding: utf-8 -*-
from django.conf import settings

from rest_framework import status
from rest_framework.test import APITestCase


class SchemeApiTestCase(APITestCase):
    endpoint = '/api/%s/scheme/' % settings.API_VERSION
    fixtures = ['fee_calculator/apps/scheme/fixtures/initial_data.yaml']

    def _test_get_not_allowed(self, url):
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def _test_post_not_allowed(self, url, data={}):
        response = self.client.post(url, data,)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def _test_put_not_allowed(self, url, data={}):
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def _test_patch_not_allowed(self, url, data={}):
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def _test_delete_not_allowed(self, url):
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_get_list_available(self):
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 10)

    def test_get_detail_available(self):
        response = self.client.get('%s1/' % self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_by_date_available(self):
        response = self.client.get('%sadvocate/2011-04-02/' % self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], 8)

    def test_methods_not_allowed(self):
        for url in [self.endpoint, '%s1/' % self.endpoint,
                    '%sadvocate/2011-04-02/' % self.endpoint]:
            self._test_post_not_allowed(url)
            self._test_put_not_allowed(url)
            self._test_patch_not_allowed(url)
            self._test_delete_not_allowed(url)