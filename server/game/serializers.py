from rest_framework  import serializers


# TODO, ModelSerialzer
class TeamSerializer(serializers.Serializer):
    team_id = serializers.IntegerField()
    team_name = serializers.CharField(max_length=200)
    join_code = serializers.CharField(max_length=200)