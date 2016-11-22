# -*- coding: utf-8 -*-
import os
from decimal import Decimal

from django.conf import settings
from django.test import TestCase
from django.utils.text import slugify
from rest_framework import status

import xlrd

from .lib.utils import bill_to_code


SPREADSHEET_PATH = os.path.join(
    os.path.dirname(__file__),
    'data/test_data.xlsx')


class CalculatorTestCase(TestCase):
    endpoint = '/api/%s/calculate' % settings.API_VERSION
    fixtures = [
        'advocatetype', 'feetype', 'offenceclass', 'price', 'scenario',
        'scheme', 'unit',
    ]

    def assertRowValuesCorrect(self, row):
        """
        Assert row values equal calculated values
        """
        code = bill_to_code(row['bill_type'], row['bill_sub_type'])
        resp = self.client.get(self.endpoint, data={
            'code': code
        })
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['amount'], 100)


def value(cell):
    """
    Decode the cell value to a Decimal if numeric
    """
    if isinstance(cell.value, float):
        return Decimal(str(cell.value))
    return cell.value


def spreadsheet():
    """
    Generator for the rows of the spreadsheet
    """
    book = xlrd.open_workbook(SPREADSHEET_PATH)
    sheet = book.sheet_by_index(0)
    cols = [slugify(sheet.cell(0, i).value) for i in range(sheet.ncols)]
    cols.append('line_number')
    for row in range(1, sheet.nrows):
        cells = [value(sheet.cell(row, i)) for i in range(sheet.ncols)]
        cells.append(row + 1)
        yield dict(zip(cols, cells))


def test_name(row):
    """
    Generate the method name for the test
    """
    return 'test_{0}_{1}'.format(
        row.get('line_number'),
        slugify(row.get('case_id')))


test_name.__test__ = False


def make_test(row):
    """
    Generate a test method
    """
    def row_test(self):
        self.assertRowValuesCorrect(row)
    row_test.__doc__ = str(row.get('line_number')) + ': ' + \
        str(row.get('case_id'))
    return row_test


make_test.__test__ = False


def create_tests():
    """
    Insert test methods into the TestCase for each case in the spreadsheet
    """
    for row in spreadsheet():
        setattr(CalculatorTestCase, test_name(row), make_test(row))


create_tests.__test__ = False

create_tests()
