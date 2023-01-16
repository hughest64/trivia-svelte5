from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from game.views.validation.data_cleaner import (
    DataCleaner,
    DataValidationError,
    get_event_or_404,
)
from user.authentication import JwtAuthentication

from game.models import (
    EventQuestionState,
    EventRoundState,
    Leaderboard,
    TriviaEvent,
    QuestionResponse,
    LEADERBOARD_TYPE_HOST,
    LEADERBOARD_TYPE_PUBLIC,
)
from game.processors import LeaderboardProcessor


class LeaderboardView(APIView):
    authentication_classes = [JwtAuthentication]

    def get(self, request, joincode):
        event = get_event_or_404(joincode)
        # TODO: we'll need to be able to determine which type to get if the same
        # view will be used by host and player (host may need to fetch both types)
        # try:
        leaderboard = Leaderboard.objects.get(event=event, type=LEADERBOARD_TYPE_PUBLIC)
        # except:
        leaderboard_data = LeaderboardProcessor(leaderboard).to_json()

        return Response(
            {"user_data": request.user.to_json(), "leaderbaord_data": leaderboard_data}
        )


# NOTE: for testing only!
class ClearEventDataView(APIView):
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
            # keep responses for event 9998 for load testing
            QuestionResponse.objects.exclude(event__joincode=9998).delete()
        except Exception as e:
            return Response({"detail": ""}, status=HTTP_400_BAD_REQUEST)

        return Response({"success": True})
