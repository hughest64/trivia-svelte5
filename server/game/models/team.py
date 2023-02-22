from django.db import models

from game.utils.code_generator import get_code


class Team(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    # TODO: unique?
    name = models.CharField(max_length=200)
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


def generate_team_password(attempts=1, max_attempts=30):
    """
    Generate a team password from the list of available words.
    Raises StopIteration if a unique password is not generated in max_attempts.
    """
    password = get_code()
    if password in [i.password for i in Team.objects.all()]:
        if attempts >= max_attempts:
            raise StopIteration("Cannot generate a team password, too many attempts")

        return generate_team_password(attempts=attempts + 1, max_attempts=max_attempts)

    return password
