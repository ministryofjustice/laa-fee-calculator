from functools import wraps


def fix_advocate_category(f):
    @wraps(f)
    def decorator(request, param_name, *args, **kwargs):
        value = f(request, param_name, *args, **kwargs)

        if param_name == 'advocate_type' and value == 'KC':
            value = 'QC'

        return value

    return decorator
