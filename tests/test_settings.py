import os

BASE_DIR = os.path.dirname(__file__)

SECRET_KEY = 'secretkey'

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'wt_templatetags'
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': ':memory:'}}

USE_TZ = True
