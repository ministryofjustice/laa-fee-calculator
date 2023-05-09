from django.db.models import Q
from django.test import TestCase
from api.utils import ModelParamFetcher, q_builder_with_null, q_builder_with_list
from rest_framework.test import APIRequestFactory
from rest_framework.exceptions import ValidationError
from calculator.models import AdvocateType, Scheme, Scenario


class ModelParamFetcherTestCase(TestCase):
    @classmethod
    def setUp(cls):
        cls.factory = APIRequestFactory()

    def test_call_gets_none_for_missing_parameter(self):
        request = self.factory.get('/api')
        request.query_params = {}
        scheme = Scheme.objects.get(pk=10)
        fetcher = ModelParamFetcher(request, 'advocate_type', AdvocateType, scheme)

        self.assertIsNone(fetcher.call())

    def test_call_fetches_an_advocate_type(self):
        request = self.factory.get('/api')
        request.query_params = {'advocate_type': 'QC'}
        scheme = Scheme.objects.get(pk=10)
        qc = AdvocateType.objects.get(pk='QC')
        fetcher = ModelParamFetcher(request, 'advocate_type', AdvocateType, scheme)

        self.assertEqual(fetcher.call(), qc)

    def test_call_fetches_the_qc_advocate_type_for_kc_with_fee_scheme_14(self):
        request = self.factory.get('/api')
        request.query_params = {'advocate_type': 'KC'}
        scheme = Scheme.objects.get(pk=10)
        qc = AdvocateType.objects.get(pk='QC')
        fetcher = ModelParamFetcher(request, 'advocate_type', AdvocateType, scheme)

        self.assertEqual(fetcher.call(), qc)

    def test_call_fetches_the_kc_advocate_type_for_qc_with_fee_scheme_15(self):
        request = self.factory.get('/api')
        request.query_params = {'advocate_type': 'QC'}
        scheme = Scheme.objects.get(pk=11)
        kc = AdvocateType.objects.get(pk='KC')
        fetcher = ModelParamFetcher(request, 'advocate_type', AdvocateType, scheme)

        self.assertEqual(fetcher.call(), kc)

    def test_call_raises_exception_for_unknown_advocate_type(self):
        request = self.factory.get('/api')
        request.query_params = {'advocate_type': 'Unknown'}
        scheme = Scheme.objects.get(pk=10)
        fetcher = ModelParamFetcher(request, 'advocate_type', AdvocateType, scheme)

        self.assertRaises(ValidationError, fetcher.call)

    def test_as_q_returns_None_for_no_parameter(self):
        request = self.factory.get('/api')
        request.query_params = {'scenario': 4}
        scheme = Scheme.objects.get(pk=10)
        fetcher = ModelParamFetcher(request, 'advocate_type', AdvocateType, scheme)

        self.assertEqual(fetcher.as_q, None)

    def test_as_q_returns_single_Q_object(self):
        request = self.factory.get('/api')
        request.query_params = {'scenario': 4}
        scheme = Scheme.objects.get(pk=10)
        fetcher = ModelParamFetcher(request, 'scenario', Scenario, scheme)
        scenario = Scenario.objects.get(pk=4)

        self.assertEqual(fetcher.as_q, Q(scenario=scenario))

    def test_as_q_uses_q_builder_strategy(self):
        request = self.factory.get('/api')
        request.query_params = {'scenario': 4}
        scheme = Scheme.objects.get(pk=10)

        def q_builder(param, value):
            return 'Param is %s and Value is %s' % (param, value)
        fetcher = ModelParamFetcher(request, 'scenario', Scenario, scheme, q_builder=q_builder)

        self.assertEqual(fetcher.as_q, 'Param is scenario and Value is Trial')

    def test_present_is_True_when_param_present(self):
        request = self.factory.get('/api')
        request.query_params = {'scenario': 4}
        scheme = Scheme.objects.get(pk=10)
        fetcher = ModelParamFetcher(request, 'scenario', Scenario, scheme)

        self.assertTrue(fetcher.present)

    def test_present_is_False_when_param_is_not_present(self):
        request = self.factory.get('/api')
        request.query_params = {'scenario': 4}
        scheme = Scheme.objects.get(pk=10)
        fetcher = ModelParamFetcher(request, 'advocate_type', AdvocateType, scheme)

        self.assertFalse(fetcher.present)


class QBuilderWithNullTestCase(TestCase):
    def test_includes_an_isnull_option(self):
        self.assertEqual(q_builder_with_null('key', 'value'), Q(key='value') | Q(key__isnull=True))


class QBuilderWithListTestCase(TestCase):
    def test_includes_an_isnull_option(self):
        self.assertEqual(q_builder_with_list('key', ['value one', 'value two']), Q(key__in=['value one', 'value two']))
