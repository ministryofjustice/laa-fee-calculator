from django.test import TestCase

from calculator.models import Scenario
from viewer.presenters.scenario_presenters import (
    scenario_presenter_factory,
    scenario_presenter_factory_from_pk,
    ScenarioPresenter,
    InterimScenarioPresenter,
    WarrantScenarioPresenter,
    NoneScenarioPresenter,
    NullScenarioPresenter
)


class ScenarioPresenterFactoryTestCase(TestCase):
    def test_creates_none_presenter_for_id_none_as_string(self):
        self.assertIsInstance(scenario_presenter_factory_from_pk('None'),
                              NoneScenarioPresenter)

    def test_creates_none_presenter_for_id_none(self):
        self.assertIsInstance(scenario_presenter_factory_from_pk(None), NoneScenarioPresenter)

    def test_creates_null_presenter_for_blank_id_string(self):
        self.assertIsInstance(scenario_presenter_factory_from_pk(''), NullScenarioPresenter)

    def test_creates_presenter_for_known_scenario(self):
        Scenario.objects.create(pk=99999)
        presenter = scenario_presenter_factory_from_pk(99999)
        self.assertIsInstance(presenter, ScenarioPresenter)
        self.assertEqual(presenter.label, '99999')

    def test_creates_presenter_for_known_scenario_with_a_string(self):
        Scenario.objects.create(pk=99999)
        presenter = scenario_presenter_factory_from_pk('99999')
        self.assertIsInstance(presenter, ScenarioPresenter)
        self.assertEqual(presenter.label, '99999')

    def test_create_from_scenario_for_simple_name(self):
        trial_scenario = Scenario.objects.get(name='Trial')
        self.assertIsInstance(scenario_presenter_factory(trial_scenario), ScenarioPresenter)
        retrial_scenario = Scenario.objects.get(name='Retrial')
        self.assertIsInstance(scenario_presenter_factory(retrial_scenario), ScenarioPresenter)

    def test_create_from_scenario_for_interim(self):
        scenario = Scenario.objects.get(name='Interim payment - trial start')
        self.assertIsInstance(scenario_presenter_factory(scenario), InterimScenarioPresenter)

    def test_create_from_scenario_for_warrant(self):
        scenario = Scenario.objects.get(name='Warrant issued - trial')
        self.assertIsInstance(scenario_presenter_factory(scenario), WarrantScenarioPresenter)


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

    def test_case_type_is_name(self):
        presenter = ScenarioPresenter(self.scenario)
        self.assertEqual(presenter.case_type, 'Test Name')


class InterimScenarioPresenterTestCase(TestCase):
    @classmethod
    def setUp(self):
        self.scenario = Scenario.objects.create(pk=99999, name='Interim payment - trial start')

    def test_has_pk_as_label(self):
        presenter = InterimScenarioPresenter(self.scenario, count=123)
        self.assertEqual(presenter.label, '99999')

    def test_has_display_name_based_on_name_and_count(self):
        presenter = InterimScenarioPresenter(self.scenario, count=123)
        self.assertEqual(presenter.display_name, 'Interim payment - trial start (123)')

    def test_display_name_when_count_is_none(self):
        presenter = InterimScenarioPresenter(self.scenario, count=None)
        self.assertEqual(presenter.display_name, 'Interim payment - trial start')

    def test_display_name_when_count_is_omitted(self):
        presenter = InterimScenarioPresenter(self.scenario)
        self.assertEqual(presenter.display_name, 'Interim payment - trial start')

    def test_is_not_null(self):
        presenter = InterimScenarioPresenter(self.scenario)
        self.assertFalse(presenter.isNull)

    # def test_case_type_for_effective_pcmh(self):
    #     scenario = Scenario.objects.create(pk=99998, name='Interim payment - effective PCMH')
    #     presenter = InterimScenarioPresenter(scenario)
    #     self.assertEqual(presenter.case_type, 'Trial')

    def test_case_type_for_trial_start(self):
        scenario = Scenario.objects.create(pk=99998, name='Interim payment - trial start')
        presenter = InterimScenarioPresenter(scenario)
        self.assertEqual(presenter.case_type, 'Trial')

    def test_case_type_for_retrial_new_solicitor(self):
        scenario = Scenario.objects.create(pk=99998, name='Interim payment - retrial (new solicitor)')
        presenter = InterimScenarioPresenter(scenario)
        self.assertEqual(presenter.case_type, 'Retrial')

    def test_case_type_for_retrial_start(self):
        scenario = Scenario.objects.create(pk=99998, name='Interim payment - retrial start')
        presenter = InterimScenarioPresenter(scenario)
        self.assertEqual(presenter.case_type, 'Retrial')


