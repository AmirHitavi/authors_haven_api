from .base import *  # noqa

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default="django-insecure-yp8qy+04_^8!vbhv7i9k6db!7inw!x%udvnic2liueoo03_5zv",
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DJANGO_DEBUG", default=True)

CSRF_TRUSTED_ORIGINS = ["http://localhost:8080"]

EMAIL_BACKEND = "djcelery_email.backends.CeleryEmailBackend"
EMAIL_HOST = env("EMAIL_HOST", default="mailhog")
EMAIL_PORT = env("EMAIL_PORT")
DEFAULT_FROM_EMAIL = "support@authorshaven.com"
DOMAIN = env("DOMAIN")
