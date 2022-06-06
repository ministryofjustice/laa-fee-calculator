from django.test import TestCase

from calculator.models import Scheme, OffenceClass, Scenario
from viewer.factories import SchemePresenterFactory, OffenceClassPresenterFactory, ScenarioPresenterFactory
from viewer.presenters.offence_class_presenters import (
    AlphaOffenceClassPresenter, NumericOffenceClassPresenter, NullOffenceClassPresenter, NoneOffenceClassPresenter)
from viewer.presenters.scenario_presenters import (
    ScenarioPresenter, InterimScenarioPresenter, WarrantScenarioPresenter, NullScenarioPresenter, NoneScenarioPresenter)
from viewer.presenters.scheme_presenters import SchemePresenter


class SchemePresenterFactoryTestCase(TestCase):
    @classmethod
    def setUp(self):
        self.factory = SchemePresenterFactory()
        self.options = {}

    def test_creates_scheme_presenter_from_pk(self):
        self.assertIsInstance(self.factory.build_from_pk(1, params=self.options), SchemePresenter)

    def test_with_no_selected_offence_class(self):
        presenter = self.factory.build_from_pk(1, params=self.options)
        self.assertIsInstance(presenter.selected_offence_class, NullOffenceClassPresenter)

    def test_with_selected_offence_class(self):
        self.options['offence_class'] = 'A'
        presenter = self.factory.build_from_pk(1, params=self.options)
        self.assertIsInstance(presenter.selected_offence_class, AlphaOffenceClassPresenter)
        self.assertEqual(presenter.selected_offence_class.label, 'A')

    def test_with_no_selected_scenario(self):
        presenter = self.factory.build_from_pk(1, params=self.options)
        self.assertIsInstance(presenter.selected_scenario, NullScenarioPresenter)

    def test_with_selected_scenario(self):
        self.options['scenario'] = '1'
        presenter = self.factory.build_from_pk(1, params=self.options)
        self.assertIsInstance(presenter.selected_scenario, ScenarioPresenter)
        self.assertEqual(presenter.selected_scenario.label, '1')


class OffenceClassPresenterFactoryTestCase(TestCase):
    @classmethod
    def setUp(self):
        self.factory = OffenceClassPresenterFactory()

    def test_creates_none_presenter_for_none_offence_class(self):
        self.assertIsInstance(self.factory.build('None'), NoneOffenceClassPresenter)

    def test_creates_none_presenter_for_id_none(self):
        self.assertIsInstance(self.factory.build(None), NoneOffenceClassPresenter)

    def test_creates_null_presenter_for_blank_id(self):
        self.assertIsInstance(self.factory.build(''), NullOffenceClassPresenter)

    def test_creates_alpha_presenter_for_known_offence_class(self):
        OffenceClass.objects.create(id='M')
        presenter = self.factory.build('M')
        self.assertIsInstance(presenter, AlphaOffenceClassPresenter)
        self.assertEqual(presenter.label, 'M')

    def test_creates_numeric_presenter_for_known_offence_class(self):
        OffenceClass.objects.create(id='50.5')
        presenter = self.factory.build('50.5')
        self.assertIsInstance(presenter, NumericOffenceClassPresenter)
        self.assertEqual(presenter.label, '50.5')


class ScenarioPresenterFactoryTestCase(TestCase):
    @classmethod
    def setUp(self):
        self.factory = ScenarioPresenterFactory()

    def test_creates_none_presenter_for_id_none_as_string(self):
        self.assertIsInstance(self.factory.build('None'), NoneScenarioPresenter)

    def test_creates_none_presenter_for_id_none(self):
        self.assertIsInstance(self.factory.build(None), NoneScenarioPresenter)

    def test_creates_null_presenter_for_blank_id_string(self):
        self.assertIsInstance(self.factory.build(''), NullScenarioPresenter)

    def test_creates_presenter_for_known_scenario(self):
        Scenario.objects.create(pk=99999)
        presenter = self.factory.build(99999)
        self.assertIsInstance(presenter, ScenarioPresenter)
        self.assertEqual(presenter.label, '99999')

    def test_creates_presenter_for_known_scenario_with_a_string(self):
        Scenario.objects.create(pk=99999)
        presenter = self.factory.build('99999')
        self.assertIsInstance(presenter, ScenarioPresenter)
        self.assertEqual(presenter.label, '99999')

    def test_create_from_scenario_for_simple_name(self):
        trial_scenario = Scenario.objects.get(name='Trial')
        self.assertIsInstance(self.factory.build_from_scenario(trial_scenario), ScenarioPresenter)
        retrial_scenario = Scenario.objects.get(name='Retrial')
        self.assertIsInstance(self.factory.build_from_scenario(retrial_scenario), ScenarioPresenter)

    def test_create_from_scenario_for_interim(self):
        scenario = Scenario.objects.get(name='Interim payment - trial start')
        self.assertIsInstance(self.factory.build_from_scenario(scenario), InterimScenarioPresenter)

    def test_create_from_scenario_for_warrant(self):
        scenario = Scenario.objects.get(name='Warrant issued - trial')
        self.assertIsInstance(self.factory.build_from_scenario(scenario), WarrantScenarioPresenter)
