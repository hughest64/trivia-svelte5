from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    active_team = models.ForeignKey(
        "game.Team", blank=True, null=True, on_delete=models.SET_NULL
    )
    auto_reveal_questions = models.BooleanField(default=False)

    home_location = models.ForeignKey(
        "game.Location", blank=True, null=True, on_delete=models.SET_NULL
    )

    def teams_json(self):
        return [team.to_json() for team in self.teams.all()]

    def to_json(self):
        active_team_id = self.active_team.id if self.active_team else None
        return {
            "id": self.pk,
            "username": self.username,
            "email": self.email,
            "is_staff": self.is_staff,
            "active_team_id": active_team_id,
            "auto_reveal_questions": self.auto_reveal_questions,
            "teams": self.teams_json(),
            "home_location": self.home_location.to_json()
            if self.home_location
            else None,
        }

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
