from abc import ABC, abstractmethod
import re

from viewer.presenters.helpers import DelegatorMixin
from calculator.models import Scenario


def scenario_presenter_factory_from_pk(pk, count=None):
    if pk == '':
        return NullScenarioPresenter(count=count)
    if pk is None or pk == 'None':
        return NoneScenarioPresenter(count=count)

    try:
        return scenario_presenter_factory(Scenario.objects.get(pk=pk), count=count)
    except Scenario.DoesNotExist:
        return NoneScenarioPresenter(count=count)


def scenario_presenter_factory(scenario, count=None):
    if (scenario.name.startswith('Interim payment - ')):
        return InterimScenarioPresenter(scenario=scenario, count=count)
    if (scenario.name.startswith('Warrant issued - ')):
        return WarrantScenarioPresenter(scenario=scenario, count=count)

    return ScenarioPresenter(scenario, count=count)


class AbstractScenarioPresenter(ABC):
    def __init__(self, scenario=None, count=None):
        self.scenario = scenario
        self.count = count

    @property
    @abstractmethod
    def label(self):
        pass

    @property
    @abstractmethod
    def display_name(self):
        pass

    @property
    @abstractmethod
    def isNull(self):
        pass

    @property
    @abstractmethod
    def case_type(self):
        pass

    @abstractmethod
    def filter(self, collection):
        pass


class ScenarioPresenter(AbstractScenarioPresenter, DelegatorMixin):
    @property
    def label(self):
        return str(self.scenario.pk)

    @property
    def display_name(self):
        if self.count is None:
            return self.scenario.name

        return '%s (%i)' % (self.scenario.name, self.count)

    @property
    def isNull(self):
        return False

    @property
    def case_type(self):
        return self.scenario.name

    def filter(self, collection):
        return collection.filter(scenario=self.scenario)


class InterimScenarioPresenter(ScenarioPresenter):
    @property
    def case_type(self):
        match = re.search('(?<=- )[^\s]*', self.scenario.name)
        return match.group(0).strip().capitalize()


class WarrantScenarioPresenter(ScenarioPresenter):
    @property
    def case_type(self):
        match = re.search('(?<=- )[^\(]*', self.scenario.name)
        return match.group(0).strip().capitalize()


class NoneScenarioPresenter(AbstractScenarioPresenter):
    @property
    def label(self):
        return 'None'

    @property
    def display_name(self):
        if self.count is None:
            return '[None]'

        return '[None] (%i)' % (self.count)

    @property
    def isNull(self):
        return False

    @property
    def case_type(self):
        return '[None]'

    def filter(self, collection):
        return collection.filter(scenario=None)


class NullScenarioPresenter(AbstractScenarioPresenter):
    @property
    def label(self):
        return ''

    @property
    def display_name(self):
        return '-'

    @property
    def isNull(self):
        return True

    @property
    def case_type(self):
        return '-'

    def filter(self, collection):
        return collection.all()
