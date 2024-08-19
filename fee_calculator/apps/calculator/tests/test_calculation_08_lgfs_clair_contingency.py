# -*- coding: utf-8 -*-
import os

from calculator.tests.base import (
    LgfsCalculatorTestCase, EvidenceProvisionFeeTestMixin, LgfsWarrantFeeTestMixin, LgfsSpecialPreparationFeeTestMixin
)


class LgfsClairContingencyCalculatorTestCase(
    LgfsCalculatorTestCase, EvidenceProvisionFeeTestMixin, LgfsWarrantFeeTestMixin, LgfsSpecialPreparationFeeTestMixin
):
    scheme_id = 8
    csv_path = os.path.join(
        os.path.dirname(__file__),
        'data/test_dataset_lgfs_2022.csv'
    )


LgfsClairContingencyCalculatorTestCase.create_tests()
LgfsClairContingencyCalculatorTestCase.create_special_prep_tests()
