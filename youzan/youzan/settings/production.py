import os

from youzan.settings.local import BASE_DIR
from .base import *

SECRET_KEY = os.environ.get('SECRET_KEY')
DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
