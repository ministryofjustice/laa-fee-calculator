from functools import wraps
from django.conf import settings


def fix_advocate_category(f):
    @wraps(f)
    def decorator(request, param_name, scheme, *args, **kwargs):
        value = f(request, param_name, scheme, *args, **kwargs)

        if param_name == 'advocate_type' and value in ['QC', 'KC']:
            value = 'KC' if scheme.start_date >= settings.QC_KC_CHANGE_DATE else 'QC'

        return value

    return decorator
