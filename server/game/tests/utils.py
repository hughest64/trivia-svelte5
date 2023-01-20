import json
import random
from typing import List

from django.db.models import QuerySet
from django.db import transaction

from game.models import *


# TODO: this is only used by a management cmd, probably move out of testings
class GameCreator:
    """This is likely to change a lot, but a good start to creating data from the a.t. import"""

    def __init__(self, responses, game=None, event=None, round_count=8):
        # TODO: for airtable imports, this would be airtable data
        self.responses = responses
        self.game = game
        self.event = event
        self.round_count = round_count
        self.default_game_title = "Responses for Scoring"
        self.default_event_data = {
            "location": Location.objects.first(),
            "joincode": 9998,
            "game": self.game,
        }
        self.game_questions = {}

    def get_question_key(self, resp):
        return f"{resp['round_number']}.{resp['question_number']}"

    def create_game(self, title=None):
        "create a game if one wasn't provided and set as an attr"
        game_title = title or self.default_game_title
        game, _ = Game.objects.get_or_create(title=game_title, block_code="A")
        [
            GameRound.objects.get_or_create(
                title=f"Response Test Rd - {i}", round_number=i, game=game
            )
            for i in range(1, self.round_count + 1)
        ]

        self.game = game

    def create_event(self, data=None):
        "create a event if one wasn't provided and set as an attr"
        if not self.game:
            raise ValueError(
                "A Game instance is required to create question data. \
                 Please pass one to the init function or call the create_game method."
            )
        event_data = data or self.default_event_data
        event_data.update({"game": self.game})
        event, _ = TriviaEvent.objects.get_or_create(**event_data)
        self.event = event

    def create_question_data(self):
        """create questions, answers, and game questions"""
        if not self.game:
            raise ValueError(
                "A Game instance is required to create question data. \
                 Please pass one to the init function or call the create_game method."
            )
        with transaction.atomic():
            for r in self.responses:
                key = self.get_question_key(r)
                if key not in self.game_questions:
                    answer, _ = QuestionAnswer.objects.get_or_create(
                        text=r["display_answer"]
                    )
                    question, _ = Question.objects.get_or_create(
                        display_answer=answer, question_text=r["text"]
                    )
                    game_question, _ = GameQuestion.objects.get_or_create(
                        question=question,
                        game=self.game,
                        question_number=r["question_number"],
                        round_number=r["round_number"],
                    )
                    self.game_questions[key] = game_question

    def create_responses(self):
        """create responses from the supplided data for an event"""
        if not self.event:
            raise ValueError(
                "A TriviaEvent instance is required to create QuestionResponses. \
                 Please pass one to the init function or call the create_event method."
            )
        with transaction.atomic():
            for r in self.responses:
                key = self.get_question_key(r)
                question = self.game_questions.get(key)
                if not question:
                    # continue
                    raise ValueError(
                        f"No GameQuestion was found for {key}. Check your data!"
                    )
                team, _ = Team.objects.get_or_create(
                    name=f"test-{r['team_id']}", defaults={"password": r["team_id"]}
                )
                resp = QuestionResponse(
                    game_question=question,
                    recorded_answer=r.get("recorded_answer", "_") or "_",
                    team=team,
                    event=self.event,
                )
                resp.grade()
                resp.save()


# TODO: we don't need this anymore
class QuestionResponseGenerator:
    """for use in testing only!"""

    def __init__(
        self,
        event: TriviaEvent,
        round_numbers: List[int],
        question_numbers: List[int] = [],
        response_options: List[str] = [],
        team_count=1,
    ) -> None:
        self.event = event
        self.round_numbers = round_numbers
        self.question_numbers = question_numbers
        self.game_questions: QuerySet[GameQuestion]
        self.team_count = team_count
        self.teams: List[Team] = []
        self.response_options = response_options
        # set by self.parse_responses, and superseeds self.response_options
        self.response_list = []

    def parse_response_json(self, fp):
        """load a list of responses from the old app that adhere to the response.serialize() call"""
        with open(fp, "r") as f:
            responses = json.load(f)

        grouped_responses = {}
        for response in responses:
            team_key = response["team_id"]
            question_key = f"{response['round_number']}.{response['question_number']}"

            grouped_responses.setdefault(team_key, {})
            grouped_responses[team_key][question_key] = {
                "display_answer": response.get("display_answer", ""),
                "recorded_answer": response.get("recorded_answer", ""),
            }
        self.team_count = len(grouped_responses.values())
        self.response_list = list(grouped_responses.values())

    def set_game_questions(self) -> None:
        self.game_questions = GameQuestion.objects.filter(
            game=self.event.game, round_number__in=self.round_numbers
        )

    def create_teams(self) -> None:
        for i in range(1, self.team_count + 1):
            self.teams.append(
                Team.objects.create(name=f"team-{i}", password="abc-123" + str(i))
            )

    def create_response(
        self, question: GameQuestion, text: str, team: Team
    ) -> QuestionResponse:
        resp = QuestionResponse(
            game_question=question, recorded_answer=text, team=team, event=self.event
        )
        resp.grade()
        resp.save()
        return resp

    def generate(self):
        self.set_game_questions()
        self.create_teams()
        for i, team in enumerate(self.teams):
            responses = {}
            if self.response_list:
                responses = self.response_list[i]
            for question in self.game_questions:
                if (
                    self.question_numbers
                    and question.question_number not in self.question_numbers
                ):
                    continue
                if not responses:
                    selections = (
                        self.response_options
                        # makes sure there is a wrong answer
                        or [a.text for a in question.question.accepted_answers.all()]
                        + ["123$0*42"]
                    )
                    response_text = selections[random.randint(0, len(selections) - 1)]
                else:
                    response_data = responses.get(question.key, {})
                    answer, _ = QuestionAnswer.objects.get_or_create(
                        text=response_data.get("display_answer", "")
                    )
                    question.question.accepted_answers.add(answer)
                    response_text = response_data.get("recorded_answer", "_") or "_"

                self.create_response(question, response_text, team)

    def clean_up(self):
        QuestionResponse.objects.all().delete()
        Team.objects.all().delete()
