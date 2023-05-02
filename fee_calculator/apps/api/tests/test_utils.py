from django.test import TestCase
from api.utils import fix_advocate_category
from rest_framework.test import APIRequestFactory


class FixAdvocateCategoryTestCase(TestCase):
    @classmethod
    def setUp(cls):
        cls.factory = APIRequestFactory()

    def dummy_function(self, return_value):
        def dummy(request, param_name, required=False, default=None):
            return return_value

        return dummy

    def test_does_not_alter_QC_advocate_type(self):
        request = self.factory.get('/api/v1/fee-schemes/10/prices/?advocate_type=QC')
        fac = fix_advocate_category(self.dummy_function('QC'))
        self.assertEqual(fac(request, 'advocate_type'), 'QC')

    def test_changes_KC_advocate_type_to_QC(self):
        request = self.factory.get('/api/v1/fee-schemes/10/prices/?advocate_type=KC')
        fac = fix_advocate_category(self.dummy_function('KC'))
        self.assertEqual(fac(request, 'advocate_type'), 'QC')

    def test_does_not_alter_a_parameter_other_than_advocate_type(self):
        request = self.factory.get('/api/v1/fee-schemes/10/prices/?other_param=KC')
        fac = fix_advocate_category(self.dummy_function('KC'))
        self.assertEqual(fac(request, 'other_param'), 'KC')

    # TODO:
    #   For AGFS fee scheme 14 and earlier, the advocate_type needs to be changed to QC
    #   For AGFS fee scheme 15 and later, the advocate_type needs to be changed to KC
