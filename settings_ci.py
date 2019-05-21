from project.settings import *


BASE_DIR = os.path.dirname(__file__)

PROJECT_NAME = 'lsns'

INSTANCE_DIR = '/tmp/' + PROJECT_NAME + '/'
create_dirs(INSTANCE_DIR)
create_dirs(INSTANCE_DIR+'sessions/')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'y#9r1u$hxrm!u*%^04ia^+tzrh3c7mxgrf29!ln-*20xo()x4$'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ADMIN_LOGIN = {'admin', 'admin@{}.com'.format(PROJECT_NAME)}
ADMIN_PASSWORD = 'pbkdf2_sha256$30000$37vfsTPxkZ2N$5JCLjrA2WWPSnqP2oHul9JFswSvHeSOLGhxw9YL6p4E='  # brian123

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
       'ENGINE': 'django.db.backends.postgresql_psycopg2',
       'NAME': 'ci',
       'USER': 'postgres',
       'PASSWORD': 'postgres',
       'HOST': 'postgres',
       'PORT': '5432',
   },
}

# Cache
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# used for mailer links
PROTOCOL = 'https'
HOST = 'localhost'
PORT = None


if DEBUG:
    # EMAIL_HOST = 'smtp.mailtrap.io'
    # EMAIL_HOST_USER = '0214920fb35621'
    # EMAIL_HOST_PASSWORD = '6239ad1f8c3275'
    # EMAIL_PORT = '2525'
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = 'smtp.sendgrid.net'
    EMAIL_PORT = 587
    EMAIL_HOST_USER = 'sendgrid_username'
    EMAIL_HOST_PASSWORD = 'sendgrid_password'
    EMAIL_USE_TLS = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
STATIC_ROOT = os.path.join(INSTANCE_DIR, 'static')
MEDIA_ROOT = os.path.join(INSTANCE_DIR, 'media')


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'skip_static_requests': {
            '()': 'django.utils.log.CallbackFilter',
            'callback': skip_static_requests
        }
    },
    'formatters': {
        'verbose': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
        'django.server': {
            '()': 'django.utils.log.ServerFormatter',
            'format': '[%(server_time)s] %(message)s',
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'formatter': 'simple'
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'file': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(INSTANCE_DIR, PROJECT_NAME+'.log'),
            'maxBytes': 1024*1024*15, # 15MB
            'backupCount': 10,
            'formatter': 'verbose'

        },
        'django.server': {
            'level': 'INFO',
            # 'filters': ['skip_static_requests'],  # <- ...with one change
            'class': 'logging.StreamHandler',
            'formatter': 'django.server',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'INFO'
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django.server': {
            'handlers': ['django.server'],
            'level': 'INFO',
            'propagate': False,
        },
        'blog': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'INFO'
        },
        'authentication': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'DEBUG'
        }

    },
}
