from rest_framework.exceptions import APIException, ValidationError, NotFound
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST

from game.models import (
    EventRoundState,
    EventQuestionState,
    GameQuestion,
    LeaderboardEntry,
    LEADERBOARD_TYPE_HOST,
    QUESTION_TYPE_TIE_BREAKER,
)


class TestFailed(APIException):
    status_code = HTTP_400_BAD_REQUEST
    default_detail = "The test failed"
    default_code = "test_failed"


class ValidateData:
    @classmethod
    def get(cls, key):
        method_dct = {
            "validate_megaround": cls.validate_megaround,
            "megaround_lock": cls.megaround_lock,
            "player_limit": cls.player_limit,
            "validate_reveal_all": cls.validate_reveal_all,
            "validate_pts_adj_reason": cls.validate_pts_adj_reason,
            "get_tb_answer": cls.get_tb_answer,
        }

        return method_dct[key]

    @classmethod
    def validate_megaround(cls, request, event):
        round = int(request.data.get("round", 0))
        team = request.data.get("team")

        try:
            lbe = LeaderboardEntry.objects.get(
                event=event,
                team__name=team,
                leaderboard_type=LEADERBOARD_TYPE_HOST,
            )
        except LeaderboardEntry.DoesNotExist:
            raise TestFailed(f"no leaderboard entry for team {team}")

        else:
            if lbe.selected_megaround != round:
                raise TestFailed(
                    f"selected megaround {lbe.selected_megaround} does not equal {round}"
                )

        return Response({"success": True})

    @classmethod
    def megaround_lock(cls, request, event):
        rd_count = event.game.game_rounds.exclude(round_number=0).count()
        for i in range(1, rd_count + 1):
            EventRoundState.objects.update_or_create(
                event=event, round_number=i, defaults={"locked": True}
            )
        return Response({"sucess": True})

    @classmethod
    def player_limit(cls, request, event):
        limit = request.data.get("limit")

        if limit != event.player_limit:
            raise TestFailed(f"limit {limit} != event limit {event.player_limit}")

        return Response({"sucess": True})

    @classmethod
    def validate_reveal_all(cls, request, event):
        rd_number = request.data.get("round_number")
        total_questions = GameQuestion.objects.filter(
            game=event.game, round_number=rd_number
        ).count()

        locked_questions = EventQuestionState.objects.filter(
            event=event, round_number=rd_number, question_displayed=True
        ).count()

        print("round", rd_number, "total", total_questions, "locked", locked_questions)

        if total_questions != locked_questions:
            raise TestFailed(
                f"only {locked_questions} of {total_questions} for {rd_number} are locked"
            )

        return Response({"sucess": True})

    @classmethod
    def validate_pts_adj_reason(cls, request, event):
        reason_id = request.data.get("reason_id")
        team_name = request.data.get("team_name")
        try:
            lbe = LeaderboardEntry.objects.get(
                event=event,
                team__name=team_name,
                leaderboard_type=LEADERBOARD_TYPE_HOST,
            )
        except LeaderboardEntry.DoesNotExist:
            raise ValidationError(f"A leaderboard entry for {team_name} was not found")

        validation_id = lbe.points_adjustment_reason
        if validation_id != int(reason_id):
            raise ValidationError(f"{reason_id} != f{validation_id}")

        return Response({"sucess": True})

    @classmethod
    def get_tb_answer(cls, request, event):
        tb_index = request.data.get("index")
        try:
            questions = event.game.game_questions.filter(
                question__question_type=QUESTION_TYPE_TIE_BREAKER
            )
            answer = questions[tb_index].question.display_answer.text
        except Exception as e:
            print(e)
            raise NotFound("could not locat the requested trivia question")

        return Response({"answer": answer})
