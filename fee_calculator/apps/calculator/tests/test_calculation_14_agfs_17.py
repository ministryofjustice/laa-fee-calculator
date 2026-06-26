# -*- coding: utf-8 -*-
import os

from calculator.tests.base import Agfs10PlusCalculatorTestCase, Agfs10PlusWarrantFeeTestMixin


class Agfs17CalculatorTestCase(Agfs10PlusCalculatorTestCase, Agfs10PlusWarrantFeeTestMixin):
    scheme_id = 14
    # THIS IS AUTO GENERATED TEST DATA, NOT REAL WORLD
    csv_path = os.path.join(
        os.path.dirname(__file__),
        'data/test_dataset_agfs_17.csv'
    )


Agfs17CalculatorTestCase.create_tests()
