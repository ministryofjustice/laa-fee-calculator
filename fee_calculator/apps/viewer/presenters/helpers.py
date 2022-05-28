class DelegatorMixin():
    def __getattr__(self, name):
        return getattr(self.object, name)
