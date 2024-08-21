from django.shortcuts import render
from django.views.decorators.http import require_GET
from django.http import Http404

from calculator.models import Scheme, Scenario
from viewer.presenters.scheme_presenters import scheme_presenter_factory_from_pk
from viewer.presenters.scenario_presenters import scenario_presenter_factory


@require_GET
def index(request):
    sections = [
        {'page': 'viewer:fee_schemes', 'title': 'Fee Schemes'},
        # WIP
        # {'page': 'viewer:scenarios', 'title': 'Scenarios'}
    ]

    return render(request, 'viewer/index.html', {'sections': sections})


@require_GET
def fee_schemes(request):
    breadcrumbs = [{'text': 'Home', 'route': 'viewer:index'}]
    schemes = Scheme.objects.all

    return render(request, 'viewer/fee_schemes.html', {'schemes': schemes, 'breadcrumbs': breadcrumbs})


@require_GET
def fee_scheme(request, pk):
    breadcrumbs = [{'text': 'Home', 'route': 'viewer:index'}, {'text': 'Fee Schemes', 'route': 'viewer:fee_schemes'}]
    try:
        scheme = scheme_presenter_factory_from_pk(pk=pk, params=request.GET)
    except Scheme.DoesNotExist:
        raise Http404

    prices_view = {'table': '', 'cards': ''}
    prices_view[request.GET.get('prices_view', 'table')] = 'checked'

    return render(
        request,
        'viewer/fee_scheme.html',
        {
            'scheme': scheme,
            'prices_view': prices_view,
            'breadcrumbs': breadcrumbs,
            'bool_values': ['true', 'false']
        }
    )


@require_GET
def scenarios(request):
    breadcrumbs = [{'text': 'Home', 'route': 'viewer:index'}]
    scenarios = list(map(lambda scenario: scenario_presenter_factory(scenario), Scenario.objects.all()))

    return render(request, 'viewer/scenarios.html', {'scenarios': scenarios, 'breadcrumbs': breadcrumbs})
