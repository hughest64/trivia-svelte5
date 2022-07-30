from django.db import models

# TODO: convert models to actual Django models!


class Team(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=200)
    password = models.CharField(max_length=200, unique=True)
    # TODO: change model ref to get_user_model()?
    members = models.ManyToManyField( "user.User", related_name="teams" )

    def __str__(self):
        return self.name


class Game:
    def __init__(self, game_id, game_title):
        self.game_id = game_id
        self.game_title = game_title


class Location:
    def __init__(self, location_id, location_name):
        self.location_id = location_id
        self.location_name = location_name
