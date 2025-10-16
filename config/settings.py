from pathlib import Path
from decouple import config
from django.urls import reverse_lazy


BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = config("SECRET_KEY")

DEBUG = config("DEBUG")

ALLOWED_HOSTS = ["*"]


INSTALLED_APPS = [
    'unfold',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # extra
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',

    # local apps
    'users',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


AUTH_PASSWORD_VALIDATORS = [
   
]


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


LOGIN_URL = "/hemis/"

# static files
STATIC_URL = 'static/'
STATIC_ROOT = "static"

# media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# user model
AUTH_USER_MODEL = "users.User"

# rest framework
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": ["rest_framework.authentication.TokenAuthentication", ],
}

# csrf
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
CSRF_TRUSTED_ORIGINS = ["https://api.practicum.uzfi.uz", "http://localhost:8000"]
if not DEBUG:
    SESSION_COOKIE_DOMAIN = ".practicum.uzfi.uz"
    CSRF_COOKIE_DOMAIN = ".practicum.uzfi.uz"
    CSRF_COOKIE_SECURE = True


UNFOLD = {
    "SITE_TITLE": "Admin Panel",
    "SITE_HEADER": "Practicum Control",
    "SITE_SUBHEADER": "Admin Panel",
    "SITE_ICON": {
        "light": lambda request: "https://uzfi.uz/static/assets/images/uzfi.png",
        "dark": lambda request: "https://uzfi.uz/static/assets/images/uzfi.png"
    },
    "SHOW_HISTORY": True,

    "SIDEBAR": {
        "show_search": True,
        "navigation": [
            {
                "title": "Asosiy",
                "separator": True,
                "collapsable": True,
                "items": [
                    {
                        "title": "Talabalar",
                        "icon": "group",
                        "link": reverse_lazy("admin:users_user_changelist")
                    },
                    {
                        "title": "Guruhlar",
                        "icon": "group",
                        "link": reverse_lazy("admin:users_group_changelist")
                    },
                    {
                        "title": "Dars jadvali",
                        "icon": "group",
                        "link": reverse_lazy("admin:users_schedule_changelist")
                    },
                    {
                        "title": "Joylashuvlar",
                        "icon": "location_on",
                        "link": reverse_lazy("admin:users_area_changelist")
                    },
                    {
                        "title": "Topshiriqlar",
                        "icon": "add_task",
                        "link": reverse_lazy("admin:users_task_changelist")
                    },
                    {
                        "title": "Yuklamalar",
                        "icon": "file_present",
                        "link": reverse_lazy("admin:users_submit_changelist")
                    },
                    {
                        "title": "Davomat",
                        "icon": "more_time",
                        "link": reverse_lazy("admin:users_attendance_changelist")
                    },
                    {
                        "title": "Guruhlar",
                        "icon": "shield",
                        "link": reverse_lazy("admin:auth_group_changelist"),
                        "permission": lambda request: request.user.is_superuser
                    }
                ]
            }
        ]
    }
}

