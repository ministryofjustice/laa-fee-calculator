from abc import ABC, abstractmethod
import re

from viewer.presenters.helpers import DelegatorMixin
from calculator.models import Scenario


def scenario_presenter_factory_from_pk(pk, count=None):
    """Create an instance of a scenario presenter from a pk

    Given the pk of an instance of Scenario return the correct presenter;

    * For ''; return NullScenarioPresenter
        This is for when no scenario has been chosen from the web interface
    * For None or 'None'; return an instance of NoneScenarioPresenter
        This is for when a price has no offence class
    * For an unknown value of pk; return a NoneScenarioPresenter
    * For a known value of pk; return a ScenarioPresenter or a child class of this

    The name field of an scenario is a combination of multiple pieces of information.
    (TODO) The presenter may be able to display the information separated out.
    """
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


class AbstractScenarioPresenter(DelegatorMixin, ABC):
    def __init__(self, scenario=None, count=None):
        self.scenario = scenario
        self.count = count
        super().__init__(scenario)

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
        """Case type of the scenario

        This can be, for example, Trial, Retrial, Cracked trial, etc
        """
        pass

    @abstractmethod
    def filter(self, collection):
        """
        Filter collection for prices with this offence class
        """
        pass


class ScenarioPresenter(AbstractScenarioPresenter):
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
        match = re.search(r'(?<=- )[^\s]*', self.scenario.name)
        return match.group(0).strip().capitalize()


class WarrantScenarioPresenter(ScenarioPresenter):
    @property
    def case_type(self):
        match = re.search(r'(?<=- )[^\(]*', self.scenario.name)
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
