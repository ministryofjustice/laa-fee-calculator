# -*- coding: utf-8 -*-
from django.core.management import BaseCommand
from django.db.transaction import atomic

from calculator.models import (
    Scheme, FeeType, Price, Unit
)


class Command(BaseCommand):
    help = '''
        Create new fee type prices based on an existing feetype's. Provide the ID of the
        source fee type as well as the new fee type's ID and it starget scheme id.
        The prices for the source fee type will be copied as those of the new fee type for the
        specified scheme. The new fee type itself and the fee scheme must have already
        been created in the DB - see feetype.json and scheme.json.
    '''

    def add_arguments(self, parser):
        parser.add_argument(
            'source_feetype_id', type=int,
            help='ID of the source feetype'
        )
        parser.add_argument(
            'source_scheme_id', type=int,
            help='ID of the source feetype\'s scheme'
        )
        parser.add_argument(
            'new_feetype_id', type=int,
            help='ID of the feetype to create prices for'
        )
        parser.add_argument(
            'new_scheme_id', type=int,
            help='ID of the scheme to create feetype prices for'
        )
        parser.add_argument(
            '-u', '--unit', type=str,
            help='[optional] ID of the unit for the feetype prices if different from source'
        )

    def handle(self, *args, **options):
        source_fee_type = FeeType.objects.get(pk=options['source_feetype_id'])
        source_scheme = Scheme.objects.get(pk=options['source_scheme_id'])
        new_fee_type = FeeType.objects.get(pk=options['new_feetype_id'])
        new_scheme = Scheme.objects.get(pk=options['new_scheme_id'])

        with atomic():
            for price in Price.objects.filter(fee_type=source_fee_type, scheme=source_scheme):
                modifiers = list(price.modifiers.all())
                price.id = None
                price.fee_type = new_fee_type
                price.scheme = new_scheme
                if options['unit']:
                    price.unit = Unit.objects.get(pk=options['unit'])

                price.save()
                price.modifiers.add(*modifiers)
