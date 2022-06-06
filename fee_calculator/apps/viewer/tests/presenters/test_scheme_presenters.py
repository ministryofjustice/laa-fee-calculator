from django.test import TestCase

from calculator.models import Scheme
from viewer.presenters.scheme_presenters import SchemePresenter


class SchemePresenterTestCase(TestCase):
    @classmethod
    def setUp(self):
        self.default_kwargs = {'base_type': 1, 'start_date': '2022-03-05'}
        self.presenter_options = {}

    def test_base_type_agfs(self):
        self.default_kwargs['base_type'] = 1
        scenario = Scheme.objects.create(**self.default_kwargs)
        presenter = SchemePresenter(scenario, **self.presenter_options)
        self.assertEqual(presenter.base_type, 'AGFS')

    def test_base_type_lgfs(self):
        self.default_kwargs['base_type'] = 2
        scenario = Scheme.objects.create(**self.default_kwargs)
        presenter = SchemePresenter(scenario, **self.presenter_options)
        self.assertEqual(presenter.base_type, 'LGFS')
