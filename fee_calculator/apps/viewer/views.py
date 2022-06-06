from django.shortcuts import render

from calculator.models import Scheme, Scenario
from viewer.factories import ScenarioPresenterFactory, SchemePresenterFactory


def index(request):
    return render(request, 'viewer/index.html')


def fee_schemes(request):
    breadcrumbs = [{'text': 'Home', 'route': 'viewer:index'}]
    schemes = Scheme.objects.all

    return render(request, 'viewer/fee_schemes.html', {'schemes': schemes, 'breadcrumbs': breadcrumbs})


def fee_scheme(request, pk):
    breadcrumbs = [{'text': 'Home', 'route': 'viewer:index'}, {'text': 'Fee Schemes', 'route': 'viewer:fee_schemes'}]
    scheme = SchemePresenterFactory().build_from_pk(pk=pk, params=request.GET)

    return render(
        request,
        'viewer/fee_scheme.html',
        {
            'scheme': scheme,
            'breadcrumbs': breadcrumbs
        }
    )


def scenarios(request):
    breadcrumbs = [{'text': 'Home', 'route': 'viewer:index'}]
    scenario_factory = ScenarioPresenterFactory()
    scenarios = list(map(lambda scenario: scenario_factory.build_from_scenario(scenario), Scenario.objects.all()))

    return render(request, 'viewer/scenarios.html', {'scenarios': scenarios, 'breadcrumbs': breadcrumbs})
