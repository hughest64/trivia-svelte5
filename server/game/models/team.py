from django.db import models


class Team(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=200)
    password = models.CharField(max_length=200, unique=True)
    members = models.ManyToManyField( "user.User", related_name="teams" )

    def to_json(self):
        return {
            "id": self.pk,
            "name": self.name,
            "password": self.password,
            "members": [member.username for member in self.members.all()]
        }

    def __str__(self):
        return self.name
