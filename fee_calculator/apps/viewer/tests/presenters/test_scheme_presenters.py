from django.test import TestCase

from calculator.models import Scheme
from viewer.presenters.scheme_presenters import SchemePresenter


class SchemePresenterTestCase(TestCase):
    @classmethod
    def setUp(self):
        self.default_kwargs = {'start_date': '2022-03-05'}

    def test_base_type_agfs(self):
        scenario = Scheme.objects.create(base_type=1, **self.default_kwargs)
        presenter = SchemePresenter(scenario)
        self.assertEqual(presenter.base_type, 'AGFS')

    def test_base_type_lgfs(self):
        scenario = Scheme.objects.create(base_type=2, **self.default_kwargs)
        presenter = SchemePresenter(scenario)
        self.assertEqual(presenter.base_type, 'LGFS')
