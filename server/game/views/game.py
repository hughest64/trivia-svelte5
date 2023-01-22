from django.db.models import Prefetch
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect

from rest_framework.response import Response
from rest_framework.views import APIView

from user.authentication import JwtAuthentication

from game.models import (
    LeaderboardEntry,
    TriviaEvent,
    QuestionResponse,
    LEADERBOARD_TYPE_HOST,
    LEADERBOARD_TYPE_PUBLIC,
)
from game.models.utils import queryset_to_json
from game.views.validation.data_cleaner import (
    DataCleaner,
    DataValidationError,
    TeamRequired,
    check_player_limit,
    get_event_or_404,
)
from user.models import User

from game.utils.socket_classes import SendTeamMessage
from user.models import User


class EventView(APIView):
    authentication_classes = [JwtAuthentication]

    def get(self, request, joincode):
        """fetch a specific event from the joincode parsed from the url"""
        user: User = request.user
        if not user.active_team:
            raise TeamRequired

        event = get_event_or_404(joincode=joincode)
        check_player_limit(event, user)

        question_responses = QuestionResponse.objects.filter(
            event__joincode=joincode, team=user.active_team
        )

        return Response(
            {
                **event.to_json(),
                "user_data": user.to_json(),
                "response_data": queryset_to_json(question_responses),
            }
        )

    @method_decorator(csrf_protect)
    def post(self, request):
        try:
            data = DataCleaner(request.data)
            joncode = data.as_int("joincode")
        except DataValidationError as e:
            return Response(e.response)

        user = request.user
        # TODO: should we add the prefetch stuff to get_event_or_404?
        # event = get_event_or_404(joincode=joncode)
        event = TriviaEvent.objects.prefetch_related(
            Prefetch(
                "leaderboards",
                to_attr="leaderboard_list",
            )
        ).get(joncode=joncode)

        check_player_limit(event, user)
        event.event_teams.add(user.active_team)
        event.players.add(user)

        # TODO: not sure I trust the indexing here
        LeaderboardEntry.objects.get_or_create(
            leaderboard=event.leaderboard_list[LEADERBOARD_TYPE_HOST],
            team=user.active_team,
        )
        public_lbe, created = LeaderboardEntry.objects.get_or_create(
            leaderboard=event.leaderboard_list[LEADERBOARD_TYPE_PUBLIC],
            team=user.active_team,
        )

        if created:
            # send a socket message
            pass

        # user and event data
        return Response()


class EventJoinView(APIView):
    authentication_classes = [JwtAuthentication]

    def get(self, request):
        user_data = request.user.to_json()

        return Response({"user_data": user_data})


class ResponseView(APIView):
    authentication_classes = [JwtAuthentication]

    @method_decorator(csrf_protect)
    def post(self, request, joincode):
        try:
            data = DataCleaner(request.data)
            team_id = data.as_int("team_id")
            question_id = data.as_int("question_id")
            response_text = data.as_string("response_text")
        except DataValidationError as e:
            return Response(e.response)

        if not request.user.active_team:
            raise TeamRequired

        event = get_event_or_404(joincode=joincode)

        # TODO: this doesn't prevent a reponse from being created if a round is already locked!
        question_response, _ = QuestionResponse.objects.get_or_create(
            team_id=team_id,
            event=event,
            game_question_id=question_id,
            defaults={"recorded_answer": response_text},
        )

        # TODO: this should probably throw an error if the response is locked, or better yetpass the
        # round number in the post data and throw an error if the corresponding round is locked
        if not question_response.locked:
            question_response.recorded_answer = response_text
            question_response.grade()
            question_response.save()

        SendTeamMessage(
            joincode,
            team_id,
            {
                "msg_type": "team_response_update",
                "message": question_response.to_json(),
            },
        )

        return Response({"success": True})
