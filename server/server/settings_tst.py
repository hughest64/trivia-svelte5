from .settings import *

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "triviamafia_tst",
        "USER": env.str("POSTGRES_USER", default="triviamafia"),
        "PASSWORD": env.str("POSTGRES_PASSWORD", default="supergoodpassword"),
        "HOST": "127.0.0.1",
        "PORT": "5432",
    }
}

# allow resetting of event data via the reset-event-data endpoint
ALLOW_EVENT_RESET = True
