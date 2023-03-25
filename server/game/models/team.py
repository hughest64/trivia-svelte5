import random

from django.conf import settings
from django.db import models


class Team(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    # TODO: unique?
    name = models.CharField(max_length=200)
    # TODO: db_index=True
    password = models.CharField(max_length=200, unique=True)
    members = models.ManyToManyField("user.User", related_name="teams")

    def to_json(self):
        return {
            "id": self.pk,
            "name": self.name,
            "password": self.password,
            "members": [member.username for member in self.members.all()],
        }

    def __str__(self):
        return self.name


def generate_team_password(attempts=1, max_attempts=30, sep="-"):
    """
    Generate a team password from the list of available words.
    Raises StopIteration if a unique password is not generated in max_attempts.
    """
    password = sep.join(random.sample(settings.WORD_LISZT, 3))

    if password in [i.password for i in Team.objects.all()]:
        if attempts >= max_attempts:
            raise StopIteration("Cannot generate a team password, too many attempts")

        return generate_team_password(
            attempts=attempts + 1, max_attempts=max_attempts, sep=sep
        )

    return password
