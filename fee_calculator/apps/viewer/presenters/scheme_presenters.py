from functools import lru_cache
from viewer.presenters.helpers import DelegatorMixin


class SchemePresenter(DelegatorMixin):
    def __init__(self, scheme, factories={}, selected_offence_class=None, selected_scenario=None):
        self.object = scheme
        self.factories = factories
        self.selected_offence_class = self._build_with_factory('offence_class', selected_offence_class)
        self.selected_scenario = self._build_with_factory('scenario', selected_scenario)

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
        return self.prices.count()

    @property
    @lru_cache(maxsize=None)
    def offence_classes(self):
        return sorted(list(
            map(
                lambda pair: {
                    'offence_class': self.factories['offence_class'].build(pair[0], count=pair[1]),
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
                    'scenario': self.factories['scenario'].build(pair[0], count=pair[1]),
                    'count': pair[1]
                }, self._tally('scenario').items()
            )
        )

    @lru_cache(maxsize=None)
    def _tally(self, field):
        tally = {}
        for id in self.prices.values(field):
            tally[id[field]] = tally.get(id[field], 0) + 1

        return tally
