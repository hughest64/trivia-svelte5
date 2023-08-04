from game.models import *
from game.processors import LeaderboardProcessor, TriviaEventCreator, QuestionResponse

from user.models import User


class EventSetup(TriviaEventCreator):
    def __init__(
        self, game: Game, joincode: int = None, auto_create=False, reset=True, **kwargs
    ) -> None:
        self.reset = reset
        self.joincode = joincode
        super().__init__(game, joincode=joincode, auto_create=auto_create, **kwargs)

    def get_or_create_event(self):
        if self.reset:
            TriviaEvent.objects.filter(joincode=self.joincode).delete()
        super().get_or_create_event()


# provide various getters/setters to update the db to simulate game play
class TeamActions:
    def __init__(
        self, event: TriviaEvent, team: Team = None, team_id: int = None
    ) -> None:
        self.event = event
        self.game = event.game
        self.team = team
        self.team_id = team_id
        self.players = []

    def get_or_create_team(self, team_name=None, i=None, players=None):
        if team_name is None:
            team_name = f"run_game_team_{i}"

        if players is None:
            players = [f"run_game_user_{i}"]

        self.team, _ = Team.objects.get_or_create(
            name=team_name, defaults={"password": f"12345_{i}"}
        )
        for player in players:
            user, created = User.objects.get_or_create(
                username=player,
                defaults={"active_team": self.team, "password": 12345},
            )
            if created:
                user.set_password("12345")
                user.save()

            self.players.append(user)

        self.team.members.set(self.players)

    def add_team_to_event(self, i=None):
        LeaderboardEntry.objects.get_or_create(
            event=self.event, team=self.team, leaderboard_type=LEADERBOARD_TYPE_HOST
        )
        LeaderboardEntry.objects.get_or_create(
            event=self.event, team=self.team, leaderboard_type=LEADERBOARD_TYPE_PUBLIC
        )
        self.event.event_teams.add(self.team)
        self.event.players.add(*self.players)

    # TODO: megaround!
    def answer_questions(self, question_data, megaround_data=None):
        """Answer a set of questions for for an event round"""
        questions = self.game.game_questions.all()

        for q in questions:
            # only answer questions provided
            if q.key not in question_data:
                continue

            q_data = question_data[q.key]
            QuestionResponse.objects.update_or_create(
                event=self.event,
                game_question=q,
                team=self.team,
                defaults={
                    "recorded_answer": q_data.get("answer"),
                    "points_awarded": q_data.get("points"),
                },
            )

    # TODO: megaround!
    # also TODO: do we even need this one anymore?
    def answer_questions_from_config(self, rd_num, team_rd):
        rd_questions = self.game.game_questions.filter(round_number=rd_num)
        # loop the config so we only answer desired questions
        # TODO: probably better to pop these into a list and bulk_create
        for q in team_rd:
            game_question = rd_questions.get(question_number=q["question"])
            answer = (
                game_question.question.display_answer
                if q["use_actual"]
                else q["answer"]
            )
            resp = QuestionResponse(
                event=self.event,
                game_question=game_question,
                team=self.team,
                recorded_answer=answer,
            )
            if q["auto_grade"]:
                resp.grade()
            else:
                resp.points_awarded = q["points"]
            resp.save()

    def answer_questions_from_percentage(
        self, percent_correct: int, through_rd: int = None, megaround_data=None
    ):
        """
        Answer all questions in game for a single team using
        percent_correct to determine how to respond and grade
        """
        if megaround_data is None:
            megaround_data = {}

        selected_megaround = megaround_data.get("round", 0)
        megaround_values = megaround_data.get("values", {})

        # get all game questions
        if through_rd is None:
            game_questions = self.game.game_questions.filter(round_number__gt=0)
        else:
            game_questions = self.game.game_questions.filter(
                round_number__gt=0, round_number__lte=through_rd
            )

        question_count = len(game_questions)
        correct = round(question_count * percent_correct / 100)
        print(f"{correct} for team {self.team}")
        incorrect = question_count - correct
        # genearate a list of random True or False values based on the above percentages
        correct_values = random.sample(
            # counts only available >= 3.9 :(
            # [True, False], counts=[correct, incorrect], k=question_count
            ([True] * correct) + ([False] * incorrect),
            k=question_count,
        )
        resps = []
        for i, q in enumerate(game_questions):
            answer_correct = correct_values[i]
            answer = q.question.display_answer if answer_correct else ""
            resp = QuestionResponse(
                event=self.event,
                game_question=q,
                team=self.team,
                recorded_answer=answer
                if answer_correct
                else f"{q.id} wrong for team {self.team}",
                megaround_value=megaround_values.get(str(q.question_number))
                if q.round_number == selected_megaround
                else None,
                points_awarded=1 if answer_correct else 0,
            )
            resps.append(resp)

        QuestionResponse.objects.bulk_create(resps)

        # set the megaround on the leaderboard entry
        if selected_megaround is not None:
            LeaderboardEntry.objects.filter(event=self.event, team=self.team).update(
                selected_megaround=selected_megaround
            )


class HostActions:
    def __init__(self, event: TriviaEvent) -> None:
        self.event = event
        self.game = event.game

    def reveal_questions(self, key=None, rd_number=None):
        """Reveal a specific question from its key (i.e. 2.5) or all questions for a give round"""
        if key is None and rd_number is None:
            raise ValueError("One of key or rd_number is required")

    def grade(self):
        pass

    def lock(self, rd_number):
        EventRoundState.objects.update_or_create(
            event=self.event, round_number=rd_number, defaults={"locked": True}
        )
        resps = QuestionResponse.objects.filter(
            event=self.event, game_question__round_number=rd_number
        )
        resps.update(locked=True)
        LeaderboardProcessor(self.event).update_host_leaderboard(
            through_round=rd_number
        )

    def score(self, rd_number):
        EventRoundState.objects.update_or_create(
            event=self.event, round_number=rd_number, defaults={"scored": True}
        )

    def reveal_answers(self, rd_number):
        EventRoundState.objects.update_or_create(
            event=self.event, round_number=rd_number, defaults={"revealed": True}
        )

    def update_leaderboard(self):
        LeaderboardProcessor(self.event).sync_leaderboards()
