# -*- coding: utf-8 -*-
from django.core.management import BaseCommand, call_command


class Command(BaseCommand):
    help = 'Load all scheme data into the database'

    def handle(self, *args, **options):
        verbosity = options['verbosity']
        fixtures = [
            'scheme',
            'scenario',
            'scenariocode',
            'advocatetype',
            'offenceclass',
            'unit',
            'modifiertype',
            'modifier',
            'feetype',
            'price_01_agfs_9',
            'price_02_lgfs_9',
            'price_03_agfs_10',
            'price_04_agfs_11',
            'price_05_agfs_12',
            'price_06_lgfs_10',
            'price_07_agfs_13',
            'price_08_lgfs_clair_contingency',
            'price_09_agfs_clair_contingency',
            'price_10_agfs_14',
            'price_11_agfs_15',
            'price_12_agfs_16',
            'price_13_lgfs_11',
            'price_14_agfs_17',
        ]
        call_command('loadbulkdata', *fixtures, verbosity=verbosity)
