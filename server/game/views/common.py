from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from game.models import (
    EventQuestionState,
    EventRoundState,
    TriviaEvent,
    QuestionResponse,
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
