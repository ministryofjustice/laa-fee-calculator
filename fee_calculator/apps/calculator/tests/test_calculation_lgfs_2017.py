# -*- coding: utf-8 -*-
import os

from calculator.tests.base import (
    LgfsCalculatorTestCase, EvidenceProvisionFeeTestMixin, LgfsWarrantFeeTestMixin
)


class Lgfs2017CalculatorTestCase(
    LgfsCalculatorTestCase, EvidenceProvisionFeeTestMixin, LgfsWarrantFeeTestMixin
):
    scheme_id = 4
    csv_path = os.path.join(
        os.path.dirname(__file__),
        'data/test_dataset_lgfs_2017.csv'
    )


Lgfs2017CalculatorTestCase.create_tests()
