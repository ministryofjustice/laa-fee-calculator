# -*- coding: utf-8 -*-
from decimal import Decimal
from math import floor
import os

from rest_framework import status

from calculator.tests.lib.utils import scenario_ccr_to_id
from calculator.tests.base import AgfsCalculatorTestCase, FeeTypeUnitMixin


class Agfs9CalculatorTestCase(AgfsCalculatorTestCase, FeeTypeUnitMixin):
    scheme_id = 1
    csv_path = os.path.join(
        os.path.dirname(__file__),
        'data/test_dataset_agfs_9.csv'
    )

    def assertRowValuesCorrect(self, row):
        """
        Assert row values equal calculated values
        """
        is_basic = row['BILL_SUB_TYPE'] == 'AGFS_FEE'

        data = {
            'scheme': self.scheme_id,
            'fee_type_code': row['BILL_SUB_TYPE'],
            'scenario': scenario_ccr_to_id(row['BILL_SCENARIO_ID']),
            'advocate_type': row['PERSON_TYPE'],
            'offence_class': row['OFFENCE_CATEGORY'],
        }

        if not is_basic:
            # get unit for fee type
            self.get_fee_type_unit(data, row)
        else:
            data['DAY'] = Decimal(row['NUM_ATTENDANCE_DAYS']) or 1
            data['PPE'] = int(row['PPE'])
            data['PW'] = int(row['NUM_OF_WITNESSES'])

        if row['NUM_OF_CASES']:
            data['NUMBER_OF_CASES'] = int(row['NUM_OF_CASES'])
        if row['NO_DEFENDANTS']:
            data['NUMBER_OF_DEFENDANTS'] = int(row['NO_DEFENDANTS'])
        if row['NUM_OF_HEARINGS']:
            data['NUMBER_OF_HEARINGS'] = int(row['NUM_OF_HEARINGS'])
        if row['TRIAL_LENGTH']:
            data['TRIAL_LENGTH'] = int(row['TRIAL_LENGTH'])
        if row['PPE']:
            data['PAGES_OF_PROSECUTING_EVIDENCE'] = int(row['PPE'])
        if row['MONTHS']:
            data['RETRIAL_INTERVAL'] = floor(abs(Decimal(row['MONTHS'])))
        if row['THIRD_CRACKED']:
            data['THIRD_CRACKED'] = int(row['THIRD_CRACKED'])

        resp = self.client.get(self.endpoint(), data=data)
        self.assertEqual(resp.status_code, status.HTTP_200_OK, resp.content)

        self.assertEqual(
            resp.data['amount'],
            Decimal(row['CALC_FEE_EXC_VAT']),
            data
        )


Agfs9CalculatorTestCase.create_tests()
