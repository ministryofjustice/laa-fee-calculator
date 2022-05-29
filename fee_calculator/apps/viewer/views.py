from django.shortcuts import render

from calculator.models import Scheme
from .factories import OffenceClassPresenterFactory, ScenarioPresenterFactory


def index(request):
    return render(request, 'viewer/index.html')


def fee_schemes(request):
    breadcrumbs = [{'text': 'Home', 'route': 'viewer:index'}]
    schemes = Scheme.objects.all

    return render(request, 'viewer/fee_schemes.html', {'schemes': schemes, 'breadcrumbs': breadcrumbs})


def fee_scheme(request, pk):
    breadcrumbs = [{'text': 'Home', 'route': 'viewer:index'}, {'text': 'Fee Schemes', 'route': 'viewer:fee_schemes'}]
    offence_class = request.GET.get('offence_class', '')
    scenario = request.GET.get('scenario', '')

    offence_class_factory = OffenceClassPresenterFactory()
    scenario_factory = ScenarioPresenterFactory()

    selected_offence_class = offence_class_factory.build(offence_class)
    selected_scenario = scenario_factory.build(scenario)

    scheme = Scheme.objects.get(pk=pk)
    prices = scheme.prices.prefetch_related('offence_class', 'scenario', 'advocate_type', 'fee_type', 'unit')
    prices = selected_offence_class.filter(prices)
    prices = selected_scenario.filter(prices)

    scenario_tally = {}
    offence_class_tally = {}
    for id in prices.values('scenario', 'offence_class'):
        scenario_tally[id['scenario']] = scenario_tally.get(id['scenario'], 0) + 1
        offence_class_tally[id['offence_class']] = offence_class_tally.get(id['offence_class'], 0) + 1

    scenarios = list(
        map(
            lambda pair: {
                'scenario': scenario_factory.build(pair[0], count=pair[1]),
                'count': pair[1]
            }, scenario_tally.items()
        )
    )
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
            'selected_scenario': selected_scenario,
            'selected_offence_class': selected_offence_class,
            'breadcrumbs': breadcrumbs
        }
    )
