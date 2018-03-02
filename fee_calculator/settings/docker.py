from .base import *  # noqa

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

ALLOWED_HOSTS = [
    'localhost',
    '.dsd.io',
]
