# -*- coding: utf-8 -*-
import csv
import shutil
import os
import decimal
from tempfile import NamedTemporaryFile

from django.conf import settings
from django.core.management import BaseCommand

from calculator.models import Price


class Command(BaseCommand):
    help = '''
        Update test data for cracked trial "advocate fee" prices for scheme 12 to be 100% of equivalent
        fee for a trial. WARNING: arguments are hardcode as a one off job.
    '''

    def handle(self, *args, **options):
        filename = os.path.join(
            settings.BASE_DIR,
            'apps/calculator/tests/data/test_dataset_agfs_12.csv'
        )

        temp_file = NamedTemporaryFile(delete=False, mode='w')

        with open(filename, 'r') as csv_file, temp_file:
            reader = csv.DictReader(csv_file)
            field_names = 'CASE_ID,PERSON_TYPE,BILL_TYPE,BILL_SUB_TYPE,REP_ORD_DATE,BILL_SCENARIO_ID,OFFENCE_CATEGORY,TRIAL_LENGTH,PPE,NO_DEFENDANTS,CALC_FEE_EXC_VAT,CALC_FEE_VAT,THIRD_CRACKED,NUM_OF_WITNESSES,NUM_OF_CASES,QUANTITY,NUM_ATTENDANCE_DAYS,RETRIAL,MONTHS'.split(',')
            writer = csv.DictWriter(
                temp_file, fieldnames=field_names, lineterminator='\n')
            writer.writeheader()

            for row in reader:
                if row['BILL_SCENARIO_ID'] == '2784':
                    new_price = Price.objects \
                        .get(scheme_id=5,
                             scenario_id=4,
                             fee_type_id=34,
                             advocate_type_id=row['PERSON_TYPE'],
                             offence_class_id=row['OFFENCE_CATEGORY'],
                             fixed_fee__gt=0
                             )
                    print(
                        f"bill test scenario id: {row['BILL_SCENARIO_ID']}, bill_sub_type: {row['BILL_SUB_TYPE']}, advocate_type_id: {row['PERSON_TYPE']}, offence_class_id: {row['OFFENCE_CATEGORY']}, fixed_fee: {row['CALC_FEE_EXC_VAT']} => {new_price.fixed_fee}")

                    row['REP_ORD_DATE'] = '17/09/2020'
                    row['CALC_FEE_EXC_VAT'] = str(
                        round(new_price.fixed_fee, 0))
                    row['CALC_FEE_VAT'] = str(
                        round(decimal.Decimal('0.2') * new_price.fixed_fee, 2))

                writer.writerow(row)

            shutil.move(temp_file.name, filename)
