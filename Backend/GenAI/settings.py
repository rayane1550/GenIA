from pathlib import Path

from datetime import timedelta

import json

from urllib.request import urlopen



BASE_DIR = Path(__file__).resolve().parent.parent



SECRET_KEY = 'django-insecure-^$#b-yihdqq%p_rnjro@+s_&q=6#w$f6@88d#7x++(_=$yb%bw'



DEBUG = True



ALLOWED_HOSTS = ['*'] #192.168.0.10 → outra máquina da rede acessando o backend, 127.0.0.1 → sua própria máquina, localhost → sua própria máquina







AUTH0_DOMAIN = "geniatcc.uk.auth0.com"

AUTH0_API_AUDIENCE = "fcNck2hsBvG8G6UJZBeSX7AyLVnQpik8"

AUTH0_ALGORITHMS = ["RS256"]







REST_FRAMEWORK = {

    'DEFAULT_AUTHENTICATION_CLASSES': (

        'rest_framework_simplejwt.authentication.JWTAuthentication',

        'Api.authentication.Auth0JWTAuthentication',

   

    ),

}



AUTHENTICATION_BACKENDS = [

    'django.contrib.auth.backends.ModelBackend',

    'allauth.account.auth_backends.AuthenticationBackend',

]





INSTALLED_APPS = [

    'django.contrib.admin',

    'django.contrib.auth',

    'django.contrib.contenttypes',

    'django.contrib.sessions',

    'django.contrib.staticfiles',

    'django.contrib.sites',

    'Api',

    "corsheaders",

    'rest_framework_simplejwt',

    'django_filters',

    'django.contrib.messages',

    'rest_framework',

    'rest_framework.authtoken',



    'allauth',

    'allauth.account',

    'allauth.socialaccount',



    'allauth.socialaccount.providers.google',

]



SITE_ID = 1



REST_FRAMEWORK = {

    'DEFAULT_AUTHENTICATION_CLASSES': (

        'rest_framework_simplejwt.authentication.JWTAuthentication',

    ),

    'DEFAULT_FILTER_BACKENDS': (

        'django_filters.rest_framework.DjangoFilterBackend',

    ),

}



SIMPLE_JWT = { # Configurações do JWT servem para controlar a validade dos tokens de acesso e refresh

    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),

    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),

    'ALGORITHM': 'RS256',

    'JWK_URL': f'https://{AUTH0_DOMAIN}/.well-known/jwks.json',

    'AUDIENCE': AUTH0_API_AUDIENCE,

    'ISSUER': f'https://{AUTH0_DOMAIN}/',

    'USER_ID_FIELD': 'username',

    'USER_ID_CLAIM': 'sub',

}



MIDDLEWARE = [

    'corsheaders.middleware.CorsMiddleware',

    'django.middleware.security.SecurityMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',

    'django.middleware.common.CommonMiddleware',





    'django.middleware.csrf.CsrfViewMiddleware',

    'django.contrib.auth.middleware.AuthenticationMiddleware',





    'django.contrib.messages.middleware.MessageMiddleware',

    'django.middleware.clickjacking.XFrameOptionsMiddleware',



    'allauth.account.middleware.AccountMiddleware',

]



CORS_ALLOW_ALL_ORIGINS = True

CORS_ALLOW_CREDENTIALS = True



ROOT_URLCONF = 'GenAI.urls'



TEMPLATES = [

    {

        'BACKEND': 'django.template.backends.django.DjangoTemplates',

        'DIRS': [],

        'APP_DIRS': True,

        'OPTIONS': {

            'context_processors': [

                'django.template.context_processors.request',

                'django.contrib.auth.context_processors.auth',

                'django.contrib.messages.context_processors.messages',

                'django.contrib.messages.context_processors.messages',

            ],

        },

    },

]



WSGI_APPLICATION = 'GenAI.wsgi.application'


SOCIALACCOUNT_LOGIN_ON_GET = True
LOGIN_REDIRECT_URL = 'http://localhost:5173/' # Ou a URL do seu React


# Database

# https://docs.djangoproject.com/en/6.0/ref/settings/#databases



DATABASES = {

    'default': {

        'ENGINE': 'django.db.backends.sqlite3',

        'NAME': BASE_DIR / 'db.sqlite3',

    }

}





# Password validation

# https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators



AUTH_PASSWORD_VALIDATORS = [

    {

        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',

    },

    {

        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',

    },

    {

        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',

    },

    {

        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',

    },

]





# Internationalization

# https://docs.djangoproject.com/en/6.0/topics/i18n/



LANGUAGE_CODE = 'en-us'



TIME_ZONE = 'UTC'



USE_I18N = True



USE_TZ = True





# Static files (CSS, JavaScript, Images)

# https://docs.djangoproject.com/en/6.0/howto/static-files/



STATIC_URL = 'static/'



CORS_ALLOWED_ORIGINS = [

    "http://localhost:5173",
    "http://127.0.0.1:5173",


]

# Obriga o Django a jogar o e-mail no console do terminal em vez de enviar de verdade
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Desativa completamente a necessidade de confirmar e-mail para registrar usuários
ACCOUNT_EMAIL_VERIFICATION = 'none'
ACCOUNT_EMAIL_REQUIRED = True