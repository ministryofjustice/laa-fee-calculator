from decimal import Decimal, InvalidOperation
from django.conf import settings
from functools import lru_cache
from rest_framework.exceptions import ValidationError
from django.db.models import Q


def basic_q_builder(param, value):
    return Q(**{param: value})


def q_builder_with_null(param, value):
    return Q(**{param: value}) | Q(**{param + '__isnull': True})


class ParamFetcher():
    def __init__(self, request, param_name, required=False, default=None, q_builder=basic_q_builder):
        self.request = request
        self.param_name = param_name
        self.required = required
        self.default = default
        self.q_builder = q_builder

    @property
    @lru_cache
    def _result(self):
        value = self.request.query_params.get(self.param_name, self.default)
        if (value is None or value == '') and self.required:
            raise ValidationError('`%s` is a required field' % self.param_name)
        return value

    @property
    def as_q(self):
        if self.present:
            return self.q_builder(self.param_name, self.call())

    @property
    def present(self):
        return self._result is not None


class ModelParamFetcher(ParamFetcher):
    def __init__(
        self, request, param_name, model_class, scheme,
        required=False, lookup='pk', many=False, default=None, q_builder=basic_q_builder
    ):
        self.scheme = scheme
        self.model_class = model_class
        self.lookup = lookup
        self.many = many

        super().__init__(request, param_name, required=required, default=default, q_builder=q_builder)

    def call(self):
        try:
            if self._result is not None and self._result != '':
                if self.many:
                    candidates = self.model_class.objects.filter(**{self.lookup: self._result})
                    if len(candidates) == 0:
                        raise self.model_class.DoesNotExist
                    else:
                        return candidates
                else:
                    return self.model_class.objects.get(**{self.lookup: self._result})
        except (self.model_class.DoesNotExist, ValueError):
            raise ValidationError(
                '\'%s\' is not a valid `%s`' % (self._result, self.param_name)
            )

    @property
    @lru_cache
    def _result(self):
        value = super()._result

        if self.param_name == 'advocate_type' and value in ['QC', 'KC']:
            value = 'KC' if self.scheme.start_date >= settings.QC_KC_CHANGE_DATE else 'QC'

        return value


class DecimalParamFetcher(ParamFetcher):
    def call(self):
        try:
            if self._result is not None and self._result != '':
                return Decimal(self._result)
        except InvalidOperation:
            raise ValidationError('`%s` must be a number' % self.param_name)
