"""
Django settings for cookingnutritious project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '!ky=cibnc)z%fmit_u(#ca&ovsy!g2f_avq!_qg$y6-@bgfe+%'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates')]

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'cookingnutritious',
    'food',
    'usda',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'social.apps.django_app.default',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_extensions',
    'tinymce',
    'payments',
    'django_forms_bootstrap',
    'autocomplete_light',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'social.apps.django_app.context_processors.backends',
    'social.apps.django_app.context_processors.login_redirect',
    #'payments.context_processors.payments_settings',
)

AUTHENTICATION_BACKENDS = (
    'social.backends.facebook.FacebookOAuth2',
    'social.backends.google.GoogleOAuth2',
    #'social.backends.twitter.TwitterOAuth',
    'django.contrib.auth.backends.ModelBackend',
)

MIDDLEWARE_CLASSES = (
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'payments.middleware.ActiveSubscriptionMiddleware',
)

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/'

SOCIAL_AUTH_FACEBOOK_KEY = '522568191211208'
SOCIAL_AUTH_FACEBOOK_SECRET = '6bb58b25a208229d356e63333aa650ac'
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '135107696376-ffdf3daa11krq5jvtnhs08ucpbbn5r9j.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'kcXd3VRa98QwkG5gt3zx5LwS'
SOCIAL_AUTH_GOOGLE_OAUTH2_USE_DEPRECATED_API = True
SOCIAL_AUTH_GOOGLE_PLUS_USE_DEPRECATED_API = True

#SOCIAL_AUTH_TWITTER_KEY = 'aaAdgOUnrFpi0PEW95IwBUgwn'
#SOCIAL_AUTH_TWITTER_SECRET = '1GGzQqy3jm6Xb8Vv3AOfYU1tFaApiElnO2AA7yrLzvpbi1wNl4'

SOCIAL_AUTH_ADMIN_USER_SEARCH_FIELDS = ['username', 'first_name', 'email']

SOCIAL_AUTH_PIPELINE = (
    'social.pipeline.social_auth.social_details',
    'social.pipeline.social_auth.social_uid',
    'social.pipeline.social_auth.auth_allowed',
    'social.pipeline.social_auth.social_user',
    'social.pipeline.user.get_username',
    #'social.pipeline.mail.mail_validation',
    'social.pipeline.social_auth.associate_by_email',
    'social.pipeline.user.create_user',
    'social.pipeline.social_auth.associate_user',
    'social.pipeline.social_auth.load_extra_data',
    'social.pipeline.user.user_details'
)

SUBSCRIPTION_REQUIRED_EXCEPTION_URLS = (
    'payments_subscribe',
)

SUBSCRIPTION_REQUIRED_REDIRECT = 'payments_subscribe'

STRIPE_SECRET_KEY = os.environ.get(
    "STRIPE_SECRET_KEY",
    "sk_test_bLo1LqgqWZX1sSRuk13i78ZD"
)
STRIPE_PUBLIC_KEY = os.environ.get(
    "STRIPE_PUBLIC_KEY",
    "pk_test_hcIx0t8Z6WiRq69FaTvKj7iI"
)

PAYMENTS_PLANS = {
    "monthly-trial": {
        "stripe_plan_id": "basic-monthly-trial",
        "name": "Cooking Nutritious Basic ($10/month with 30 days free)",
        "description": "Limited API use. Unlimited Backend use. Monthly Plan.",
        "price": 10,
        "currency": "usd",
        "interval": "month",
        "trial_period_days": 30
    },
    "basic-monthly": {
        "stripe_plan_id": "basic-monthly",
        "name": "Cooking Nutritious Basic ($10/month)",
        "description": "Limited API use. Unlimited Backend use. Monthly Plan.",
        "price": 10,
        "currency": "usd",
        "interval": "month"
    },
    "basic-yearly": {
        "stripe_plan_id": "basic-yearly",
        "name": "Cooking Nutritious Basic ($79/year)",
        "description": "Limited API use. Unlimited Backend use. Yearly Plan.",
        "price": 79,
        "currency": "usd",
        "interval": "year"
    },
    "pro-monthly": {
        "stripe_plan_id": "pro-monthly",
        "name": "Cooking Nutritious Pro ($32/month)",
        "description": "Higher API use. Unlimited Backend use. Monthly Plan.",
        "price": 32,
        "currency": "usd",
        "interval": "month"
    },
    "pro-yearly": {
        "stripe_plan_id": "pro-yearly",
        "name": "Cooking Nutritious Pro ($253/year)",
        "description": "Higher API use. Unlimited Backend use. Yearly Plan.",
        "price": 253,
        "currency": "usd",
        "interval": "year"
    },
    "enterprise-monthly": {
        "stripe_plan_id": "enterprise-monthly",
        "name": "Cooking Nutritious Enterprise ($72/month)",
        "description": "Highest API use. Unlimited Backend use. Monthly Plan.",
        "price": 72,
        "currency": "usd",
        "interval": "month"
    },
    "enterprise-yearly": {
        "stripe_plan_id": "enterprise-yearly",
        "name": "Cooking Nutritious Enterprise ($570/year)",
        "description": "Highest API use. Unlimited Backend use. Yearly Plan.",
        "price": 570,
        "currency": "usd",
        "interval": "year"
    }
}

ROOT_URLCONF = 'cookingnutritious.urls'

WSGI_APPLICATION = 'cookingnutritious.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'cookingnutritious_dev',
        'USER': 'cooking',
        'PASSWORD': 'cooking',
        'HOST': 'localhost',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/' 

#STATICFILES_DIRS = (
#    os.path.join(BASE_DIR, "cookingnutritious"),
#)

STATIC_ROOT = os.path.join(BASE_DIR, "static")

REST_FRAMEWORK = {
    # Use hyperlinked styles by default.
    # Only used if the `serializer_class` attribute is not set on a view.
    'DEFAULT_MODEL_SERIALIZER_CLASS':
    'rest_framework.serializers.HyperlinkedModelSerializer',

    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissions',
    ],

    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.ScopedRateThrottle',
    ),
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/day',
    },
    'DEFAULT_RENDERER_CLASSES': ( 
        'rest_framework.renderers.JSONRenderer', 
        'rest_framework.renderers.JSONPRenderer', 
        'rest_framework.renderers.BrowsableAPIRenderer', 
    )

    #'PAGINATE_BY': 20,

}

REST_FRAMEWORK_EXTENSIONS = {
    'DEFAULT_OBJECT_CACHE_KEY_FUNC':
    'rest_framework_extensions.utils.default_object_cache_key_func',
    'DEFAULT_LIST_CACHE_KEY_FUNC':
    'rest_framework_extensions.utils.default_list_cache_key_func',
    'DEFAULT_OBJECT_ETAG_FUNC':
    'rest_framework_extensions.utils.default_object_etag_func',
    'DEFAULT_LIST_ETAG_FUNC':
    'rest_framework_extensions.utils.default_list_etag_func',
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

CORS_ORIGIN_WHITELIST = (
    'localhost:9000',
    'caloriecounter.fitness'
)

CORS_ALLOW_CREDENTIALS = True
