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
            'price'
        ]
        call_command('loadbulkdata', *fixtures, verbosity=verbosity)
