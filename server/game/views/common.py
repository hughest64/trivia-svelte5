from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from game.views.validation.data_cleaner import get_event_or_404, DataCleaner
from user.authentication import JwtAuthentication

from game.utils.socket_classes import SendEventMessage

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
        event = get_event_or_404(joincode=joincode)
        data = DataCleaner(request.data)
        chat_message = data.as_string("chat_message")
        is_host_message = data.as_bool("host_message")
        user = request.user
        user_team = user.active_team if not is_host_message else None

        msg = ChatMessage.objects.create(
            user=user,
            team=user_team,
            event=event,
            chat_message=chat_message,
            is_host_message=is_host_message,
        )
        SendEventMessage(
            joincode=joincode,
            message={"msg_type": "chat_message", "message": msg.to_json()},
        )

        return Response({"success": True})
