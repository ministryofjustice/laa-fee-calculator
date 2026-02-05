# -*- coding: utf-8 -*-
import os

from calculator.tests.base import (
    LgfsCalculatorTestCase, EvidenceProvisionFeeTestMixin, LgfsWarrantFeeTestMixin
)


class Lgfs2026CalculatorTestCase(
    LgfsCalculatorTestCase, EvidenceProvisionFeeTestMixin, LgfsWarrantFeeTestMixin
):
    scheme_id = 13
    csv_path = os.path.join(
        os.path.dirname(__file__),
        'data/test_dataset_lgfs_2026.csv'
    )


Lgfs2026CalculatorTestCase.create_tests()
