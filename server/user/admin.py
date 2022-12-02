from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class TriviaUserAdmin(UserAdmin):
    fieldsets = (
        ("User Info", {"fields": ('active_team', 'auto_reveal_questions')}),
    ) + UserAdmin.fieldsets


admin.site.register(User, TriviaUserAdmin)
