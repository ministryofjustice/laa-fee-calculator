from django.test import TestCase
from calculator.models import Scheme
from calculator.constants import SCHEME_TYPE
from api.filters import SchemeFilter

NUMBER_OF_AGFS_SCHEMES = 5
NUMBER_OF_LGFS_SCHEMES = 2


class SchemeFilterTestCase(TestCase):
    @classmethod
    def setUp(cls):
        cls.allSchemes = Scheme.objects.all()

    def test_filter_for_agfs_type(self):
        schemes = SchemeFilter(data={'type': 'AGFS'}, queryset=self.allSchemes).qs
        self.assertEqual(len(schemes), NUMBER_OF_AGFS_SCHEMES)
        self.assertEqual({s.base_type for s in schemes}, {SCHEME_TYPE.for_constant('AGFS').value})

    def test_filter_for_lgfs_type(self):
        schemes = SchemeFilter(data={'type': 'LGFS'}, queryset=self.allSchemes).qs
        self.assertEqual(len(schemes), NUMBER_OF_LGFS_SCHEMES)
        self.assertEqual({s.base_type for s in schemes}, {SCHEME_TYPE.for_constant('LGFS').value})

    def test_filter_for_case_date(self):
        schemes = SchemeFilter(data={'case_date': '2020-06-06'}, queryset=self.allSchemes).qs
        self.assertEqual(len(schemes), 2)
        self.assertEqual({s.pk for s in schemes}, {2, 4})

    def test_filter_for_type_and_case_date(self):
        schemes = SchemeFilter(data={'type': 'AGFS', 'case_date': '2020-06-06'}, queryset=self.allSchemes).qs
        self.assertEqual(len(schemes), 1)
        self.assertEqual(schemes.first().pk, 4)