from abc import ABC, abstractmethod
from functools import total_ordering
from calculator.models import OffenceClass

from viewer.presenters.helpers import DelegatorMixin


def offence_class_presenter_factory_from_pk(pk, count=None):
    """Create an instance of an offence class presenter from a pk

    Given the pk of an instance of OffenceClass return the correct presenter;

    * For ''; return NullOffenceClassPresenter
      This is for when no offence class has been chosen from the web interface
    * For None or 'None'; return an instance of NoneOffenceClassPresenter
      This is for when a price has no offence class
    * For an unknown value of pk; return a NoneOffenceClassPresenter
    * For a fee scheme 9 style pk (single letter frm A to K); return an AlphaOffenceClassPresenter
    * for a fee scheme 10+ style pk (eg, 3.4); return a NumericOffenceClassPresenter
    """
    if pk == '':
        return NullOffenceClassPresenter(count=count)
    if pk is None or pk == 'None':
        return NoneOffenceClassPresenter(count=count)
    try:
        return _presenter_class(pk)(OffenceClass.objects.get(pk=pk), count=count)
    except OffenceClass.DoesNotExist:
        return NoneOffenceClassPresenter(count=count)


def _presenter_class(pk):
    try:
        float(pk)
    except ValueError:
        return AlphaOffenceClassPresenter
    else:
        return NumericOffenceClassPresenter


class AbstractOffenceClassPresenter(DelegatorMixin, ABC):
    def __init__(self, offence_class=None, count=None):
        self.offence_class = offence_class
        self.count = count
        super().__init__(offence_class)

    @property
    @abstractmethod
    def label(self):
        """
        The label to be used in a form
        """
        pass

    @property
    @abstractmethod
    def display_name(self):
        """
        The name as it should be displayed
        """
        pass

    @property
    @abstractmethod
    def isNull(self):
        """
        Is the null class?
        """
        pass

    @abstractmethod
    def filter(self, collection):
        """
        Filter collection for prices with this offence class
        """
        pass


class OffenceClassPresenter(AbstractOffenceClassPresenter):
    @property
    def label(self):
        return self.offence_class.id

    @property
    def isNull(self):
        return False

    def filter(self, collection):
        return collection.filter(offence_class=self.offence_class)

    def __eq__(self, other):
        return self.offence_class == other.offence_class


@total_ordering
class AlphaOffenceClassPresenter(OffenceClassPresenter):
    @property
    def display_name(self):
        if self.count is None:
            return '[%s] %s' % (self.offence_class.id, self.offence_class.description)

        return '[%s] %s (%i)' % (self.offence_class.id, self.offence_class.description, self.count)

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
            return '%s' % (self.offence_class.name)

        return '%s (%i)' % (self.offence_class.name, self.count)

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
