from django.contrib.auth.models import AbstractUser, UserManager
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils.crypto import get_random_string


class CustomUserManager(UserManager):
    def create_guest_user(self):
        last_id = self.last().id

        return super().create_user(
            username=f"_guest_{last_id + 1}", password=get_random_string(12)
        )

    def get_or_create_user(self, username, password, email=None, **extra_fields):
        created = False
        try:
            user = self.get(username=username)
        except ObjectDoesNotExist:
            created = True
            user = self.create_user(
                username=username, password=password, email=email, **extra_fields
            )

        return (user, created)


class User(AbstractUser):
    screen_name = models.CharField(max_length=100, blank=True)
    active_team = models.ForeignKey(
        "game.Team", blank=True, null=True, on_delete=models.SET_NULL
    )
    auto_reveal_questions = models.BooleanField(default=False)

    home_location = models.ForeignKey(
        "game.Location", blank=True, null=True, on_delete=models.SET_NULL
    )

    objects = CustomUserManager()

    def teams_json(self):
        return [team.to_json() for team in self.teams.all()]

    def to_json(self):
        active_team_id = self.active_team.id if self.active_team else None
        return {
            "id": self.pk,
            "username": self.username,
            "screen_name": self.screen_name if self.screen_name is not None else "",
            "email": self.email,
            "is_staff": self.is_staff,
            "active_team_id": active_team_id,
            "auto_reveal_questions": self.auto_reveal_questions,
            "teams": self.teams_json(),
            "home_location": self.home_location.to_json()
            if self.home_location
            else None,
        }

    # def save(self, *args, **kwargs):
    #     self.full_clean()
    #     super().save(*args, **kwargs)
