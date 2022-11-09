from django.db import models


class Team(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=200)
    password = models.CharField(max_length=200, unique=True)
    # TODO: change model ref to get_user_model()?
    members = models.ManyToManyField( "user.User", related_name="teams" )

    def __str__(self):
        return self.name
