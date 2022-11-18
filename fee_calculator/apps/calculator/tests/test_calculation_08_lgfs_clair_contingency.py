# -*- coding: utf-8 -*-
import os

from calculator.tests.base import (
    LgfsCalculatorTestCase, EvidenceProvisionFeeTestMixin, LgfsWarrantFeeTestMixin
)


class LgfsClairContingencyCalculatorTestCase(
    LgfsCalculatorTestCase, EvidenceProvisionFeeTestMixin, LgfsWarrantFeeTestMixin
):
    scheme_id = 8
    csv_path = os.path.join(
        os.path.dirname(__file__),
        'data/test_dataset_lgfs_2022.csv'
    )


LgfsClairContingencyCalculatorTestCase.create_tests()
