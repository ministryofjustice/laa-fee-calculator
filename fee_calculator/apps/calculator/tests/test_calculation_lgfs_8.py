# -*- coding: utf-8 -*-
from decimal import Decimal
import os

from calculator.tests.base import LgfsCalculatorTestCase


class Lgfs8CalculatorTestCase(LgfsCalculatorTestCase):
    scheme_id = 2
    csv_path = os.path.join(
        os.path.dirname(__file__),
        'data/test_dataset_lgfs_8.csv'
    )

    def test_evidence_provision_fee_0(self):
        data = {
            'scheme': self.scheme_id,
            'fee_type_code': 'EVID_PROV_FEE',
            'scenario': 4,
            'offence_class': 'A',
            'level': 0
        }
        self.check_result(data, Decimal(0))

    def test_evidence_provision_fee_1(self):
        data = {
            'scheme': self.scheme_id,
            'fee_type_code': 'EVID_PROV_FEE',
            'scenario': 4,
            'offence_class': 'A',
            'level': 1
        }
        self.check_result(data, Decimal(45))

    def test_evidence_provision_fee_2(self):
        data = {
            'scheme': self.scheme_id,
            'fee_type_code': 'EVID_PROV_FEE',
            'scenario': 2,
            'offence_class': 'B',
            'level': 2
        }
        self.check_result(data, Decimal(90))

    def test_evidence_provision_fee_3(self):
        data = {
            'scheme': self.scheme_id,
            'fee_type_code': 'EVID_PROV_FEE',
            'scenario': 1,
            'offence_class': 'D',
            'level': 3
        }
        self.check_result(data, Decimal(90))


Lgfs8CalculatorTestCase.create_tests()
