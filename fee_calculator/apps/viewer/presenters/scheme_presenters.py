from functools import lru_cache
from calculator.models import Scheme
from viewer.presenters.helpers import DelegatorMixin
from viewer.presenters.offence_class_presenters import offence_class_presenter_factory_from_pk
from viewer.presenters.scenario_presenters import scenario_presenter_factory_from_pk
from viewer.presenters.price_presenters import price_presenter_factory


def scheme_presenter_factory_from_pk(pk, params={}):
    return SchemePresenter(
        Scheme.objects.get(pk=pk),
        selected_offence_class=params.get('offence_class', ''),
        selected_scenario=params.get('scenario', '')
    )


class SchemePresenter(DelegatorMixin):
    def __init__(self, scheme, factories={}, selected_offence_class=None, selected_scenario=None):
        self.object = scheme
        self.factories = factories
        self.selected_offence_class = offence_class_presenter_factory_from_pk(selected_offence_class)
        self.selected_scenario = scenario_presenter_factory_from_pk(selected_scenario)

    @property
    def base_type(self):
        if self.object.base_type == 1:
            return 'AGFS'

        return 'LGFS'

    def _build_with_factory(self, factory, key):
        if factory in self.factories is not None:
            return self.factories[factory].build(key)

    @property
    @lru_cache(maxsize=None)
    def prices(self):
        return list(map(lambda price: price_presenter_factory(price), list(self._raw_prices)))

    @property
    @lru_cache(maxsize=None)
    def _raw_prices(self):
        prices = self.object.prices.prefetch_related(
            'offence_class', 'scenario', 'advocate_type', 'fee_type', 'unit').all()
        if self.selected_offence_class is not None:
            prices = self.selected_offence_class.filter(prices)
        if self.selected_scenario is not None:
            prices = self.selected_scenario.filter(prices)

        return prices

    @property
    @lru_cache(maxsize=None)
    def prices_count(self):
        return len(self._raw_prices)

    @property
    @lru_cache(maxsize=None)
    def offence_classes(self):
        return sorted(list(
            map(
                lambda pair: {
                    'offence_class': offence_class_presenter_factory_from_pk(pair[0], count=pair[1]),
                    'count': pair[1]
                }, self._tally('offence_class').items()
            )
        ), key=lambda item: item['offence_class'])

    @property
    @lru_cache(maxsize=None)
    def scenarios(self):
        return list(
            map(
                lambda pair: {
                    'scenario': scenario_presenter_factory_from_pk(pair[0], count=pair[1]),
                    'count': pair[1]
                }, self._tally('scenario').items()
            )
        )

    @lru_cache(maxsize=None)
    def _tally(self, field):
        tally = {}
        for id in self._raw_prices.values(field):
            tally[id[field]] = tally.get(id[field], 0) + 1

        return tally
