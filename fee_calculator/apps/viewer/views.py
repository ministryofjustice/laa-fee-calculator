from django.shortcuts import render

from calculator.models import Scheme, Scenario
from viewer.factories import OffenceClassPresenterFactory, ScenarioPresenterFactory, SchemePresenterFactory


def index(request):
    return render(request, 'viewer/index.html')


def fee_schemes(request):
    breadcrumbs = [{'text': 'Home', 'route': 'viewer:index'}]
    schemes = Scheme.objects.all

    return render(request, 'viewer/fee_schemes.html', {'schemes': schemes, 'breadcrumbs': breadcrumbs})


def fee_scheme(request, pk):
    breadcrumbs = [{'text': 'Home', 'route': 'viewer:index'}, {'text': 'Fee Schemes', 'route': 'viewer:fee_schemes'}]

    offence_class_factory = OffenceClassPresenterFactory()
    scenario_factory = ScenarioPresenterFactory()
    scheme_factory = SchemePresenterFactory()

    scheme = scheme_factory.build_from_pk(pk=pk, params=request.GET)

    scenario_tally = {}
    offence_class_tally = {}
    for id in scheme.prices.values('scenario', 'offence_class'):
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
            'scenarios': scenarios,
            'offence_classes': offence_classes,
            'breadcrumbs': breadcrumbs
        }
    )


def scenarios(request):
    breadcrumbs = [{'text': 'Home', 'route': 'viewer:index'}]
    scenario_factory = ScenarioPresenterFactory()
    scenarios = list(map(lambda scenario: scenario_factory.build_from_scenario(scenario), Scenario.objects.all()))

    return render(request, 'viewer/scenarios.html', {'scenarios': scenarios, 'breadcrumbs': breadcrumbs})
