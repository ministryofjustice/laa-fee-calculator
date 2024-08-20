# -*- coding: utf-8 -*-
import csv
from decimal import Decimal
import math

from django.conf import settings
from django.test import SimpleTestCase
from rest_framework import status

from calculator.tests.lib.utils import scenario_clf_to_id, scenario_ccr_to_id
from calculator.models import Price, FeeType


class CalculatorTestCase(SimpleTestCase):
    scheme_id = NotImplemented
    databases = ['default']

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


class FeeTypeUnitMixin:
    def get_fee_type_unit(self, data, row):
        """
        Commmon code shared between AGFS 9 Calculator and AGFS 10+ Calculators to retrieve the unit for non-basic
        fee types.
        """
        unit_resp = self.client.get(
            '/api/{version}/fee-schemes/{scheme_id}/units/'.format(
                version=settings.API_VERSION, scheme_id=self.scheme_id),
            data=data
        )
        self.assertEqual(
            unit_resp.status_code, status.HTTP_200_OK, unit_resp.content
        )
        self.assertEqual(unit_resp.json()['count'], 1, data)
        unit = unit_resp.json()['results'][0]['id']
        data[unit] = (
                         Decimal(row['NUM_ATTENDANCE_DAYS'])
                         if row['BILL_TYPE'] == 'AGFS_FEE'
                         else Decimal(row['QUANTITY'])
                     ) or 1


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

        data['TRIAL_LENGTH'] = data['day']

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


class EvidenceProvisionFeeTestMixin():

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
        self.check_result(data, Decimal(0))


class BaseWarrantFeeTestMixin():

    def _test_warrant_fee_matches_appropriate_base(
        self, base_scenario_id, warrant_scenario_id, fee_type_code
    ):
        advocate_resp = self.client.get(
            '/api/{version}/fee-schemes/{scheme_id}/advocate-types/'.format(
                version=settings.API_VERSION, scheme_id=self.scheme_id),
        )
        self.assertEqual(
            advocate_resp.status_code, status.HTTP_200_OK, advocate_resp.content
        )
        advocate_types = [item['id'] for item in advocate_resp.json()['results']]

        offence_class_resp = self.client.get(
            '/api/{version}/fee-schemes/{scheme_id}/offence-classes/'.format(
                version=settings.API_VERSION, scheme_id=self.scheme_id),
        )
        self.assertEqual(
            offence_class_resp.status_code,
            status.HTTP_200_OK,
            offence_class_resp.content
        )
        offence_classes = [
            item['id'] for item in offence_class_resp.json()['results']
        ]

        for advocate_type in advocate_types:
            for offence_class in offence_classes:
                data = {
                    'scheme': self.scheme_id,
                    'scenario': base_scenario_id,
                    'fee_type_code': fee_type_code,
                    'offence_class': offence_class,
                    'advocate_type': advocate_type
                }

                unit_resp = self.client.get(
                    '/api/{version}/fee-schemes/{scheme_id}/units/'.format(
                        version=settings.API_VERSION, scheme_id=self.scheme_id),
                    data=data
                )
                self.assertEqual(
                    unit_resp.status_code, status.HTTP_200_OK, unit_resp.content
                )
                unit = unit_resp.json()['results'][0]['id']
                data[unit] = 1

                base_resp = self.client.get(self.endpoint(), data=data)

                # check 0 returned without warrant_interval >= 3
                data['scenario'] = warrant_scenario_id
                self.check_result(data, Decimal(0))

                data['warrant_interval'] = 3
                self.check_result(data, base_resp.data['amount'])


