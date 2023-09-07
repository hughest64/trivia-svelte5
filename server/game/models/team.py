import random

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from game.views.validation.exceptions import TeamPasswordError

MAX_CREATE_JOINCODE_ATTEMPTS = 30

TEAM_CHAT_STORAGE_LIMIT = 200


class Team(models.Model):
    def __init__(self, *args, create_password=False, **kwargs):
        # shall we auto-generate a team joincode?
        self.create_password = create_password
        super().__init__(*args, **kwargs)

    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100)
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


class ChatMessage(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(
        "user.User", related_name="chats", on_delete=models.CASCADE
    )
    team = models.ForeignKey(Team, related_name="chats", on_delete=models.CASCADE)
    event = models.ForeignKey(
        "TriviaEvent", blank=True, null=True, on_delete=models.CASCADE
    )
    chat_message = models.TextField(max_length=255)

    def local_created_at(self, as_string=True):
        """return the created_at field in local time"""
        local_time = timezone.localtime(self.created_at)

        if as_string:
            return f"{local_time:%I:%M:%S %P}"
        return local_time

    def __str__(self):
        return f"{self.user} - {self.chat_message[:10]}"

    def to_json(self):
        return {
            "id": self.id,
            "user": self.user.screen_name or self.user.username,
            "team": self.team.name,
            "chat_message": self.chat_message,
            "time": self.local_created_at(),
        }

    def save(self, *args, **kwargs):
        self.full_clean()

        if not self.pk:
            # limit chat storage per team
            num_existing_chats = ChatMessage.objects.filter(team=self.team).count()
            if num_existing_chats >= TEAM_CHAT_STORAGE_LIMIT:
                num_existing_chats[:1].delete()

            # add the time
            self.time = timezone.localtime()

        super().save(*args, **kwargs)
