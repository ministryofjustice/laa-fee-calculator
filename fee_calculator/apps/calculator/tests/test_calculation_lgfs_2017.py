# -*- coding: utf-8 -*-
import os

from calculator.tests.base import (
    LgfsCalculatorTestCase, EvidenceProvisionFeeTestMixin
)


class Lgfs2017CalculatorTestCase(
    LgfsCalculatorTestCase, EvidenceProvisionFeeTestMixin
):
    scheme_id = 4
    csv_path = os.path.join(
        os.path.dirname(__file__),
        'data/test_dataset_lgfs_2017.csv'
    )


Lgfs2017CalculatorTestCase.create_tests()
