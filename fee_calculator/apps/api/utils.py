from functools import wraps
import datetime


def fix_advocate_category(f):
    @wraps(f)
    def decorator(request, param_name, scheme, *args, **kwargs):
        value = f(request, param_name, scheme, *args, **kwargs)

        if param_name == 'advocate_type' and value in ['QC', 'KC']:
            value = 'KC' if scheme.start_date >= datetime.date(2023, 4, 17) else 'QC'

        return value

    return decorator
