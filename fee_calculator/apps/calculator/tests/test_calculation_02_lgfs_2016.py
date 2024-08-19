# -*- coding: utf-8 -*-
import os

from calculator.tests.base import (
    LgfsCalculatorTestCase, EvidenceProvisionFeeTestMixin, LgfsWarrantFeeTestMixin, LgfsSpecialPreparationFeeTestMixin
)


class Lgfs2016CalculatorTestCase(
    LgfsCalculatorTestCase, EvidenceProvisionFeeTestMixin, LgfsWarrantFeeTestMixin, LgfsSpecialPreparationFeeTestMixin
):
    scheme_id = 2
    csv_path = os.path.join(
        os.path.dirname(__file__),
        'data/test_dataset_lgfs_2016.csv'
    )


Lgfs2016CalculatorTestCase.create_tests()

valid_special_prep_scenarios = list(range(2, 13)) + list(range(19, 37)) + list(range(38, 43))
Lgfs2016CalculatorTestCase.create_special_prep_tests(valid_special_prep_scenarios, [43.12, 41.06])
