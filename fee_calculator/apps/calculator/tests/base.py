# -*- coding: utf-8 -*-
import csv
from decimal import Decimal
import math

from django.conf import settings
from django.test import TestCase
from rest_framework import status

from calculator.tests.lib.utils import scenario_clf_to_id
from calculator.models import Price, FeeType


class CalculatorTestCase(TestCase):
    scheme_id = NotImplemented

    def endpoint(self):
        return '/api/{version}/fee-schemes/{scheme_id}/calculate/'.format(
            version=settings.API_VERSION, scheme_id=self.scheme_id
        )

    def assertRowValuesCorrect(self, row):
        return NotImplemented

    def check_result(self, data, expected):
        resp = self.client.get(self.endpoint(), data=data)
        self.assertEqual(
            resp.status_code, status.HTTP_200_OK, resp.content
        )

        self.assertEqual(
            resp.data['amount'],
            expected,
            data
        )

    @staticmethod
    def get_test_name(prefix, row, line_number):
        """
        Generate the method name for the test
        """
        return 'test_{0}_{1}_{2}'.format(
            prefix,
            line_number,
            row.get('CASE_ID')
        )

    @staticmethod
    def make_test(row, line_number):
        """
        Generate a test method
        """
        def row_test(self):
            self.assertRowValuesCorrect(row)
        row_test.__doc__ = str(line_number) + ': ' + str(row.get('CASE_ID'))
        return row_test

    @classmethod
    def create_tests(cls):
        return NotImplemented


class AgfsCalculatorTestCase(CalculatorTestCase):
    csv_path = NotImplemented

    @classmethod
    def create_tests(cls):
        """
        Insert test methods into the TestCase for each case in the spreadsheet
        """

        tested_scenarios = set()
        tested_fees = set()
        with open(cls.csv_path) as csvfile:
            reader = csv.DictReader(csvfile)
            priced_fees = FeeType.objects.filter(
                id__in=Price.objects.all().values_list('fee_type_id', flat=True).distinct()
            ).values_list('code', flat=True).distinct()
            for i, row in enumerate(reader):
                if row['BILL_SUB_TYPE'] in priced_fees:
                    tested_scenarios.add(row['BILL_SCENARIO_ID'])
                    tested_fees.add(row['BILL_SUB_TYPE'])
                    setattr(
                        cls,
                        cls.get_test_name('agfs', row, i+2),
                        cls.make_test(row, i+2)
                    )
        print('{0}: Testing {1} scenarios and {2} fees'.format(
            cls.__name__, len(tested_scenarios), len(tested_fees)
        ))


class LgfsCalculatorTestCase(CalculatorTestCase):
    csv_path = NotImplemented

    def assertRowValuesCorrect(self, row):
        """
        Assert row values equal calculated values
        """
        data = {
            'scheme': self.scheme_id,
            'fee_type_code': row['BILL_SUB_TYPE'],
            'scenario': scenario_clf_to_id(row['SCENARIO']),
            'offence_class': row['OFFENCE_CATEGORY'],
            'day': int(row['TRIAL_LENGTH']) if row['TRIAL_LENGTH'] else 0,
            'ppe': int(row['EVIDENCE_PAGES']) if row['EVIDENCE_PAGES'] else 0
        }

        if row['NO_DEFENDANTS']:
            data['NUMBER_OF_DEFENDANTS'] = int(row['NO_DEFENDANTS'])

        resp = self.client.get(self.endpoint(), data=data)
        self.assertEqual(
            resp.status_code, status.HTTP_200_OK, resp.content
        )

        returned = resp.data['amount']
        expected = Decimal(row['ACTUAL_FEE_EXC_VAT'] or row['CALC_FEE_EXC_VAT'])
        close_enough = math.isclose(returned, expected, abs_tol=0.011)
        if not close_enough:
            expected = Decimal(row['CALC_FEE_EXC_VAT'])
            close_enough = math.isclose(returned, expected, abs_tol=0.011)
        self.assertTrue(
            close_enough,
            msg='{returned} != {expected} within £0.01 tolerance : {data}'.format(
                returned=returned,
                expected=expected,
                data=data
            )
        )

    @classmethod
    def create_tests(cls):
        """
        Insert test methods into the TestCase for each case in the spreadsheet
        """
        tested_scenarios = set()
        with open(cls.csv_path) as csvfile:
            reader = csv.DictReader(csvfile)
            for i, row in enumerate(reader):
                tested_scenarios.add(row['SCENARIO'])
                setattr(
                    cls,
                    cls.get_test_name('lgfs', row, i+2),
                    cls.make_test(row, i+2)
                )
        print('{0}: Testing {1} scenarios'.format(
            cls.__name__, len(tested_scenarios)
        ))
