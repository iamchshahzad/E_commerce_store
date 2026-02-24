"""
Django settings for e_commerce project.
"""

from pathlib import Path
from datetime import timedelta

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIST_DIR = BASE_DIR / 'frontend' / 'dist'
REACT_DEV_SERVER_URL = 'http://localhost:5173'

# -------------------------------------------------------
# Security
# -------------------------------------------------------
SECRET_KEY = 'django-insecure-g^kwl)ou&(s8jcc&ghar&o!a#z2i)@5*j%99&_^&&oci&_*5nd'
DEBUG = True
ALLOWED_HOSTS = ['*']

# -------------------------------------------------------
# Jazzmin - Modern Admin UI (NOTE: must stay before django.contrib.admin)
# Keep all strings ASCII-only to avoid encoding issues with certain editors.
# -------------------------------------------------------
JAZZMIN_SETTINGS = {
    # Branding
    "site_title": "E-Shop Admin",
    "site_header": "E-Shop",
    "site_brand": "E-Shop",
    "welcome_sign": "Welcome to E-Shop Admin Panel",
    "copyright": "E-Shop 2026",

    # Top menu links
    "topmenu_links": [
        {"name": "View Store", "url": "/", "new_window": True},
        {"model": "auth.User"},
    ],

    # User dropdown menu
    "usermenu_links": [
        {"name": "View Store", "url": "/", "new_window": True},
    ],

    # Sidebar
    "show_sidebar": True,
    "navigation_expanded": True,
    "hide_apps": [],
    "hide_models": [],
    "order_with_respect_to": [
        "products", "cart", "orders", "users", "auth",
    ],

    # Font Awesome 5 icons for each model
    "icons": {
        "auth":             "fas fa-shield-alt",
        "auth.user":        "fas fa-user",
        "auth.Group":       "fas fa-users",
        "products.Product": "fas fa-box-open",
        "products.Category":"fas fa-tags",
        "cart.Cart":        "fas fa-shopping-cart",
        "cart.CartItem":    "fas fa-list-ul",
        "orders.Order":     "fas fa-receipt",
        "users.User":       "fas fa-user-circle",
    },
    "default_icon_parents":  "fas fa-folder",
    "default_icon_children": "fas fa-dot-circle",

    # Misc UI
    "related_modal_active": True,
    "custom_css": "css/admin_custom.css",   # our extra overrides on top
    "custom_js":  None,
    "use_google_fonts_cdn": True,
    "show_ui_builder": False,

    # Use single layout - all sections always visible, no JS required
    "changeform_format": "single",
    "changeform_format_overrides": {
        "products.product": "single",
        "auth.user":        "single",
        "auth.group":       "single",
    },
}

# JAZZMIN_UI_TWEAKS = {
#     "navbar_small_text":        False,
#     "footer_small_text":        False,
#     "body_small_text":          False,
#     "brand_small_text":         False,
#     "brand_colour":             False,
#     "accent":                   "accent-purple",
#     "navbar":                   "navbar-dark",
#     "no_navbar_border":         True,
#     "navbar_fixed":             True,
#     "layout_boxed":             False,
#     "footer_fixed":             False,
#     "sidebar_fixed":            True,
#     "sidebar":                  "sidebar-dark-purple",
#     "sidebar_nav_small_text":   False,
#     "sidebar_disable_expand":   False,
#     "sidebar_nav_child_indent": True,
#     "sidebar_nav_compact_style":False,
#     "sidebar_nav_legacy_style": False,
#     "sidebar_nav_flat_style":   False,
#     "theme":                    "darkly",
#     "dark_mode_theme":          "darkly",
#     "button_classes": {
#         "primary":   "btn-primary",
#         "secondary": "btn-secondary",
#         "info":      "btn-outline-info",
#         "warning":   "btn-warning",
#         "danger":    "btn-danger",
#         "success":   "btn-success",
#     },
# }

# -------------------------------------------------------
# Applications
# -------------------------------------------------------
INSTALLED_APPS = [
    # 'jazzmin',              # must be FIRST - before django.contrib.admin
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'django_filters',
    'users',
    'products',
    'cart',
    'orders',
]

# -------------------------------------------------------
# Middleware
# -------------------------------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'e_commerce.urls'

# -------------------------------------------------------
# Templates
# -------------------------------------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # React handles storefront UI; keep template dirs empty.
        'DIRS': [],
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

WSGI_APPLICATION = 'e_commerce.wsgi.application'

# -------------------------------------------------------
# Database
# -------------------------------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'e_commerce',
        'USER': 'postgres',
        'PASSWORD': 'qwerty',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# -------------------------------------------------------
# Auth
# -------------------------------------------------------
AUTH_USER_MODEL = 'users.User'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# -------------------------------------------------------
# REST Framework & JWT
# -------------------------------------------------------
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
    ],
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME':  timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
}

# -------------------------------------------------------
# Internationalisation
# -------------------------------------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE     = 'UTC'
USE_I18N      = True
USE_TZ        = True

# -------------------------------------------------------
# Static & Media
# -------------------------------------------------------
STATIC_URL       = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
MEDIA_URL        = '/media/'
MEDIA_ROOT       = BASE_DIR / 'media'
