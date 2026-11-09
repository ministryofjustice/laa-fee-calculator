from decimal import Decimal

from django.core.management import BaseCommand, CommandError, call_command
from django.db.transaction import atomic

from calculator.models import FeeType, Price, ScenarioCode, Scheme


class Command(BaseCommand):
    help = 'Copy AGFS 17 prices to AGFS 18 and add its four hearing fees after loading reference fixtures'

    def handle(self, *args, **options):
        previous = Scheme.objects.get(pk=14)
        scheme = Scheme.objects.get(pk=15)
        if not previous.prices.exists():
            raise CommandError('Load scheme 17 prices before creating scheme 18')

        fees = [
            ('AGFS_SENT_ADD', 'HOUR', ('48.02', '68.94', '91.11')),
            ('AGFS_MITIG', 'DAY', ('166.00', '266.00', '400.00')),
            ('AGFS_MIT_ADD', 'HOUR', ('48.02', '68.94', '91.11')),
            ('AGFS_BAIL_APP', 'DAY', ('118.00', '176.00', '234.00')),
        ]
        scenarios = ScenarioCode.objects.filter(scheme_type=previous.base_type).order_by('scenario_id')
        grades = {'JUNIOR': 0, 'LEADJR': 1, 'KC': 2}

        with atomic():
            if not scheme.prices.exists():
                call_command('copyscheme', previous.pk, scheme.pk)

            for code, unit, rates in fees:
                fee_type = FeeType.objects.get(code=code)
                scheme.prices.filter(fee_type=fee_type).exclude(advocate_type_id__in=grades).delete()
                for scenario in scenarios:
                    for grade, rate_index in grades.items():
                        rate = Decimal(rates[rate_index])
                        Price.objects.update_or_create(
                            scheme=scheme,
                            scenario_id=scenario.scenario_id,
                            advocate_type_id=grade,
                            offence_class=None,
                            fee_type=fee_type,
                            unit_id=unit,
                            defaults={
                                'fixed_fee': rate if unit == 'DAY' else Decimal('0'),
                                'fee_per_unit': rate if unit == 'HOUR' else Decimal('0'),
                                'limit_from': 1,
                                'limit_to': None,
                                'strict_range': False,
                            },
                        )

        self.stdout.write(self.style.SUCCESS(f'AGFS scheme 18 has {scheme.prices.count()} prices'))
