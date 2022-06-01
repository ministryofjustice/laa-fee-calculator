from viewer.presenters.helpers import DelegatorMixin


class SchemePresenter(DelegatorMixin):
    def __init__(self, scheme):
        self.object = scheme

    @property
    def base_type(self):
        if self.object.base_type == 1:
            return 'AGFS'

        return 'LGFS'
