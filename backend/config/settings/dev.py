import sys
from .bases_setting import *
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

DATABASES = {
    'default': {
        # 'ENGINE': 'mssql',
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / "db.sqlite3",
        'USER': 'sa',
        'PASSWORD': '123456',
        'HOST': 'LAPTOP-6R6QNJFA\\MSSQLSERVER1',
        'PORT': '1433',
        "TEST": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": ":memory:",
        },
    }
}
if 'pytest' in sys.modules:
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db_test.sqlite3',
    }
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
]
INSTALLED_APPS=[
    "django.contrib.admin",
    "django.contrib.auth",  
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",


    "apps.conferences",
    "apps.submissions",
    "apps.reviews.apps.ReviewsConfig",
    "rest_framework",
    "corsheaders",
]
WSGI_APPLICATION = 'config.wsgi.application'
CORS_ALLOW_ALL_ORIGINS = True
