from .settings import *

# test database, TODO: move to postgres
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db_validation.sqlite3",
    }
}
