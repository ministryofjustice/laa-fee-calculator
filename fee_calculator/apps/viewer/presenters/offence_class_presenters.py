from abc import ABC, abstractmethod
from functools import total_ordering

from viewer.presenters.helpers import DelegatorMixin


class AbstractOffenceClassPresenter(ABC):
    def __init__(self, offence_class=None, count=None):
        self.object = offence_class
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


class OffenceClassPresenter(AbstractOffenceClassPresenter, DelegatorMixin):
    @property
    def label(self):
        return self.object.id

    @property
    def isNull(self):
        return False

    def filter(self, collection):
        return collection.filter(offence_class=self.object)

    def __eq__(self, other):
        return self.object == other.object


@total_ordering
class AlphaOffenceClassPresenter(OffenceClassPresenter):
    @property
    def display_name(self):
        if self.count is None:
            return '[%s] %s' % (self.object.id, self.object.description)

        return '[%s] %s (%i)' % (self.object.id, self.object.description, self.count)

    def __lt__(self, other):
        if isinstance(other, (NoneOffenceClassPresenter, NullOffenceClassPresenter)):
            return False

        if isinstance(other, NumericOffenceClassPresenter):
            return True

        return self.id < other.id

    def __gt__(self, other):
        return isinstance(other, (NoneOffenceClassPresenter, NullOffenceClassPresenter)) or other < self


@total_ordering
class NumericOffenceClassPresenter(OffenceClassPresenter):
    @property
    def display_name(self):
        if self.count is None:
            return '%s' % (self.object.name)

        return '%s (%i)' % (self.object.name, self.count)

    def __lt__(self, other):
        if isinstance(other, (AlphaOffenceClassPresenter, NoneOffenceClassPresenter, NullOffenceClassPresenter)):
            return False

        return float(self.id) < float(other.id)

    def __gt__(self, other):
        return isinstance(
            other,
            (AlphaOffenceClassPresenter, NoneOffenceClassPresenter, NullOffenceClassPresenter)
        ) or other < self


@total_ordering
class NoneOffenceClassPresenter(AbstractOffenceClassPresenter):
    @property
    def label(self):
        return 'None'

    @property
    def display_name(self):
        return '[None] (%i)' % self.count if self.count is not None else '[None]'

    @property
    def id(self):
        return 'None'

    @property
    def name(self):
        return '(None)'

    @property
    def description(self):
        return '(None)'

    @property
    def isNull(self):
        False

    def filter(self, collection):
        return collection.filter(offence_class=None)

    def __lt__(self, other):
        return isinstance(other, OffenceClassPresenter)

    def __eq__(self, other):
        return isinstance(other, NoneOffenceClassPresenter)


@total_ordering
class NullOffenceClassPresenter(AbstractOffenceClassPresenter):
    @property
    def label(self):
        return ''

    @property
    def display_name(self):
        return '-'

    @property
    def id(self):
        return '-'

    @property
    def name(self):
        return '-'

    @property
    def description(self):
        return '-'

    @property
    def isNull(self):
        return True

    def filter(self, collection):
        return collection.all()

    def __lt__(self, other):
        return True

    def __eq__(self, other):
        return isinstance(other, NullOffenceClassPresenter)
