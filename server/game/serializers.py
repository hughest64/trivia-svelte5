from rest_framework import serializers
from .models import Team


class TeamSerializer(serializers.ModelSerializer):
    members = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="username"
    )

    class Meta:
        model = Team
        fields = "__all__"


# TODO, ModelSerialzer
class LocationSerializer(serializers.Serializer):
    location_id = serializers.IntegerField()
    location_name = serializers.CharField(max_length=200)


class GameSerializer(serializers.Serializer):
    game_id = serializers.IntegerField()
    game_title = serializers.CharField(max_length=200)
