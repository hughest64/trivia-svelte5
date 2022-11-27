from asgiref.sync import async_to_sync

from channels.layers import get_channel_layer

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect

from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND
from rest_framework.views import APIView

from user.authentication import JwtAuthentication

from game.models import Team, Response as QuestionResponse, TriviaEvent, queryset_to_json

channel_layer = get_channel_layer()


class EventView(APIView):
    authentication_classes = [JwtAuthentication]

    def get(self, request, joincode):
        """fetch a specific event from the joincode parsed from the url"""
        user_data = request.user.to_json()

        try:
            event = TriviaEvent.objects.get(join_code=joincode)
        except TriviaEvent.DoesNotExist:
            return Response(
                {"detail": "an event with that join code does not exist"},
                status=HTTP_404_NOT_FOUND,
            )

        # TODO: get responses for this event via the user's active team
        # if they do not have an active team respond with a 400 and a message
        # kit will need to handle the response accordingly
        question_responses = QuestionResponse.objects.filter(
            event__join_code=joincode, team_id=request.user.active_team_id
        )

        return Response(
            {
                **event.to_json(),
                "user_data": user_data,
                "response_data": queryset_to_json(question_responses),
            }
        )


class EventJoinView(APIView):
    authentication_classes = [JwtAuthentication]

    def get(self, request):
        """return user data to /game/join"""
        user_data = request.user.to_json()

        return Response({"user_data": user_data})


class TeamView(APIView):
    authentication_classes = [JwtAuthentication]

    def get(self, request):
        user_data = request.user.to_json()

        return Response({"user_data": user_data})

    @method_decorator(csrf_protect)
    def post(self, request):
        print(request.data)
        team_id = request.data.get("team_id")
        status = HTTP_200_OK
        if team_id:
            user = request.user
            requested_team = Team.objects.filter(id=team_id)
            if requested_team.exists():
                user.active_team_id = requested_team.first().id
                user.save()

            else:
                status = HTTP_404_NOT_FOUND

        return Response({"active_team_id": team_id}, status=status)


class ResponseView(APIView):
    authentication_classes = [JwtAuthentication]

    def post(self, request, joincode):
        team_id = request.data.get("team_id")
        question_id = request.data.get("question_id")
        response_text = request.data.get("response_text")

        # TODO: permission class for this?
        # if request.user.active_team_id != request.data.get("team_id"):
        #     return Response(code=400, data={ "detail": "you are not on the right team"})

        try:
            question_response = QuestionResponse.objects.get(
                team_id=team_id,
                event__join_code=joincode,
                game_question_id=question_id,
            )
            question_response.recorded_answer = response_text
            question_response.save()

        except QuestionResponse.DoesNotExist:
            # TODO: can we look this up more efficiently?
            event = TriviaEvent.objects.filter(join_code=joincode).first()
            question_response = QuestionResponse.objects.create(
                team_id=team_id,
                event=event,
                game_question_id=question_id,
                recorded_answer=response_text 
            )

        async_to_sync(channel_layer.group_send)(
            f"team_{team_id}_event_{joincode}",
            {
                "type": "team_update",
                "msg_type": "team_response_update",
                "store": "responseData",
                "message": question_response.to_json(),
            },
        )

        return Response({"success": True})
