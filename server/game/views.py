from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect

from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from user.authentication import JwtAuthentication
from user.serializers import UserSerializer

from game.models import (
    EventQuestionState,
    EventRoundState,
    Location,
    Team,
    TriviaEvent,
    Game,
    Response as QuestionResponse,
    queryset_to_json,
)

# TODO: remove once creating event is implemented
DEMO_EVENT_JOIN_CODE = 1234


class TeamView(APIView):
    authentication_classes = [JwtAuthentication]

    def get(self, request):
        serializer = UserSerializer(request.user)

        return Response({"user_data": serializer.data})

    @method_decorator(csrf_protect)
    def post(self, request):
        team_id = request.data.get("team_id")
        status = HTTP_200_OK
        if team_id:
            user = request.user
            requested_team = Team.objects.filter(id=team_id)
            if requested_team.exists():
                user.active_team_id = requested_team.first().id
                user.save()

            else:
                status = HTTP_404_NOT_FOUND

        return Response({"active_team_id": team_id}, status=status)


class EventSetupView(APIView):
    authentication_classes = [JwtAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, request):
        """get this weeks games and a list of locations"""
        user = request.user
        locations = queryset_to_json(Location.objects.filter(active=True))
        # TODO: a filter of some sort to limit avialable games (should there be an active pram on the model?)
        games = queryset_to_json(Game.objects.all())
        user_serializer = UserSerializer(user)

        return Response(
            {
                "location_select_data": locations,
                "game_select_data": games,
                "user_data": user_serializer.data,
            }
        )

    @method_decorator(csrf_protect)
    def post(self, request):
        """create a new event or fetch an existing one with a specified game/location combo"""
        user = request.user
        # TODO: get or create
        event = TriviaEvent.objects.get(join_code=DEMO_EVENT_JOIN_CODE)
        user_serializer = UserSerializer(user)

        # TODO: this could just return the join code since the data won't be loaded from this response
        return Response(
            {
                "event_data": event.to_json()["event_data"],
                "user_data": user_serializer.data,
            }
        )


class EventView(APIView):
    authentication_classes = [JwtAuthentication]

    def get(self, request, joincode):
        """fetch a specific event from the joincode parsed from the url"""
        user_serializer = UserSerializer(request.user)

        try:
            event = TriviaEvent.objects.get(join_code=joincode)
        except TriviaEvent.DoesNotExist:
            return Response(
                {"detail": "an event with that join code does not exist"},
                status=HTTP_404_NOT_FOUND,
            )

        # TODO: get responses for this event via the user's active team
        # if they do not have an active team respond with a 400 and a message
        # kit will need to handle the response accordingly
        question_responses = QuestionResponse.objects.filter(
            event__join_code=joincode, team_id=request.user.active_team_id
        )

        return Response(
            {
                **event.to_json(),
                "user_data": user_serializer.data,
                "response_data": queryset_to_json(question_responses),
            }
        )


class EventJoinView(APIView):
    authentication_classes = [JwtAuthentication]

    def get(self, request):
        """return user data to /game/join"""
        serializer = UserSerializer(request.user)

        return Response({"user_data": serializer.data})


# TODO: do we need this? The data isn't any different from the player view
class EventHostView(APIView):
    authentication_classes = [JwtAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, request, joincode):
        """fetch a specific event from the joincode parsed from the url"""
        user_serializer = UserSerializer(request.user)

        try:
            event = TriviaEvent.objects.get(join_code=joincode or DEMO_EVENT_JOIN_CODE)
        except TriviaEvent.DoesNotExist:
            return Response(
                {"detail": "an event with that join code does not exist"},
                status=HTTP_404_NOT_FOUND,
            )

        return Response({**event.to_json(), "user_data": user_serializer.data})


class ClearEventDataView(APIView):
    # NOTE: for resetting post data only!
    def post(self, request):
        secret = request.data.get("secret")
        if secret != "todd is great":
            return Response(
                {"detail": "ah ah ah, you didn't say the magic word"},
                status=HTTP_400_BAD_REQUEST,
            )

        try:
            TriviaEvent.objects.all().update(
                current_question_number=1, current_round_number=1
            )
            EventQuestionState.objects.all().update(
                question_displayed=False, answer_displayed=False
            )
            EventRoundState.objects.all().update(scored=False, locked=False)
            QuestionResponse.objects.all().delete()
        except Exception as e:
            return Response({"detail": ""}, status=HTTP_400_BAD_REQUEST)

        return Response({"success": True})
