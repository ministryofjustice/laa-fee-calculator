from django.test import TestCase

from calculator.models import OffenceClass
from viewer.presenters.offence_class_presenters import (
    AlphaOffenceClassPresenter, NumericOffenceClassPresenter, NoneOffenceClassPresenter, NullOffenceClassPresenter)


class AlphaOffenceClassPresenterTestCase(TestCase):
    @classmethod
    def setUp(self):
        self.offence_class = OffenceClass.objects.create(id='Q', name='Test Name', description='Test Description')

    def test_has_id_as_label(self):
        presenter = AlphaOffenceClassPresenter(self.offence_class, count=123)
        self.assertEqual(presenter.label, 'Q')

    def test_has_display_name_based_on_description_and_count(self):
        presenter = AlphaOffenceClassPresenter(self.offence_class, count=123)
        self.assertEqual(presenter.display_name, '[Q] Test Description (123)')

    def test_display_name_when_count_is_none(self):
        presenter = AlphaOffenceClassPresenter(self.offence_class, count=None)
        self.assertEqual(presenter.display_name, '[Q] Test Description')

    def test_display_name_when_count_is_omitted(self):
        presenter = AlphaOffenceClassPresenter(self.offence_class)
        self.assertEqual(presenter.display_name, '[Q] Test Description')

    def test_is_not_null(self):
        presenter = AlphaOffenceClassPresenter(self.offence_class)
        self.assertFalse(presenter.isNull)

    def test_alpha_offence_class_presenters_are_sortable(self):
        presenter1 = AlphaOffenceClassPresenter(OffenceClass.objects.get(id='C'))
        presenter2 = AlphaOffenceClassPresenter(OffenceClass.objects.get(id='F'))
        self.assertLess(presenter1, presenter2)
        self.assertGreater(presenter2, presenter1)

    def test_alpha_offence_class_presenters_is_less_than_a_numeric_offence_class_presenter(self):
        presenter1 = AlphaOffenceClassPresenter(OffenceClass.objects.get(id='A'))
        presenter2 = NumericOffenceClassPresenter(OffenceClass.objects.get(id='3.4'))
        self.assertLess(presenter1, presenter2)
        self.assertGreater(presenter2, presenter1)

    def test_offence_class_presenter_is_greater_than_none(self):
        presenter1 = AlphaOffenceClassPresenter(self.offence_class)
        presenter2 = NoneOffenceClassPresenter()
        self.assertLess(presenter2, presenter1)
        self.assertGreater(presenter1, presenter2)

    def test_offence_class_presenter_is_greater_than_null(self):
        presenter1 = AlphaOffenceClassPresenter(self.offence_class)
        presenter3 = NullOffenceClassPresenter()
        self.assertLess(presenter3, presenter1)
        self.assertGreater(presenter1, presenter3)

    def test_offence_class_presenters_are_equal_with_same_offence_class(self):
        presenter1 = AlphaOffenceClassPresenter(self.offence_class)
        presenter2 = AlphaOffenceClassPresenter(self.offence_class)
        self.assertEqual(presenter1, presenter2)


class NumericOffenceClassPresenterTestCase(TestCase):
    @classmethod
    def setUp(self):
        self.offence_class = OffenceClass.objects.create(id='20.5', name='Test Name', description='Test Description')

    def test_has_id_as_label(self):
        presenter = NumericOffenceClassPresenter(self.offence_class, count=123)
        self.assertEqual(presenter.label, '20.5')

    def test_has_display_name_based_on_name_and_count(self):
        presenter = NumericOffenceClassPresenter(self.offence_class, count=123)
        self.assertEqual(presenter.display_name, 'Test Name (123)')

    def test_display_name_when_count_is_none(self):
        presenter = NumericOffenceClassPresenter(self.offence_class, count=None)
        self.assertEqual(presenter.display_name, 'Test Name')

    def test_display_name_when_count_is_omitted(self):
        presenter = NumericOffenceClassPresenter(self.offence_class)
        self.assertEqual(presenter.display_name, 'Test Name')

    def test_is_not_null(self):
        presenter = NumericOffenceClassPresenter(self.offence_class)
        self.assertFalse(presenter.isNull)

    def test_alpha_offence_class_presenters_are_sortable(self):
        presenter1 = NumericOffenceClassPresenter(OffenceClass.objects.get(id='3.1'))
        presenter2 = NumericOffenceClassPresenter(OffenceClass.objects.get(id='3.4'))
        presenter3 = NumericOffenceClassPresenter(OffenceClass.objects.get(id='11.1'))
        self.assertLess(presenter1, presenter2)
        self.assertGreater(presenter2, presenter1)
        self.assertLess(presenter2, presenter3)
        self.assertGreater(presenter3, presenter2)

    def test_offence_class_presenter_is_greater_than_none(self):
        presenter1 = NumericOffenceClassPresenter(self.offence_class)
        presenter2 = NoneOffenceClassPresenter()
        self.assertLess(presenter2, presenter1)
        self.assertGreater(presenter1, presenter2)

    def test_offence_class_presenter_is_greater_than_null(self):
        presenter1 = NumericOffenceClassPresenter(self.offence_class)
        presenter2 = NullOffenceClassPresenter()
        self.assertLess(presenter2, presenter1)
        self.assertGreater(presenter1, presenter2)

    def test_offence_class_presenters_are_equal_with_same_offence_class(self):
        presenter1 = NumericOffenceClassPresenter(self.offence_class)
        presenter2 = NumericOffenceClassPresenter(self.offence_class)
        self.assertEqual(presenter1, presenter2)


