from abc import ABC, abstractmethod

from viewer.presenters.helpers import DelegatorMixin


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

    def filter(self, collection):
        return collection.filter(scenario=self.scenario)


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

    def filter(self, collection):
        return collection.all()
