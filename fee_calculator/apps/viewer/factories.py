from calculator.models import (OffenceClass, Scenario)
from viewer.presenters.offence_class_presenters import (
    AlphaOffenceClassPresenter, NumericOffenceClassPresenter, NoneOffenceClassPresenter, NullOffenceClassPresenter)
from viewer.presenters.scenario_presenters import (ScenarioPresenter, NoneScenarioPresenter, NullScenarioPresenter)


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
            return ScenarioPresenter(Scenario.objects.get(pk=pk))
        except Scenario.DoesNotExist:
            return NoneScenarioPresenter(count=count)
