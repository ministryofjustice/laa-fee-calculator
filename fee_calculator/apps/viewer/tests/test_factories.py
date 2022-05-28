from django.test import TestCase

from calculator.models import OffenceClass
from viewer.factories import OffenceClassPresenterFactory
from viewer.presenters.offence_class_presenters import (
    AlphaOffenceClassPresenter, NumericOffenceClassPresenter, NullOffenceClassPresenter, NoneOffenceClassPresenter)


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
