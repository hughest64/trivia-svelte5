from rest_framework import serializers
from .models import Team


class TeamSerializer(serializers.ModelSerializer):
    members = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="username"
    )

    class Meta:
        model = Team
        exclude = ["created_at"]
