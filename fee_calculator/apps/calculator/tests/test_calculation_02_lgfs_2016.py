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

Lgfs2016CalculatorTestCase.create_special_prep_tests([43.12, 41.06])
