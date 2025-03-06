from functools import lru_cache
from calculator.models import Scheme
from viewer.presenters.helpers import DelegatorMixin
from viewer.presenters.offence_class_presenters import offence_class_presenter_factory_from_pk
from viewer.presenters.scenario_presenters import scenario_presenter_factory_from_pk
from viewer.presenters.price_presenters import price_presenter_factory
from viewer.presenters.london_rates_apply_presenter import london_rates_apply_from_bool


def scheme_presenter_factory_from_pk(pk, params={}):
    return SchemePresenter(
        Scheme.objects.get(pk=pk),
        selected_offence_class=params.get('offence_class', ''),
        selected_scenario=params.get('scenario', ''),
        selected_london_rates_apply=params.get('london_rates_apply', ''),
    )


class SchemePresenter(DelegatorMixin):
    def __init__(self, scheme=None, selected_offence_class=None,
                 selected_scenario=None, selected_london_rates_apply=None):
        self.object = scheme
        self.selected_offence_class = offence_class_presenter_factory_from_pk(selected_offence_class)
        self.selected_scenario = scenario_presenter_factory_from_pk(selected_scenario)
        self.selected_london_rates_apply = london_rates_apply_from_bool(selected_london_rates_apply)
        super().__init__(scheme)

    @property
    def base_type(self):
        """Base type of the scheme - AGFS or LGFS

        The base type of a scheme in the database is 1 (AGFS) or 2 (LGFS)
        """
        if self.object.base_type == 1:
            return 'AGFS'

        return 'LGFS'

    @property
    @lru_cache(maxsize=None)
    def prices(self):
        """Fetch list of prices for the scheme

        The prices are filtered based on the selected offence class and scenario, if present. The returned value is an
        array of presenters for the prices.
        """
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
        if self.selected_london_rates_apply is not None:
            prices = self.selected_london_rates_apply.filter(prices)

        return prices

    @property
    @lru_cache(maxsize=None)
    def prices_count(self):
        """Total number of prices for scheme

        This count is after the prices list has been filtered
        """
        return len(self._raw_prices)

    @property
    @lru_cache(maxsize=None)
    def offence_classes(self):
        """Fetch list of offence classes related to the scheme

        Returns: [
            presenter_for_offence_class_1,
            presenter_for_offence_class_2,
            ...
        ]
        """
        return sorted(list(
            map(
                lambda pair: offence_class_presenter_factory_from_pk(pair[0], count=pair[1]),
                self._tally('offence_class').items()
            )
        ))

    @property
    @lru_cache(maxsize=None)
    def scenarios(self):
        """Fetch list of scenarios related to the scheme

        Returns: [
            presenter_for_scenario_1,
            presenter_for_scenario_2,
            ...
        ]
        """
        return list(
            map(
                lambda pair: scenario_presenter_factory_from_pk(pair[0], count=pair[1]),
                self._tally('scenario').items()
            )
        )

    @lru_cache(maxsize=None)
    def _tally(self, field):
        """Tally prices bases on a field

        Count the number of prices for each value of a field.
        Returns: { 'field_value_1': count, ... }
        """
        tally = {}
        for id in self._raw_prices.values(field):
            tally[id[field]] = tally.get(id[field], 0) + 1

        return tally
