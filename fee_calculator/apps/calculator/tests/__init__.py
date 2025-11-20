# -*- coding: utf-8 -*-
from django.core.management import call_command
from xmlrunner.extra.djangotestrunner import XMLTestRunner


class PreloadDataDiscoverRunner(XMLTestRunner):

    def setup_databases(self, **kwargs):
        config = super().setup_databases(**kwargs)
        call_command('loadalldata', verbosity=0)
        return config

    def run_tests(self, test_labels, **kwargs):
        """
        Run the unit tests for all the test labels in the provided list.

        Test labels should be dotted Python paths to test modules, test
        classes, or test methods.

        A list of 'extra' tests may also be provided; these tests
        will be added to the test suite.

        Returns the number of tests that failed.
        """
        self.setup_test_environment()
        old_config = self.setup_databases()
        suite = self.build_suite(test_labels)
        self.run_checks(['default'])
        result = self.run_suite(suite)
        self.teardown_databases(old_config)
        self.teardown_test_environment()
        return self.suite_result(suite, result)
