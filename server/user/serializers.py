from rest_framework import serializers
from rest_framework import validators
from django.contrib.auth import get_user_model

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

    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "is_staff", "active_team_id"]

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
