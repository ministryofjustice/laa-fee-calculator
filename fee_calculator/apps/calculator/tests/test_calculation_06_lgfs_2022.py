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

valid_special_prep_scenarios = list(range(2, 12)) + list(range(19, 37)) + list(range(38, 43))
Lgfs2022CalculatorTestCase.create_special_prep_tests(valid_special_prep_scenarios, [49.59, 47.22])
