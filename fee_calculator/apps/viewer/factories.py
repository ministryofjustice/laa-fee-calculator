from functools import lru_cache

from calculator.models import (OffenceClass, Scenario, Scheme)
from viewer.presenters.offence_class_presenters import (
    AlphaOffenceClassPresenter, NumericOffenceClassPresenter, NoneOffenceClassPresenter, NullOffenceClassPresenter)
from viewer.presenters.scenario_presenters import (
    ScenarioPresenter, InterimScenarioPresenter, WarrantScenarioPresenter, NoneScenarioPresenter, NullScenarioPresenter)
from viewer.presenters.scheme_presenters import SchemePresenter


class OffenceClassPresenterFactory():
    def build(self, pk, count=None):
        if pk == '':
            return NullOffenceClassPresenter(count=count)
        if pk is None or pk == 'None':
            return NoneOffenceClassPresenter(count=count)

        try:
            return self.__presenterClass(pk)(OffenceClass.objects.get(pk=pk), count=count)
        except OffenceClass.DoesNotExist:
            return NoneOffenceClassPresenter(count=count)

    def __presenterClass(self, pk):
        try:
            float(pk)
            return NumericOffenceClassPresenter
        except ValueError:
            return AlphaOffenceClassPresenter


class ScenarioPresenterFactory():
    def build(self, pk, count=None):
        if pk == '':
            return NullScenarioPresenter(count=count)
        if pk is None or pk == 'None':
            return NoneScenarioPresenter(count=count)

        try:
            return self.build_from_scenario(Scenario.objects.get(pk=pk))
        except Scenario.DoesNotExist:
            return NoneScenarioPresenter(count=count)

    def build_from_scenario(self, scenario):
        if (scenario.name.startswith('Interim payment - ')):
            return InterimScenarioPresenter(scenario)
        if (scenario.name.startswith('Warrant issued - ')):
            return WarrantScenarioPresenter(scenario)

        return ScenarioPresenter(scenario)


class SchemePresenterFactory():
    def build_from_pk(self, pk, params={}):
        return SchemePresenter(
            Scheme.objects.get(pk=pk),
            factories={'offence_class': self._offence_class_factory, 'scenario': self._scenario_factory},
            selected_offence_class=params.get('offence_class', ''),
            selected_scenario=params.get('scenario', '')
        )

    @property
    @lru_cache(maxsize=None)
    def _offence_class_factory(self):
        return OffenceClassPresenterFactory()

    @property
    @lru_cache(maxsize=None)
    def _scenario_factory(self):
        return ScenarioPresenterFactory()
