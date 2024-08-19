# -*- coding: utf-8 -*-
import os

from calculator.tests.base import (
    LgfsCalculatorTestCase, EvidenceProvisionFeeTestMixin, LgfsWarrantFeeTestMixin, LgfsSpecialPreparationFeeTestMixin
)


class Lgfs2022CalculatorTestCase(
    LgfsCalculatorTestCase, EvidenceProvisionFeeTestMixin, LgfsWarrantFeeTestMixin, LgfsSpecialPreparationFeeTestMixin
):
    scheme_id = 6
    csv_path = os.path.join(
        os.path.dirname(__file__),
        'data/test_dataset_lgfs_2022.csv'
    )


Lgfs2022CalculatorTestCase.create_tests()
Lgfs2022CalculatorTestCase.create_special_prep_tests()
