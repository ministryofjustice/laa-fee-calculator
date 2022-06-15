from django.test import TestCase
from calculator.models import Scheme


class IndexTestCase(TestCase):
    def test_display_index(self):
        response = self.client.get('/viewer/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'viewer/index.html')


class FeeSchemesTestCase(TestCase):
    def test_display_fee_scheme_list(self):
        response = self.client.get('/viewer/fee_schemes')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'viewer/fee_schemes.html')


class FeeSchemeTestCase(TestCase):
    def test_display_a_known_fee_scheme(self):
        Scheme.objects.create(id=9999, start_date='2022-06-15', base_type=1)
        response = self.client.get('/viewer/fee_schemes/9999')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'viewer/fee_scheme.html')

    def test_404_for_an_unkonwn_fee_scheme(self):
        response = self.client.get('/viewer/fee_schemes/9999')
        self.assertEqual(response.status_code, 404)


class ScenariosTestCase(TestCase):
    def test_display_scenario_list(self):
        response = self.client.get('/viewer/scenarios')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'viewer/scenarios.html')
