from django.test import TestCase

from calculator.models import OffenceClass, Scenario
from viewer.factories import OffenceClassPresenterFactory, ScenarioPresenterFactory
from viewer.presenters.offence_class_presenters import (
    AlphaOffenceClassPresenter, NumericOffenceClassPresenter, NullOffenceClassPresenter, NoneOffenceClassPresenter)
from viewer.presenters.scenario_presenters import (ScenarioPresenter, NullScenarioPresenter, NoneScenarioPresenter)


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
