from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    active_team_id = models.IntegerField(blank=True, null=True)
