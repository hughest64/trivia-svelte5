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


class LeaderboardView(APIView):
    authentication_classes = [JwtAuthentication]

    def get(self, request, joincode):
        event = get_event_or_404(joincode)
        try:
            leaderboard = Leaderboard.objects.get(
                event=event, leaderboard_type=LEADERBOARD_TYPE_PUBLIC
            )
        except Leaderboard.DoesNotExist:
            return Response(
                {
                    "detail": f"No public leaderboard for event with joincode {joincode} was found"
                },
                status=404,
            )

        return Response(
            {
                "user_data": request.user.to_json(),
                "leaderboard_data": leaderboard.to_json(),
            }
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
