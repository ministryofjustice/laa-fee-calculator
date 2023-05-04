from django.test import TestCase
from api.utils import fix_advocate_category
from rest_framework.test import APIRequestFactory
from calculator.models import Scheme


class FixAdvocateCategoryTestCase(TestCase):
    @classmethod
    def setUp(cls):
        cls.factory = APIRequestFactory()

    def dummy_function(self, return_value):
        def dummy(request, param_name, scheme, required=False, default=None):
            return return_value

        return dummy

    def test_does_not_alter_QC_advodate_type(self):
        request = self.factory.get('/api/v1/fee-schemes/10/prices/?advocate_type=QC')
        fac = fix_advocate_category(self.dummy_function('QC'))
        scheme = Scheme.objects.get(pk=10)
        self.assertEqual(fac(request, 'advocate_type', scheme), 'QC')

    def test_changes_KC_advodate_type_to_QC(self):
        request = self.factory.get('/api/v1/fee-schemes/10/prices/?advocate_type=KC')
        fac = fix_advocate_category(self.dummy_function('KC'))
        scheme = Scheme.objects.get(pk=10)
        self.assertEqual(fac(request, 'advocate_type', scheme), 'QC')

    def test_does_not_alter_a_parameter_other_than_advocate_type(self):
        request = self.factory.get('/api/v1/fee-schemes/10/prices/?other_param=KC')
        fac = fix_advocate_category(self.dummy_function('KC'))
        scheme = Scheme.objects.get(pk=10)
        self.assertEqual(fac(request, 'other_param', scheme), 'KC')

    def test_does_not_alter_KC_advodate_type_in_AGFS_fee_scheme_15(self):
        request = self.factory.get('/api/v1/fee-schemes/11/prices/?advocate_type=QC')
        fac = fix_advocate_category(self.dummy_function('KC'))
        scheme = Scheme.objects.get(pk=11)
        self.assertEqual(fac(request, 'advocate_type', scheme), 'KC')

    def test_changes_QC_advodate_type_to_KC_in_AGFS_fee_scheme_15(self):
        request = self.factory.get('/api/v1/fee-schemes/11/prices/?advocate_type=KC')
        fac = fix_advocate_category(self.dummy_function('QC'))
        scheme = Scheme.objects.get(pk=11)
        self.assertEqual(fac(request, 'advocate_type', scheme), 'KC')

    def test_does_not_alter_a_parameter_other_than_advocate_type_in_AGFS_fee_scheme_15(self):
        request = self.factory.get('/api/v1/fee-schemes/11/prices/?other_param=QC')
        fac = fix_advocate_category(self.dummy_function('QC'))
        scheme = Scheme.objects.get(pk=11)
        self.assertEqual(fac(request, 'other_param', scheme), 'QC')
