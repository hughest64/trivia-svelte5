from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from game.views.validation.data_cleaner import get_event_or_404, DataCleaner
from user.authentication import JwtAuthentication

from game.utils.socket_classes import SendTeamMessage

from game.models import (
    LeaderboardEntry,
    ChatMessage,
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


class ChatCreateView(APIView):
    authentication_classes = [JwtAuthentication]

    def post(self, request, chat_type, joincode):
        # TODO: temp until host messaging is in place
        if chat_type != "game":
            return Response(
                {"detail": "host messaging is not implemented"},
                status=HTTP_400_BAD_REQUEST,
            )
        event = get_event_or_404(joincode=joincode)
        data = DataCleaner(request.data)
        chat_message = data.as_string("chat_message")
        user = request.user
        user_team = user.active_team

        msg = ChatMessage.objects.create(
            user=user, team=user_team, event=event, chat_message=chat_message
        )
        SendTeamMessage(
            team_id=user_team.id,
            joincode=joincode,
            message={"msg_type": "chat_message", "message": msg.to_json()},
        )

        return Response({"success": True})