class Agfs10PlusWarrantFeeTestMixin(BaseWarrantFeeTestMixin):

    def test_trial_warrant_fee_equals_guilty_plea_fee(self):
        self._test_warrant_fee_matches_appropriate_base(2, 47, 'AGFS_FEE')

    def test_appeal_against_conviction_warrant_fee(self):
        self._test_warrant_fee_matches_appropriate_base(5, 51, 'AGFS_APPEAL_CON')

    def test_appeal_against_sentence_warrant_fee(self):
        self._test_warrant_fee_matches_appropriate_base(6, 52, 'AGFS_APPEAL_SEN')

    def test_committal_for_sentence_warrant_fee(self):
        self._test_warrant_fee_matches_appropriate_base(7, 53, 'AGFS_COMMITTAL')

    def test_order_breach_warrant_fee(self):
        self._test_warrant_fee_matches_appropriate_base(9, 54, 'AGFS_ORDER_BRCH')


class LgfsWarrantFeeTestMixin(BaseWarrantFeeTestMixin):

    def test_pre_plea_warrant_fee_equals_guilty_plea_fee(self):
        self._test_warrant_fee_matches_appropriate_base(2, 48, 'LIT_FEE')

    def test_post_plea_warrant_fee_equals_cracked_trial_fee(self):
        self._test_warrant_fee_matches_appropriate_base(3, 49, 'LIT_FEE')

    def test_trail_started_warrant_fee_equals_trial_fee(self):
        self._test_warrant_fee_matches_appropriate_base(4, 50, 'LIT_FEE')

    def test_post_plea_retrial_warrant_fee_equals_cracked_retrial_fee(self):
        self._test_warrant_fee_matches_appropriate_base(10, 55, 'LIT_FEE')

    def test_retrial_started_warrant_fee_equals_retrial_fee(self):
        self._test_warrant_fee_matches_appropriate_base(11, 56, 'LIT_FEE')

    def test_appeal_against_conviction_warrant_fee(self):
        self._test_warrant_fee_matches_appropriate_base(5, 51, 'LIT_FEE')

    def test_appeal_against_sentence_warrant_fee(self):
        self._test_warrant_fee_matches_appropriate_base(6, 52, 'LIT_FEE')

    def test_committal_for_sentence_warrant_fee(self):
        self._test_warrant_fee_matches_appropriate_base(7, 53, 'LIT_FEE')

    def test_order_breach_warrant_fee(self):
        self._test_warrant_fee_matches_appropriate_base(9, 54, 'LIT_FEE')


class BaseLondonRatesTestMixin:

    def make_london_rates_test(scenario_id, fee_type_code, london_rates_apply,
                               unit_code, amount, expected_amount):
        """
        Generate a test method
        """
        def lr_test(self):
            self._test_fee_with_london_rates(scenario_id, fee_type_code, london_rates_apply,
                                             unit_code, amount, expected_amount)

        return lr_test

    def _test_fee_with_london_rates(
        self, scenario_id, fee_type_code, london_rates_apply, unit_code, amount, expected_amount
    ):
        """
        Run API call and check the response matches expectations
        """
        response = self.client.get(
            '/api/{version}/fee-schemes/{scheme_id}/calculate/?fee_type_code={fee_type_code}&'
            '{unit}={amount}&london_rates_apply={london_rates_apply}&scenario={scenario}'.format(
                version=settings.API_VERSION, scheme_id=self.scheme_id,
                fee_type_code=fee_type_code, unit=unit_code, amount=amount,
                london_rates_apply=london_rates_apply, scenario=scenario_id),
        )
        self.assertEqual(
            response.status_code, status.HTTP_200_OK, response.content
        )

        returned = response.data['amount']
        close_enough = math.isclose(returned, expected_amount, abs_tol=0.011)
        self.assertTrue(
            close_enough,
            msg='{returned} != {expected} within £0.01 tolerance'.format(
                returned=returned,
                expected=expected_amount,
            )
        )


