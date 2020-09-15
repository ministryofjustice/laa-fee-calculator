# -*- coding: utf-8 -*-
from django.core.management import BaseCommand
from django.db.transaction import atomic

from calculator.models import (
    Scheme, FeeType, Price, Unit
)


class Command(BaseCommand):
    help = '''
        Update cracked trial "advocate fee" prices for scheme 12 to be 100% of equivalent
        fee for a trial. Equivalent, in this context means, for the same scheme,
        offence, advocate type.
    '''

    def handle(self, *args, **options):
      with atomic():
        for price in Price.objects \
          .extra(
            select={'offence_class_id_decimal': 'CAST(offence_class_id as DECIMAL)'}
          ) \
          .filter(scheme_id=5,
            scenario_id=3,
            fee_type_id=34
          ) \
          .order_by('offence_class_id_decimal'):

          new_price = Price.objects \
                        .get(scheme_id=5,
                          scenario_id=4,
                          fee_type_id=34,
                          advocate_type_id=price.advocate_type_id,
                          offence_class_id=price.offence_class_id,
                          fixed_fee__gt=0
                        )

          print(f'UPDATING: scheme: {price.scheme_id}, scenario: {price.scenario_id}, fee_type: {price.fee_type_id}, advocate: {price.advocate_type_id}, offence_class_id: {price.offence_class_id}, fixed_fee: {price.fixed_fee} => {new_price.fixed_fee}')
          price.fixed_fee = new_price.fixed_fee
          price.save()
