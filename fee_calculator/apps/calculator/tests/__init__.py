# -*- coding: utf-8 -*-
from django.core.management import call_command
from django.test.runner import DiscoverRunner


class PreloadDataDiscoverRunner(DiscoverRunner):

    def setup_databases(self, **kwargs):
        config = super().setup_databases(**kwargs)
        call_command('loadalldata', verbosity=0)
        return config
