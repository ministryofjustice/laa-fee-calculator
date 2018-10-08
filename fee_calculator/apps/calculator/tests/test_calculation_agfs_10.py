# -*- coding: utf-8 -*-
import os

from calculator.tests.base import Agfs10PlusCalculatorTestCase, Agfs10PlusWarrantFeeTestMixin


class Agfs10CalculatorTestCase(Agfs10PlusCalculatorTestCase, Agfs10PlusWarrantFeeTestMixin):
    scheme_id = 3
    csv_path = os.path.join(
        os.path.dirname(__file__),
        'data/test_dataset_agfs_10.csv'
    )


Agfs10CalculatorTestCase.create_tests()
