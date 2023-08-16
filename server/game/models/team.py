import random

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

from game.views.validation.exceptions import TeamPasswordError

MAX_CREATE_JOINCODE_ATTEMPTS = 30


class Team(models.Model):
    def __init__(self, *args, create_password=False, **kwargs):
        # shall we auto-generate a team joincode?
        self.create_password = create_password
        super().__init__(*args, **kwargs)

    created_at = models.DateTimeField(auto_now_add=True)
    # TODO: unique?
    name = models.CharField(max_length=60)
    password = models.CharField(max_length=120, unique=True, db_index=True)
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

    def generate_password(self, attempts, *args, sep="-", **kwargs):
        if attempts > MAX_CREATE_JOINCODE_ATTEMPTS:
            raise TeamPasswordError(
                detail="cannot create a password for this team, too many attempts"
            )
        try:
            self.password = sep.join(random.sample(settings.WORD_LISZT, 3))
            self.full_clean()

        except ValidationError as e:
            if "password" in e.error_dict:
                self.generate_password(attempts + 1, *args, **kwargs)
            raise ValidationError(e)

    def save(self, *args, **kwargs):
        if self.pk is not None and self.create_password:
            raise TeamPasswordError(
                detail="cannot auto generate a password for an existing team"
            )

        if self.create_password:
            self.generate_password(0, *args, **kwargs)
        else:
            self.full_clean()

        super().save(*args, **kwargs)
