from abc import ABC, abstractmethod

from viewer.presenters.helpers import DelegatorMixin


def price_presenter_factory(price):
    """
    Generate a presenter for the price
    """
    return PricePresenter(price)


class AbstractPricePresenter(ABC):
    def __init__(self, price=None):
        self.object = price

    @abstractmethod
    def title(self):
        """
        The display title of the price
        """
        pass


class PricePresenter(AbstractPricePresenter, DelegatorMixin):
    def title(self):
        return '%s | %s | %s' % (self.object.advocate_type, self.object.offence_class, self.object.fee_type)
