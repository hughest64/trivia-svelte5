from django.db import models

from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    active_team_id = models.IntegerField(blank=True, null=True)
    # TODO: many to many for teams