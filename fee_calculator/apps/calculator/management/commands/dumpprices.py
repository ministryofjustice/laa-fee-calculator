# -*- coding: utf-8 -*-
import json

from django.core.management import BaseCommand
from django.core.serializers import serialize

from calculator.models import Price, Scheme


class Command(BaseCommand):
    help = 'Dump prices for a given scheme to a JSON fixture file'

    def add_arguments(self, parser):
        parser.add_argument(
            'scheme_id', type=int,
            help='ID of the scheme to dump prices for'
        )
        parser.add_argument(
            'output_file', type=str,
            help='Path to the output fixture file'
        )

    def handle(self, *args, **options):
        scheme_id = options['scheme_id']
        output_file = options['output_file']

        try:
            scheme = Scheme.objects.get(pk=scheme_id)
        except Scheme.DoesNotExist:
            self.stderr.write(self.style.ERROR(f'Scheme {scheme_id} does not exist'))
            return

        prices = Price.objects.filter(scheme_id=scheme_id)
        count = prices.count()

        if count == 0:
            self.stderr.write(self.style.WARNING(f'No prices found for scheme {scheme_id}'))
            return

        data = json.loads(serialize('json', prices))

        with open(output_file, 'w') as f:
            json.dump(data, f, indent=2)
            f.write('\n')

        self.stdout.write(
            self.style.SUCCESS(f'Dumped {count} prices for {scheme.description} to {output_file}')
        )
