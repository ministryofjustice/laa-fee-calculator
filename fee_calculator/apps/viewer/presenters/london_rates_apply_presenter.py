def london_rates_apply_from_bool(bool):
    if bool == '':
        return NullPresenter()
    if bool == 'true':
        return TruePresenter()
    else:
        return FalsePresenter()


class NullPresenter:
    @property
    def label(self):
        return ''

    @property
    def isNull(self):
        return True

    def filter(self, collection):
        return collection.all()


class TruePresenter:
    @property
    def label(self):
        return 'True'

    @property
    def isNull(self):
        return False

    def filter(self, collection):
        return collection.filter(london_rates_apply=True)


class FalsePresenter:
    @property
    def label(self):
        return 'True'

    @property
    def isNull(self):
        return False

    def filter(self, collection):
        return collection.filter(london_rates_apply=False)
