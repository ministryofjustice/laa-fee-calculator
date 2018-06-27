# -*- coding: utf-8 -*-
from django.conf import settings
from django.test import TestCase


class CalculatorTestCase(TestCase):
    scheme_id = NotImplemented

    def endpoint(self):
        return '/api/{version}/fee-schemes/{scheme_id}/calculate/'.format(
            version=settings.API_VERSION, scheme_id=self.scheme_id
        )

    def assertRowValuesCorrect(self, row):
        return NotImplemented


def get_test_name(prefix, row, line_number):
    """
    Generate the method name for the test
    """
    return 'test_{0}_{1}_{2}'.format(
        prefix,
        line_number,
        row.get('CASE_ID')
    )


def make_test(row, line_number):
    """
    Generate a test method
    """
    def row_test(self):
        self.assertRowValuesCorrect(row)
    row_test.__doc__ = str(line_number) + ': ' + str(row.get('CASE_ID'))
    return row_test
