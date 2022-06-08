"""Mixin to allow functions and properties to be delegated

Any calls to an unknown class function will be delegated to self.object. For example;

class NewClass(DelegatorMixin):
    def __init__(self):
        self.object = OtherClass()

x = NewClass()

# This will call x.object.boo():
x.boo()
"""


class DelegatorMixin():
    def __getattr__(self, name):
        return getattr(self.object, name)
