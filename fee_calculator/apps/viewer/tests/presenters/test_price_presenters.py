from django.test import TestCase

from calculator.models import Price, AdvocateType, OffenceClass, FeeType, Scenario, Scheme, Unit
from viewer.presenters.price_presenters import (price_presenter_factory, PricePresenter)


class PricePresenterFactoryTestCase(TestCase):
    @classmethod
    def setUp(self):
        self.options = {
            'advocate_type': AdvocateType.objects.create(),
            'offence_class': OffenceClass.objects.create(),
            'fee_type': FeeType.objects.create(is_basic=True),
            'fee_per_unit': 1.0,
            'fixed_fee': 1.0,
            'unit': Unit.objects.create(),
            'scenario': Scenario.objects.create(),
            'scheme': Scheme.objects.create(start_date='2022-05-05', base_type=1)
        }

    def test_creates_presenter_for_known_price(self):
        self.options['pk'] = 99999
        Price.objects.create(**self.options)
        presenter = price_presenter_factory(99999)
        self.assertIsInstance(presenter, PricePresenter)


class PricePresenterTestCase(TestCase):
    @classmethod
    def setUp(self):
        self.options = {
            'advocate_type': AdvocateType.objects.create(),
            'offence_class': OffenceClass.objects.create(),
            'fee_type': FeeType.objects.create(is_basic=True),
            'fee_per_unit': 1.0,
            'fixed_fee': 1.0,
            'unit': Unit.objects.create(),
            'scenario': Scenario.objects.create(),
            'scheme': Scheme.objects.create(start_date='2022-05-05', base_type=1)
        }

    def test_default_display_title(self):
        self.options['advocate_type'] = AdvocateType.objects.create(id=9999, name='Test Advocate')
        self.options['offence_class'] = OffenceClass.objects.create(id=9999, name='Test Offence')
        self.options['fee_type'] = FeeType.objects.create(name='Test Fee', is_basic=True)
        price = Price.objects.create(**self.options)
        presenter = PricePresenter(price)
        self.assertEqual(presenter.title(), 'Test Advocate | Test Offence | Test Fee')
