# -*- coding: utf-8 -*-
from django.core.management import BaseCommand
from django.db.transaction import atomic

from calculator.models import (
    Price, Scheme
)


class Command(BaseCommand):
    help = '''
        Create a new fee scheme based on an existing one. Provide the ID of the
        source scheme and the new scheme, and the prices for the source scheme
        will be copied to the new scheme. You must have already created a
        Scheme record for the new scheme.
    '''

    def add_arguments(self, parser):
        parser.add_argument(
            'source_scheme_id', type=int,
            help='ID of the source scheme'
        )
        parser.add_argument(
            'new_scheme_id', type=int,
            help='ID of the scheme to copy prices to'
        )

    def handle(self, *args, **options):
        source_scheme = Scheme.objects.get(pk=options['source_scheme_id'])
        new_scheme = Scheme.objects.get(pk=options['new_scheme_id'])

        with atomic():
            for price in Price.objects.filter(scheme=source_scheme):
                modifiers = list(price.modifiers.all())
                price.id = None
                price.scheme = new_scheme
                price.save()
                price.modifiers.add(*modifiers)
