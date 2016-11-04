import dj_database_url

from .base import *


db_from_env = dj_database_url.config()
DATABASES['default'].update(db_from_env)
