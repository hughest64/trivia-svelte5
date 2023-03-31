from django.conf import settings
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


class ClearEventDataView(APIView):
    """Endpoint used for resetting event data during tests"""

    def post(self, request):
        # TODO: this kinda get's buried in the test run (we only see the 400 response)
        # if not settings.ALLOW_EVENT_RESET:
        #     return Response(
        #         {"detail": "that is not allowed"}, status=HTTP_400_BAD_REQUEST
        #     )

        secret = request.data.get("secret")
        joincodes = request.data.get("joincodes", [])
        if isinstance(joincodes, (str, int)):
            joincodes = [joincodes]

        # TODO: probably better to keep the secret in a .env file and read it into settings
        # if secret != "todd is great":
        #     return Response(
        #         {"detail": "ah ah ah, you didn't say the magic word"},
        #         status=HTTP_400_BAD_REQUEST,
        #     )

        try:
            msg = management.call_command("reset", *joincodes)
            print(msg)
        except Exception as e:
            print(e)
            return Response({"detail": ""}, status=HTTP_400_BAD_REQUEST)

        return Response({"success": True})
