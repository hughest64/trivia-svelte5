from game.models import *
from game.processors import LeaderboardProcessor, TriviaEventCreator

from user.models import User


class GameActions(TriviaEventCreator):
    def __init__(
        self,
        game: Game,
        joincode: int = None,
        team_count: int = None,
        auto_create=False,
        **kwargs,
    ) -> None:
        super().__init__(game, joincode, auto_create, **kwargs)

        if not auto_create:
            self.set_existing_event()

        # number of teams to create and add to the event
        self.team_count = team_count
        self.players = []
        self.teams = []

        if self.team_count > 0:
            self.create_teams()
            self.add_teams_to_event()

    def set_existing_event(self, reset=True):
        self.event = TriviaEvent.objects.get(joincode=self.joincode)
        self.game = self.event.game
        if reset:
            self.event.round_states.update(locked=False, scored=False, revealed=False)
            QuestionResponse.objects.filter(event=self.event).delete()
            LeaderboardEntry.objects.filter(event=self.event).delete()

    def create_teams(self):
        """Create the desired number of teams and player user per teams"""
        for i in range(1, self.team_count + 1):
            team, _ = Team.objects.get_or_create(
                name=f"run_game_team_{i}", password=f"run_game_team_{i}"
            )
            user, created = User.objects.get_or_create(
                username=f"run_game_user_{i}",
                defaults={"active_team": team, "password": 12345},
            )
            if created:
                user.set_password("12345")
                user.save()

            team.members.add(user)
            self.players.append(user)
            self.teams.append(team)

    def add_teams_to_event(self):
        """Add teams to the event"""
        # create leaderboard entries for each team (based off of user active team)
        for team in self.teams:
            LeaderboardEntry.objects.get_or_create(
                event=self.event, team=team, leaderboard_type=LEADERBOARD_TYPE_HOST
            )
            LeaderboardEntry.objects.get_or_create(
                event=self.event, team=team, leaderboard_type=LEADERBOARD_TYPE_PUBLIC
            )
        self.event.event_teams.set(self.teams)
        self.event.players.set(self.players)


# provide various getters/setters to update the db to simulate game play
class TeamActions:
    def __init__(self, event: TriviaEvent, team: Team) -> None:
        self.event = event
        self.game = event.game
        self.team = team

    def answer_questions(
        self, rd_num: int, question_count: int = None, points_awarded: int = None
    ):
        """Answer a set of questions for for an event round"""
        rd_questions = self.game.game_questions.filter(round_number=rd_num)
        if question_count is not None:
            rd_questions = rd_questions[: (question_count - 1)]
        points_available = points_awarded

        for q in rd_questions:
            resp = QuestionResponse(
                event=self.event,
                game_question=q,
                team=self.team,
                # how do we handle this? use some condition to lookup the correct answer
                recorded_answer="maybe look me up, or get it wrong or purpose",
            )
            # this works, but doesn't allow random point assigning, I think that's ok at least for now
            if points_available >= 1:
                resp.points_awarded = 1
                points_available -= 1
            elif points_available == 0.5:
                resp.points_awarded = 0.5
                points_available = 0

            resp.save()

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