class LgfsSpecialPreparationFeeTestMixin(BaseLondonRatesTestMixin):

    @classmethod
    def create_special_prep_tests(cls, valid_scenarios, expected_prices):
        """
        Trigger different batches of test generation
        """
        cls._test_special_preparation_fee_inside_london(valid_scenarios, expected_prices[0] * 2)
        cls._test_special_preparation_fee_outside_london(valid_scenarios, expected_prices[1] * 2)
        cls._test_special_preparation_fee_edge_cases(valid_scenarios)

    @classmethod
    def _test_special_preparation_fee_inside_london(cls, scenarios, expected):
        """
        Generate test scenarios with london rates
        """
        for scenario_id in scenarios:
            test_name = "test_special_preparation_fee_inside_london_{scenario}".format(scenario=scenario_id)

            setattr(cls,
                    test_name,
                    cls.make_london_rates_test(scenario_id, 'LGFS_SPCL_PREP', 'true', 'HOUR', 2, expected))

    @classmethod
    def _test_special_preparation_fee_outside_london(cls, scenarios, expected):
        """
        Generate test scenarios without london rates
        """
        for scenario_id in scenarios:
            test_name = "test_special_preparation_fee_outside_london_{scenario}".format(scenario=scenario_id)

            setattr(cls,
                    test_name,
                    cls.make_london_rates_test(scenario_id, 'LGFS_SPCL_PREP', 'false', 'HOUR', 2, expected))

    @classmethod
    def _test_special_preparation_fee_edge_cases(cls, scenarios):
        """
        Generate test scenarios for edge cases
        """

        # Zero amounts
        for scenario_id in scenarios:
            test_name = "test_special_preparation_fee_zero_amounts_{scenario}".format(scenario=scenario_id)

            setattr(cls,
                    test_name,
                    cls.make_london_rates_test(scenario_id, 'LGFS_SPCL_PREP', 'true', 'HOUR', 0, 0))

        # london_rates_apply not provided
        for scenario_id in scenarios:
            test_name = "test_special_preparation_fee_null_london_{scenario}".format(scenario=scenario_id)

            setattr(cls,
                    test_name,
                    cls.make_london_rates_test(scenario_id, 'LGFS_SPCL_PREP', '', 'HOUR', 2, 0))


class Agfs10PlusCalculatorTestCase(AgfsCalculatorTestCase, FeeTypeUnitMixin):

    def assertRowValuesCorrect(self, row):
        """
        Assert row values equal calculated values
        """
        is_basic = row['BILL_SUB_TYPE'] == 'AGFS_FEE'

        data = {
            'scheme': self.scheme_id,
            'fee_type_code': row['BILL_SUB_TYPE'],
            'scenario': scenario_ccr_to_id(row['BILL_SCENARIO_ID'], scheme=10),
            'advocate_type': row['PERSON_TYPE'],
            'offence_class': row['OFFENCE_CATEGORY'],
        }

        if not is_basic:
            self.get_fee_type_unit(data, row)
        else:
            data['DAY'] = Decimal(row['NUM_ATTENDANCE_DAYS']) or 1

        if row['NUM_OF_CASES']:
            data['NUMBER_OF_CASES'] = int(row['NUM_OF_CASES'])
        if row['NO_DEFENDANTS']:
            data['NUMBER_OF_DEFENDANTS'] = int(row['NO_DEFENDANTS'])
        if row['NUM_OF_HEARINGS']:
            data['NUMBER_OF_HEARINGS'] = int(row['NUM_OF_HEARINGS'])
        if row['TRIAL_LENGTH']:
            data['TRIAL_LENGTH'] = int(row['TRIAL_LENGTH'])
        if row['MONTHS']:
            data['RETRIAL_INTERVAL'] = math.floor(abs(Decimal(row['MONTHS'])))
        if row['THIRD_CRACKED']:
            data['THIRD_CRACKED'] = row['THIRD_CRACKED']
        if row['PPE']:
            data['PAGES_OF_PROSECUTING_EVIDENCE'] = int(row['PPE'])

        resp = self.client.get(self.endpoint(), data=data)
        self.assertEqual(resp.status_code, status.HTTP_200_OK, resp.content)

        self.assertEqual(
            resp.data['amount'],
            Decimal(row['CALC_FEE_EXC_VAT']),
            data
        )
