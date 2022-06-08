from unittest.util import _MAX_LENGTH
from rest_framework  import serializers


# TODO, ModelSerialzer
class TeamSerializer(serializers.Serializer):
    team_id = serializers.IntegerField()
    team_name = serializers.CharField(max_length=200)
    join_code = serializers.CharField(max_length=200)


class LocationSerializer(serializers.Serializer):
    location_id = serializers.IntegerField()
    location_name = serializers.CharField(max_length=200)


class GameSerializer(serializers.Serializer):
    game_id = serializers.IntegerField()
    game_title= serializers.CharField(max_length=200)