class NoneOffenceClassPresenterTestCase(TestCase):
    def test_has_a_default_label(self):
        presenter = NoneOffenceClassPresenter(count=123)
        self.assertEqual(presenter.label, 'None')

    def test_has_a_default_display_name_including_count(self):
        presenter = NoneOffenceClassPresenter(count=123)
        self.assertEqual(presenter.display_name, '[None] (123)')

    def test_display_name_when_count_is_none(self):
        presenter = NoneOffenceClassPresenter(count=None)
        self.assertEqual(presenter.display_name, '[None]')

    def test_display_name_when_count_is_omitted(self):
        presenter = NoneOffenceClassPresenter()
        self.assertEqual(presenter.display_name, '[None]')

    def test_displays_default_id(self):
        presenter = NoneOffenceClassPresenter()
        self.assertEqual(presenter.id, 'None')

    def test_displays_default_name(self):
        presenter = NoneOffenceClassPresenter()
        self.assertEqual(presenter.name, '(None)')

    def test_displays_default_description(self):
        presenter = NoneOffenceClassPresenter()
        self.assertEqual(presenter.description, '(None)')

    def test_is_not_null(self):
        presenter = NoneOffenceClassPresenter()
        self.assertFalse(presenter.isNull)

    def test_none_offence_class_presenter_is_greater_than_null(self):
        presenter1 = NoneOffenceClassPresenter()
        presenter2 = NullOffenceClassPresenter()
        self.assertLess(presenter2, presenter1)
        self.assertGreater(presenter1, presenter2)

    def test_two_none_offence_class_presenters_are_equal(self):
        presenter1 = NoneOffenceClassPresenter()
        presenter2 = NoneOffenceClassPresenter()
        self.assertEqual(presenter1, presenter2)


class NullOffenceClassPresenterTestCase(TestCase):
    def test_has_a_default_label(self):
        presenter = NullOffenceClassPresenter(count=123)
        self.assertEqual(presenter.label, '')

    def test_has_a_default_display_name_including_count(self):
        presenter = NullOffenceClassPresenter(count=123)
        self.assertEqual(presenter.display_name, '-')

    def test_display_name_when_count_is_none(self):
        presenter = NullOffenceClassPresenter(count=None)
        self.assertEqual(presenter.display_name, '-')

    def test_display_name_when_count_is_omitted(self):
        presenter = NullOffenceClassPresenter()
        self.assertEqual(presenter.display_name, '-')

    def test_displays_default_id(self):
        presenter = NullOffenceClassPresenter()
        self.assertEqual(presenter.id, '-')

    def test_displays_default_name(self):
        presenter = NullOffenceClassPresenter()
        self.assertEqual(presenter.name, '-')

    def test_displays_default_description(self):
        presenter = NullOffenceClassPresenter()
        self.assertEqual(presenter.description, '-')

    def test_is_null(self):
        presenter = NullOffenceClassPresenter()
        self.assertTrue(presenter.isNull)

    def test_two_null_offence_class_presenters_are_equal(self):
        presenter1 = NullOffenceClassPresenter()
        presenter2 = NullOffenceClassPresenter()
        self.assertEqual(presenter1, presenter2)
