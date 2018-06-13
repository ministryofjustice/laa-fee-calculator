# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand

from calculator.models import (
    Scheme, Scenario, ScenarioCode, AdvocateType, FeeType, OffenceClass, Unit,
    Modifier, ModifierType, Price
)


def print_deleted_info(results):
    if results[0] > 0:
        for key in list(results[1].keys()):
            if results[1][key] == 0:
                del results[1][key]
        print('Deleted {count} records {types}'.format(
            count=results[0], types=results[1]
        ))


class Command(BaseCommand):
    help = 'Delete all scheme data from the database'

    def handle(self, *args, **options):
        print_deleted_info(Price.objects.all().delete())
        print_deleted_info(Modifier.objects.all().delete())
        print_deleted_info(ModifierType.objects.all().delete())
        print_deleted_info(Unit.objects.all().delete())
        print_deleted_info(OffenceClass.objects.all().delete())
        print_deleted_info(FeeType.objects.all().delete())
        print_deleted_info(AdvocateType.objects.all().delete())
        print_deleted_info(ScenarioCode.objects.all().delete())
        print_deleted_info(Scenario.objects.all().delete())
        print_deleted_info(Scheme.objects.all().delete())
