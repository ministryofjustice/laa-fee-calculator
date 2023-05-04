from django.test import TestCase
from api.utils import ModelParamFetcher
from rest_framework.test import APIRequestFactory
from rest_framework.exceptions import ValidationError
from calculator.models import AdvocateType, Scheme


class ModelParamFetcherTestCase(TestCase):
    @classmethod
    def setUp(cls):
        cls.factory = APIRequestFactory()

    def test_gets_none_for_missing_parameter(self):
        request = self.factory.get('/api')
        request.query_params = {}
        scheme = Scheme.objects.get(pk=10)
        fetcher = ModelParamFetcher(request, 'advocate_type', AdvocateType, scheme)

        self.assertIsNone(fetcher.call())

    def test_fetches_an_advocate_type(self):
        request = self.factory.get('/api')
        request.query_params = {'advocate_type': 'QC'}
        scheme = Scheme.objects.get(pk=10)
        qc = AdvocateType.objects.get(pk='QC')
        fetcher = ModelParamFetcher(request, 'advocate_type', AdvocateType, scheme)

        self.assertEqual(fetcher.call(), qc)

    def test_fetches_the_qc_advocate_type_for_kc_with_fee_scheme_14(self):
        request = self.factory.get('/api')
        request.query_params = {'advocate_type': 'KC'}
        scheme = Scheme.objects.get(pk=10)
        qc = AdvocateType.objects.get(pk='QC')
        fetcher = ModelParamFetcher(request, 'advocate_type', AdvocateType, scheme)

        self.assertEqual(fetcher.call(), qc)

    def test_fetches_the_kc_advocate_type_for_qc_with_fee_scheme_15(self):
        request = self.factory.get('/api')
        request.query_params = {'advocate_type': 'QC'}
        scheme = Scheme.objects.get(pk=11)
        kc = AdvocateType.objects.get(pk='KC')
        fetcher = ModelParamFetcher(request, 'advocate_type', AdvocateType, scheme)

        self.assertEqual(fetcher.call(), kc)

    def test_raises_exception_for_unknown_advocate_type(self):
        request = self.factory.get('/api')
        request.query_params = {'advocate_type': 'Unknown'}
        scheme = Scheme.objects.get(pk=10)
        fetcher = ModelParamFetcher(request, 'advocate_type', AdvocateType, scheme)

        self.assertRaises(ValidationError, fetcher.call)
