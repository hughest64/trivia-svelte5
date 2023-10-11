from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class TriviaUserAdmin(UserAdmin):
    fieldsets = (
        (
            "User Info",
            {
                "fields": (
                    "screen_name",
                    "active_team",
                    "is_guest",
                    "auto_reveal_questions",
                    "home_location",
                )
            },
        ),
    ) + UserAdmin.fieldsets


admin.site.register(User, TriviaUserAdmin)
