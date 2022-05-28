from django.shortcuts import render

from calculator.models import (Scenario, Scheme)
from .factories import OffenceClassPresenterFactory


def index(request):
    return render(request, 'viewer/index.html')


def fee_schemes(request):
    schemes = Scheme.objects.all

    return render(request, 'viewer/fee_schemes.html', {'schemes': schemes})


def fee_scheme(request, pk):
    offence_class = request.GET.get('offence_class', '')

    offence_class_factory = OffenceClassPresenterFactory()
    selected_offence_class = offence_class_factory.build(offence_class)

    scheme = Scheme.objects.get(pk=pk)
    prices = selected_offence_class.filter(scheme.prices)

    scenario_tally = {}
    offence_class_tally = {}
    for id in prices.values('scenario', 'offence_class'):
        scenario_tally[id['scenario']] = scenario_tally.get(id['scenario'], 0) + 1
        offence_class_tally[id['offence_class']] = offence_class_tally.get(id['offence_class'], 0) + 1

    scenarios = sorted(list(
        map(lambda pair: {'scenario': Scenario.objects.get(pk=pair[0]), 'count': pair[1]}, scenario_tally.items())
    ), key=lambda item: item['scenario'].name)
    offence_classes = sorted(list(
        map(
            lambda pair: {
                'offence_class': offence_class_factory.build(pair[0], count=pair[1]),
                'count': pair[1]
            }, offence_class_tally.items()
        )
    ), key=lambda item: item['offence_class'])

    return render(
        request,
        'viewer/fee_scheme.html',
        {
            'scheme': scheme,
            'prices_count': prices.count(),
            'prices': prices,
            'scenarios': scenarios,
            'offence_classes': offence_classes,
            'selected_offence_class': selected_offence_class
        }
    )
