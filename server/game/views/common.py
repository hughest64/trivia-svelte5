from django.core import management

from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from game.views.validation.data_cleaner import get_event_or_404
from user.authentication import JwtAuthentication

from game.models import (
    LeaderboardEntry,
    LEADERBOARD_TYPE_PUBLIC,
    queryset_to_json,
)


class LeaderboardView(APIView):
    authentication_classes = [JwtAuthentication]

    def get(self, request, joincode):
        event = get_event_or_404(joincode)

        public_lb_entries = LeaderboardEntry.objects.filter(
            event=event, leaderboard_type=LEADERBOARD_TYPE_PUBLIC
        )

        return Response(
            {
                "user_data": request.user.to_json(),
                "leaderboard_data": queryset_to_json(public_lb_entries),
            }
        )


# NOTE: for testing only!
# TODO: raise if not settings.DEBUG, and use a better secret code (possibly a shared env variable?)
class ClearEventDataView(APIView):
    def post(self, request):
        secret = request.data.get("secret")
        joincode = request.data.get("joincode")
        if secret != "todd is great":
            return Response(
                {"detail": "ah ah ah, you didn't say the magic word"},
                status=HTTP_400_BAD_REQUEST,
            )

        try:
            msg = management.call_command("reset", joincode=joincode)
            print(msg)
        except Exception as e:
            return Response({"detail": ""}, status=HTTP_400_BAD_REQUEST)

        return Response({"success": True})
