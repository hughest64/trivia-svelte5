from django.contrib.auth.models import AbstractUser
from django.db import models
from game.models import Team

class User(AbstractUser):
    active_team_id = models.IntegerField(blank=True, null=True)
    auto_reveal_questions = models.BooleanField(default=False)

    def teams_json(self):
        return [team.to_json() for team in self.teams.all()]

    def to_json(self):
        active_team_id = self.active_team_id if self.active_team_id else None
        return {
            "username": self.username,
            "active_team_id": active_team_id,
            "teams": self.teams_json()
        }

    def clean(self):
        # ensure that whenever an active id is set, the user is added to the team
        if self.active_team_id:
            team_query = Team.objects.filter(id=self.active_team_id)
            if not team_query.exists():
                raise ValueError(f"Team with id {self.active_team_id} does not exist")

            self.teams.add(self.active_team_id)

        return super().clean()