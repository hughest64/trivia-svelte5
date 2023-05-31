from datetime import timedelta
from typing import List

from django.db.models import QuerySet, Q
from django.utils import timezone

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect

from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from game.processors import TriviaEventCreator
from game.views.validation.data_cleaner import (
    DataCleaner,
    DataValidationError,
    get_event_or_404,
    get_game_or_404,
    get_location_or_404,
)
from user.authentication import OpsAuthentication

from game.models import (
    Game,
    GameQuestion,
    Location,
    EventRoundState,
    EventQuestionState,
    TriviaEvent,
    QuestionResponse,
    Leaderboard,
    LeaderboardEntry,
    LEADERBOARD_TYPE_PUBLIC,
    LEADERBOARD_TYPE_HOST,
)
from game.models.utils import queryset_to_json
from game.processors import LeaderboardProcessor
from game.utils.socket_classes import SendEventMessage, SendHostMessage

# TODO:
# - maybe convert to regular view functions as there will be a lot of stuffz here
# - extrapolate common processing and share w/ the actual view func


class HostControlsView(APIView):
    authentication_classes = [OpsAuthentication]

    def post(self, request);
        data = DataCleaner(request.data)
        round_number = data.as_int("round_number")
        locked = data.as_bool("locked")
        joincode = data.as_int("joincode")

        event = get_event_or_404(joincode)

        round_state, _ = EventRoundState.objects.update_or_create(
            event=event,
            round_number=round_number,
            defaults={"locked": locked},
        )
        # TODO: bind these so we can send the updated values back in the socket
        # lock or unlock responses for the round
        resps = QuestionResponse.objects.filter(
            event=event, game_question__round_number=round_number
        )
        resps.update(locked=locked)

        resp_summary = None
        if locked:
            resp_summary = QuestionResponse.summarize(event=event)
            # update the host leaderboard
            lb_processor = LeaderboardProcessor(event)
            leaderboard_data = lb_processor.update_host_leaderboard(
                through_round=event.max_locked_round() or round_state.round_number
            )

            # TODO: perhaps we don't need to send this as a separate host message
            # maybe we just ignore the piece of data if the broswer is on a /game route
            # send host message
            SendHostMessage(
                joincode,
                {
                    "msg_type": "leaderboard_update",
                    "message": leaderboard_data,
                },
            )

        SendEventMessage(
            joincode,
            {
                "msg_type": "round_update",
                "message": {
                    "round_state": round_state.to_json(),
                    "responses": queryset_to_json(resps),
                    "response_summary": resp_summary,
                },
            },
        )

        return Response({"success": True})
