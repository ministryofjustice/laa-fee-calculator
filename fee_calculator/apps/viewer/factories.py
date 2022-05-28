from calculator.models import (OffenceClass)
from viewer.presenters.offence_class_presenters import (
    AlphaOffenceClassPresenter, NumericOffenceClassPresenter, NoneOffenceClassPresenter, NullOffenceClassPresenter)


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
