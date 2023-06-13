from rest_framework.response import Response
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
