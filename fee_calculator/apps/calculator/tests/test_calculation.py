# -*- coding: utf-8 -*-
from django.test import TestCase


class CalculatorTestCase(TestCase):
    fixtures = [
        'advocatetypes', 'feetype', 'offenceclass', 'price', 'scenario',
        'scheme', 'unit',
    ]

    def test_calculations_from_data(self):
        """
        load data from excel and chack calculations
        """
        pass
