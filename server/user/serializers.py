from rest_framework import serializers
from rest_framework import validators
from django.contrib.auth import get_user_model

from game.serializers import TeamSerializer

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    username = serializers.CharField(
        max_length=255,
        validators=[
            validators.UniqueValidator(
                queryset=User.objects.all(),
                message="This Username is Taken. Please Select a Different One",
            )
        ],
    )

    teams = TeamSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "password",
            "is_staff",
            "auto_reveal_questions",
            "active_team_id",
            "teams",
        ]

        # never return the password
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        instance = self.Meta.model(**validated_data)

        # hash the password in the db
        if password is not None:
            instance.set_password(password)

        instance.save()

        return instance
