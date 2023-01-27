from django.db.models import Prefetch
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.core.exceptions import ValidationError

from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView

from user.authentication import JwtAuthentication

from game.models import (
    Leaderboard,
    LeaderboardEntry,
    TriviaEvent,
    QuestionResponse,
    LEADERBOARD_TYPE_HOST,
    LEADERBOARD_TYPE_PUBLIC,
)
from game.models.utils import queryset_to_json
from game.utils.socket_classes import SendEventMessage
from game.views.validation.data_cleaner import (
    DataCleaner,
    check_player_limit,
    get_event_or_404,
)
from user.models import User

from game.views.validation.exceptions import (
    DataValidationError,
    EventJoinRequired,
    TeamRequired,
)
from game.utils.socket_classes import SendTeamMessage
from user.models import User


class EventView(APIView):
    authentication_classes = [JwtAuthentication]

    def get(self, request, joincode):
        """fetch a specific event from the joincode parsed from the url"""
        event = get_event_or_404(joincode=joincode)
        user: User = request.user
        if user.active_team is None:
            raise TeamRequired

        player_joined = check_player_limit(event, user)

        try:
            public_lb = Leaderboard.objects.get(
                event__joincode=joincode, leaderboard_type=LEADERBOARD_TYPE_PUBLIC
            )
        except Leaderboard.DoesNotExist:
            # TODO: should we raise, or just ship an empty dict?
            raise NotFound(f"No leaderboard exists for event {joincode}.")

        question_responses = QuestionResponse.objects.filter(
            event=event, team=user.active_team
        )

        # TODO: chats (last 50 for the players active team on this event)

        return Response(
            {
                **event.to_json(),
                "user_data": user.to_json(),
                "response_data": queryset_to_json(question_responses),
                "leaderboard_data": public_lb.to_json(),
                # if false, the player can view the event but not respond to questions
                # this should probably trigger a pop up so that user is aware that they can't do anything
                "player_joined": player_joined,
            }
        )


class EventJoinView(APIView):
    authentication_classes = [JwtAuthentication]

    def get(self, request):
        return Response({"user_data": request.user.to_json()})

    @method_decorator(csrf_protect)
    def post(self, request):
        data = DataCleaner(request.data)
        joincode = data.as_int("joincode")

        user = request.user
        if user.active_team is None:
            raise TeamRequired

        try:
            event = TriviaEvent.objects.prefetch_related(
                Prefetch("leaderboards", to_attr="leaderboard_list")
            ).get(joincode=joincode)
        except TriviaEvent.DoesNotExist:
            raise NotFound(detail=f"Event with join code {joincode} does not exist")

        check_player_limit(event, user)
        event.event_teams.add(user.active_team)
        event.players.add(user)

        LeaderboardEntry.objects.get_or_create(
            leaderboard=event.leaderboard_list[LEADERBOARD_TYPE_HOST],
            team=user.active_team,
        )
        public_lbe, created = LeaderboardEntry.objects.get_or_create(
            leaderboard=event.leaderboard_list[LEADERBOARD_TYPE_PUBLIC],
            team=user.active_team,
        )

        if created:
            SendEventMessage(
                joincode,
                message={
                    "msg_type": "leaderboard_join",
                    "message": public_lbe.to_json(),
                },
            )

        return Response({"success": True})


class ResponseView(APIView):
    authentication_classes = [JwtAuthentication]

    @method_decorator(csrf_protect)
    def post(self, request, joincode):
        data = DataCleaner(request.data)
        team_id = data.as_int("team_id")
        question_id = data.as_int("question_id")
        response_text = data.as_string("response_text")

        if not request.user.active_team:
            raise TeamRequired

        event = get_event_or_404(joincode=joincode)

        if request.user not in event.players:
            raise EventJoinRequired

        # this is a bit verbose, but it allows for updating or creating a response as well as score it with one db write
        question_lookup = dict(
            team_id=team_id, event=event, game_question_id=question_id
        )
        try:
            question_response = QuestionResponse.objects.get(**question_lookup)
        except QuestionResponse.DoesNotExist:
            question_response = QuestionResponse(**question_lookup)

        if question_response.locked:
            raise DataValidationError("This response is locked and cannot be updated")

        question_response.recorded_answer = response_text
        question_response.grade()
        try:
            question_response.save()
        # mostly to ensure the game_question_id is valid
        except ValidationError as e:
            raise DataValidationError(str(e))

        SendTeamMessage(
            joincode,
            team_id,
            {
                "msg_type": "team_response_update",
                "message": question_response.to_json(),
            },
        )

        return Response({"success": True})