class WarrantScenarioPresenterTestCase(TestCase):
    @classmethod
    def setUp(self):
        self.scenario = Scenario.objects.create(pk=99999, name='Warrant issued - trial')

    def test_has_pk_as_label(self):
        presenter = WarrantScenarioPresenter(self.scenario, count=123)
        self.assertEqual(presenter.label, '99999')

    def test_has_display_name_based_on_name_and_count(self):
        presenter = WarrantScenarioPresenter(self.scenario, count=123)
        self.assertEqual(presenter.display_name, 'Warrant issued - trial (123)')

    def test_display_name_when_count_is_none(self):
        presenter = WarrantScenarioPresenter(self.scenario, count=None)
        self.assertEqual(presenter.display_name, 'Warrant issued - trial')

    def test_display_name_when_count_is_omitted(self):
        presenter = WarrantScenarioPresenter(self.scenario)
        self.assertEqual(presenter.display_name, 'Warrant issued - trial')

    def test_is_not_null(self):
        presenter = WarrantScenarioPresenter(self.scenario)
        self.assertFalse(presenter.isNull)

    def test_case_type_for_trial(self):
        scenario = Scenario.objects.create(pk=99998, name='Warrant issued - trial (after plea hearing)')
        presenter = WarrantScenarioPresenter(scenario)
        self.assertEqual(presenter.case_type, 'Trial')

    def test_case_type_for_appeal_against_conviction(self):
        scenario = Scenario.objects.create(pk=99998, name='Warrant issued - appeal against conviction')
        presenter = WarrantScenarioPresenter(scenario)
        self.assertEqual(presenter.case_type, 'Appeal against conviction')

    def test_case_type_for_appeal_against_sentence(self):
        scenario = Scenario.objects.create(pk=99998, name='Warrant issued - appeal against sentence')
        presenter = WarrantScenarioPresenter(scenario)
        self.assertEqual(presenter.case_type, 'Appeal against sentence')

    def test_case_type_for_commital_for_sentence(self):
        scenario = Scenario.objects.create(pk=99998, name='Warrant issued - commital for sentence')
        presenter = WarrantScenarioPresenter(scenario)
        self.assertEqual(presenter.case_type, 'Commital for sentence')

    def test_case_type_for_breach_of_crown_court_order(self):
        scenario = Scenario.objects.create(pk=99998, name='Warrant issued - breach of crown court order')
        presenter = WarrantScenarioPresenter(scenario)
        self.assertEqual(presenter.case_type, 'Breach of crown court order')

    def test_case_type_for_retrial(self):
        scenario = Scenario.objects.create(pk=99998, name='Warrant issued - retrial (after trial start)')
        presenter = WarrantScenarioPresenter(scenario)
        self.assertEqual(presenter.case_type, 'Retrial')


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

    def test_case_type_is_none(self):
        presenter = NoneScenarioPresenter()
        self.assertEqual(presenter.case_type, '[None]')


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

    def test_case_type_is_blank(self):
        presenter = NullScenarioPresenter()
        self.assertEqual(presenter.case_type, '-')
