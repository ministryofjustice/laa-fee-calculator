# -*- coding: utf-8 -*-
import os

from calculator.tests.base import (
    LgfsCalculatorTestCase, EvidenceProvisionFeeTestMixin
)


class Lgfs2016CalculatorTestCase(
    LgfsCalculatorTestCase, EvidenceProvisionFeeTestMixin
):
    scheme_id = 2
    csv_path = os.path.join(
        os.path.dirname(__file__),
        'data/test_dataset_lgfs_2016.csv'
    )


Lgfs2016CalculatorTestCase.create_tests()