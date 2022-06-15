from django.test import TestCase

from calculator.models import Scheme
from viewer.presenters.scheme_presenters import scheme_presenter_factory_from_pk, SchemePresenter
from viewer.presenters.offence_class_presenters import NullOffenceClassPresenter, AlphaOffenceClassPresenter
from viewer.presenters.scenario_presenters import NullScenarioPresenter, ScenarioPresenter


class SchemePresenterFactoryTestCase(TestCase):
    @classmethod
    def setUp(self):
        self.options = {}

    def test_creates_scheme_presenter_from_pk(self):
        self.assertIsInstance(scheme_presenter_factory_from_pk(1, params=self.options), SchemePresenter)

    def test_with_no_selected_offence_class(self):
        presenter = scheme_presenter_factory_from_pk(1, params=self.options)
        self.assertIsInstance(presenter.selected_offence_class, NullOffenceClassPresenter)

    def test_with_selected_offence_class(self):
        self.options['offence_class'] = 'A'
        presenter = scheme_presenter_factory_from_pk(1, params=self.options)
        self.assertIsInstance(presenter.selected_offence_class, AlphaOffenceClassPresenter)
        self.assertEqual(presenter.selected_offence_class.label, 'A')

    def test_with_no_selected_scenario(self):
        presenter = scheme_presenter_factory_from_pk(1, params=self.options)
        self.assertIsInstance(presenter.selected_scenario, NullScenarioPresenter)

    def test_with_selected_scenario(self):
        self.options['scenario'] = '1'
        presenter = scheme_presenter_factory_from_pk(1, params=self.options)
        self.assertIsInstance(presenter.selected_scenario, ScenarioPresenter)
        self.assertEqual(presenter.selected_scenario.label, '1')


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
