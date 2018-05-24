# -*- coding: utf-8 -*-
import csv
from datetime import datetime
from decimal import Decimal
import os

from django.conf import settings
from rest_framework import status

from calculator.tests.lib.utils import scenario_clf_to_id
from calculator.tests.calculation_utils import (
    CalculatorTestCase, get_test_name, make_test
)


LGFS_CSV_PATH = os.path.join(
    os.path.dirname(__file__),
    'data/test_dataset_lgfs.csv'
)


class Lgfs8CalculatorTestCase(CalculatorTestCase):

    def assertRowValuesCorrect(self, row):
        """
        Assert row values equal calculated values
        """
        calc_date_str = row['REP_ORD_DATE']
        if calc_date_str:
            if len(calc_date_str) > 10:
                calc_date_str = calc_date_str[:-9]
            calculation_date = datetime.strptime(
                calc_date_str, '%d/%m/%Y'
            ).date()
        else:
            calculation_date = datetime.now().date()

        # get scheme for date
        scheme_resp = self.client.get(
            '/api/{version}/fee-schemes/'.format(version=settings.API_VERSION),
            data=dict(supplier_type='solicitor', case_date=calculation_date)
        )
        self.assertEqual(
            scheme_resp.status_code, status.HTTP_200_OK, scheme_resp.content
        )
        self.assertEqual(scheme_resp.json()['count'], 1)
        scheme_id = scheme_resp.json()['results'][0]['id']

        data = {
            'scheme': scheme_id,
            'fee_type_code': row['BILL_SUB_TYPE'],
            'scenario': scenario_clf_to_id(row['SCENARIO']),
            'offence_class': row['OFFENCE_CATEGORY'],
            'day': int(row['TRIAL_LENGTH']) if row['TRIAL_LENGTH'] else 0,
            'ppe': int(row['EVIDENCE_PAGES']) if row['EVIDENCE_PAGES'] else 0
        }

        if row['NO_DEFENDANTS']:
            data['NUMBER_OF_DEFENDANTS'] = int(row['NO_DEFENDANTS'])

        resp = self.client.get(self.endpoint(scheme_id), data=data)
        self.assertEqual(
            resp.status_code, status.HTTP_200_OK, resp.content
        )

        self.assertEqual(
            resp.data['amount'],
            Decimal(row['CALC_FEE_EXC_VAT']),
            data
        )


def create_tests():
    """
    Insert test methods into the TestCase for each case in the spreadsheet
    """

    with open(LGFS_CSV_PATH) as csvfile:
        reader = csv.DictReader(csvfile)
        for i, row in enumerate(reader):
            setattr(
                Lgfs8CalculatorTestCase,
                get_test_name('lgfs', row, i+2),
                make_test(row, i+2)
            )


create_tests()
