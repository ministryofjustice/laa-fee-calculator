from django.test import TestCase

from calculator.models import Scenario
from viewer.presenters.scenario_presenters import (ScenarioPresenter, NoneScenarioPresenter, NullScenarioPresenter)


class ScenarioPresenterTestCase(TestCase):
    @classmethod
    def setUp(self):
        self.scenario = Scenario.objects.create(pk=99999, name='Test Name')

    def test_has_pk_as_label(self):
        presenter = ScenarioPresenter(self.scenario, count=123)
        self.assertEqual(presenter.label, '99999')

    def test_has_display_name_based_on_name_and_count(self):
        presenter = ScenarioPresenter(self.scenario, count=123)
        self.assertEqual(presenter.display_name, 'Test Name (123)')

    def test_display_name_when_count_is_none(self):
        presenter = ScenarioPresenter(self.scenario, count=None)
        self.assertEqual(presenter.display_name, 'Test Name')

    def test_display_name_when_count_is_omitted(self):
        presenter = ScenarioPresenter(self.scenario)
        self.assertEqual(presenter.display_name, 'Test Name')

    def test_is_not_null(self):
        presenter = ScenarioPresenter(self.scenario)
        self.assertFalse(presenter.isNull)


class NoneScenarioPresenterTestCase(TestCase):
    def test_has_pk_as_label(self):
        presenter = NoneScenarioPresenter(count=123)
        self.assertEqual(presenter.label, 'None')

    def test_has_display_name_based_on_name_and_count(self):
        presenter = NoneScenarioPresenter(count=123)
        self.assertEqual(presenter.display_name, '[None] (123)')

    def test_display_name_when_count_is_none(self):
        presenter = NoneScenarioPresenter(count=None)
        self.assertEqual(presenter.display_name, '[None]')

    def test_display_name_when_count_is_omitted(self):
        presenter = NoneScenarioPresenter()
        self.assertEqual(presenter.display_name, '[None]')

    def test_is_not_null(self):
        presenter = NoneScenarioPresenter()
        self.assertFalse(presenter.isNull)


class NullScenarioPresenterTestCase(TestCase):
    def test_has_pk_as_label(self):
        presenter = NullScenarioPresenter(count=123)
        self.assertEqual(presenter.label, '')

    def test_has_display_name_based_on_name_and_count(self):
        presenter = NullScenarioPresenter(count=123)
        self.assertEqual(presenter.display_name, '-')

    def test_display_name_when_count_is_none(self):
        presenter = NullScenarioPresenter(count=None)
        self.assertEqual(presenter.display_name, '-')

    def test_display_name_when_count_is_omitted(self):
        presenter = NullScenarioPresenter()
        self.assertEqual(presenter.display_name, '-')

    def test_is_null(self):
        presenter = NullScenarioPresenter()
        self.assertTrue(presenter.isNull)
