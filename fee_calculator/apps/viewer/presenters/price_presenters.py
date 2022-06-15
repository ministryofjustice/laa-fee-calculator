from abc import ABC, abstractmethod

from viewer.presenters.helpers import DelegatorMixin


def price_presenter_factory(price):
    """
    Generate a presenter for the price
    """
    return PricePresenter(price)


class PricePresenter:
    def __init__(self, price=None):
        self.price = price

    def title(self):
        return '%s | %s | %s' % (self.price.advocate_type, self.price.offence_class, self.price.fee_type)
