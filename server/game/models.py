from django.db import models

# TODO: convert models to actual Djanog models!

class Team:
    def __init__(self, team_id, team_name, join_code, team_members=list):
        self.team_id = team_id
        self.team_name = team_name
        self.join_code = join_code
        self.team_members = team_members
