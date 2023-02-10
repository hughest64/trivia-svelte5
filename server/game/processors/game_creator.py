# game_creator.py
"""
Classes used to process airtable data and update or create game, round, and question data.
The dertermination to create new data or update existing data is based solely on the
game's meta data with the following criteria:
- Existing games are determined by the title (combination of date used, block code, and optionally
  'Sound' vs. 'xNoSound'). If a game with that title does not exist, a new one is created.
- Existing rounds are determined by the combination of the related game and round number. If the related
  game already has a round with a particular round numer, the existing round is updated.
- Existing questions are determined by the combination of the related round and question number. if the
  related round has a question with the particular question number, the existing question is updated.
- Question ids are not written back to Airtable as they are not used as a lookup value.
- Tiebreakers rounds (rd 0) are now tied to the game. They are excluded from the the game models serialize
  method via an exclude filter.
"""
from textwrap import dedent

import pandas as pd

from django.conf import settings
from django.db import transaction
from django.utils.safestring import mark_safe

from game.models import *
from game.processors.airtable_importer import AirtableData

PRIVATE_EVENT = bool(settings.PRIVATE_EVENT)

# TODO:
# logging
# testing - be sure to add a test that validates rd 0 is not fetched when serializing game data


class ProcedureError(Exception):
    def __init__(self, message=None) -> None:
        self.message = (
            message
            or "This method should not be called indepentently use the 'update_or_create' method to ensure proper trivia game creation."
        )

    def __str__(self):
        return self.message


def pluralize(value, plural_value=None):
    if plural_value is None:
        plural_value = "s"

    if isinstance(value, str):
        raise TypeError("only numbers and iterable collections are allowed")

    if isinstance(value, (int, float)) and value != 1:
        return plural_value

    if hasattr(value, "__iter__") and len(value) != 1:
        return plural_value

    return ""


def validate_sequence(sequence, drop_zero=True):
    """
    Validate a sequence of numbers and return a dict of
    information about missing and/or duplicated values
    """
    if not all([isinstance(val, int) for val in sequence]):
        raise ValueError("sequence must an iterable of integers")

    missing = set()
    duplicated = set()
    sorted_seq = sorted(sequence, reverse=True)
    for i, num in enumerate(sorted_seq):
        if drop_zero and num == 0:
            continue
        try:
            next_num = sorted_seq[i + 1]
            dif = num - next_num
            if dif == 0:
                duplicated.add(num)
            elif dif > 1:
                m_set = {num - i for i in range(1, dif)}
                missing.update(m_set)
        except IndexError:
            pass

    # TODO: I'd rather not convert to strings here, but it's mighty convienient later perhaps a kwarg?
    return dict(
        missing=[str(x) for x in missing], duplicated=[str(x) for x in duplicated]
    )


class TriviaGameCreator:
    """Create or update a single trivia game and all of the required parts. Methods other than
    update_or_create should not be called directly in order to respect atomic transaction handling
    """

    # TODO: use the enum from models
    general_knowledge_type = None  # QuestionType.objects.get(type="General Knowledge")

    def __init__(self, frame: pd.DataFrame, private_event: bool = PRIVATE_EVENT):
        raise NotImplementedError("The Game Creator class is not yet implemented")
        self.frame = frame
        self.private_event = private_event
        self.game = None
        self.no_sound_game = None
        self.private_event_instance = None
        self.total_new_games = 0
        self.total_new_rounds = 0
        self.total_new_questions = 0
        self.total_new_private_events = 0
        self.total_new_trivia_events = 0
        self.validation_data = self._validate_frame()

    def _validate_frame(self):
        round_numbers = set(self.frame.round_number)
        round_number_data = validate_sequence(round_numbers)
        question_number_data = []
        for rd_num in round_numbers:
            if rd_num == 0:
                continue
            q_frame = self.frame[self.frame.round_number == rd_num]
            seq = validate_sequence(list(q_frame.question_number))
            seq["rd_num"] = rd_num
            question_number_data.append(seq)

        return {
            "round_validation": round_number_data,  # standalone list
            "question_validation": question_number_data,  # list of objects (1 per round)
        }

    def _update_or_create_game(self, slug=None) -> Game:
        """Create or update a game object from the dataframe."""
        if slug is None:
            slug = ""
        first_row = self.frame.iloc[0]
        game_title = first_row.game_title + slug

        game, created = Game.objects.update_or_create(
            title=game_title,
            defaults={
                "block_code": first_row.block_code,
                "date_used": first_row.date_used,
            },
        )
        if created:
            self.total_new_games += 1

        return game

    # TODO: privaate events are not yet implemented
    def _update_or_create_private_event(self, rd_frame: pd.DataFrame) -> None:
        if self.game is None:
            raise ProcedureError
        data = rd_frame.iloc[0]
        self.private_event_instance, created = None, None
        # PrivateEvent.objects.update_or_create(
        #     name=data.pe_name,
        #     event_code=data.join_code,
        #     defaults={"date": data.date_used},
        # )
        if created:
            self.total_new_private_events += 1

    def _update_or_create_trivia_event_for_private_event(
        self, rd_frame: pd.DataFrame
    ) -> None:
        if self.game is None:
            raise ProcedureError
        try:
            pe_location = Location.objects.get(name="Private Event Location")
        except Location.DoesNotExist:
            raise RuntimeError(
                f"Cannot create trivia event for private event {self.private_event.name}. A location with the name 'Private Event Location' does not exist."
            )

        data = rd_frame.iloc[0]
        # TODO: update to match db architecture
        trivia_event, created = TriviaEvent.objects.update_or_create(
            game=self.game,
            private_event=self.private_event_instance,
            location=pe_location,
            is_private_event=True,
            # TODO: this should be configurable, somehow
            use_megaround=False,
            defaults={"date": data.date_used},
        )
        # TODO: js generator is not yet implemented, jc's are also no longer a table
        if created:
            trivia_event.join_code_id = (
                1234  # db.create_join_code("game").get("join_code_id")
            )
            trivia_event.save()
            self.total_new_trivia_events += 1

    def _update_or_create_round(self, rd_frame: pd.DataFrame) -> None:
        if self.game is None:
            raise ProcedureError

        round_data = rd_frame.iloc[0]
        round_number = round_data.round_number
        # TODO: we still need better handling of sound vs. no sound game creation
        if self.no_sound_game is not None and round_number == 9:
            round_number = 8
            game_round_queryset = self.no_sound_game.rounds.filter(
                round_number=round_number
            )
        else:
            game_round_queryset = self.game.rounds.filter(round_number=round_number)

        # TODO: update to match db Architecure
        if not game_round_queryset.exists():
            game_round = GameRound.objects.create(
                round_number=round_number,
                title=round_data.game_title,
                round_description=round_data.round_description,
                round_description_player=round_data.round_description_player,
            )
            self.total_new_rounds += 1
        else:
            game_round_queryset.update(
                title=round_data.game_title,
                round_description=round_data.round_description,
                round_description_player=round_data.round_description_player,
            )
            game_round = game_round_queryset[0]

        self._update_or_create_questions(game_round, rd_frame)

        if self.no_sound_game is not None and round_data.question_type != "Sound Round":
            self.no_sound_game.rounds.add(game_round)
        self.game.rounds.add(game_round)

    # TODO: deprecate
    @classmethod
    def lookup_question_type(cls, val):
        """
        Try to lookup a question type in the database,
        default to general knowledge if it doens't exist.
        """
        # try:
        #     return QuestionType.objects.get(type=val)
        # except QuestionType.DoesNotExist:
        #     return cls.general_knowledge_type\
        return

    # TODO: you know the drill by now
    def _update_or_create_questions(
        self, game_round: GameRound, rd_frame: pd.DataFrame
    ) -> None:
        if self.game is None:
            raise ProcedureError

        questions = []
        for i in range(len(rd_frame)):
            # we have the same M2M limitation here as in round creation
            row = rd_frame.iloc[i]
            question_queryset = game_round.questions.filter(
                question_number=row.question_number
            )
            created = False
            question_dict = dict(
                question_number=row.question_number,
                question_text=row.question_text,
                question_url=row.question_url,
                display_answer=row.display_answer,
                question_notes=row.question_notes,
                answer_notes=row.answer_notes,
                question_type=self.lookup_question_type(row.question_type),
                answers=row.answers,
            )
            if not question_queryset.exists():
                question = Question.objects.create(**question_dict)
                created = True
            else:
                question_queryset.update(**question_dict)
                question = question_queryset[0]

            questions.append(question)
            if created:
                self.total_new_questions += 1

        game_round.questions.set(questions)

    def update_or_create(self, commit=True):
        """create game data and commit to the database only if commit=True"""
        try:
            with transaction.atomic():
                round_numbers = set(self.frame.round_number)
                max_round = max(round_numbers)
                # create sound and no sound versions of the same game if it's not a private envent
                if max_round == 9 and not self.private_event:
                    self.game = self._update_or_create_game(slug=" - Sound")
                    self.no_sound_game = self._update_or_create_game(slug=" - xNoSound")
                else:
                    self.game = self._update_or_create_game()

                for num in round_numbers:
                    rd_frame = self.frame[self.frame.round_number == num]
                    self._update_or_create_round(rd_frame)

                if self.private_event:
                    self._update_or_create_private_event(rd_frame)
                    self._update_or_create_trivia_event_for_private_event(rd_frame)

                if commit == False:
                    raise RuntimeError("Transaction not commited!")

        except RuntimeError as e:
            # TODO: log e
            pass
            # print(e)

    def validation_data_html(self):
        """Format validation data as a user digestable string"""
        round_data, question_data = self.validation_data.values()
        if not round_data and not question_data:
            return None

        missing_rounds = ""
        duplicated_rounds = ""
        if round_data:
            mr = round_data.get("missing")
            if mr:
                missing_rounds = (
                    f"Possible missing round{pluralize(mr)}: {', '.join(mr)}"
                )
            dr = round_data.get("duplicated")
            if dr:
                duplicated_rounds = (
                    f"Possible duplicated round{pluralize(dr)}: {', '.join(dr)}"
                )

        missing_questions = ""
        duplicated_questions = ""
        if question_data:
            for data in question_data:
                rd_num = data.get("rd_num", "-")
                qm = data.get("missing")
                if qm:
                    missing_questions += f"Round {rd_num} may be missing question{pluralize(qm)} {', '.join(qm)}."
                qd = data.get("duplicated")
                if qd:
                    duplicated_questions += f"Round {rd_num} may have duplicate question number{pluralize(qd)} {', '.join(qd)}."

        if any(
            [missing_rounds, missing_questions, duplicated_rounds, duplicated_questions]
        ):
            msg = dedent(
                f"""
                <h1>Warning!</h1>
                <h2>Game {self.frame.iloc[0].game_title} May Have Missing and/or Extra Data:</h2>
                {missing_rounds}
                {duplicated_rounds}
                {missing_questions}
                {duplicated_questions}
            """
            ).strip()

            return mark_safe(msg)

        return None

    def summarize_transaction(self, verbose=False):
        """
        Return meta data about games, rounds, and questions created as an object or user digestable string. It does not return validation data. Validation
        data can be directly accessed as an object via the validation_data parameter or as an HTML safe string via the validation_data_html method.
        """
        if not self.game:
            raise ProcedureError(
                "A transaction summary is only available after the update_or_create method is called."
            )

        data = {
            "date_used": self.game.date_used,
            "games_created": self.total_new_games,
            "rounds_created": self.total_new_rounds,
            "questions_created": self.total_new_questions,
        }
        if self.private_event:
            data.update(
                {
                    "private_events_created": self.total_new_private_events,
                    "trivia_events_created": self.total_new_private_events,
                }
            )
        if not verbose:
            return data

        summary = (
            f"Created {self.total_new_games} new game{pluralize(self.total_new_games)}, "
            + f"{self.total_new_rounds} new round{pluralize(self.total_new_rounds)}, "
            + f"and {self.total_new_questions} new question{pluralize(self.total_new_questions)} for {self.game.date_used: %Y-%m-%d}"
        )
        if self.private_event:
            summary += (
                f" as well as {self.total_new_private_events} new private event{pluralize(self.total_new_private_events)} "
                + f"and {self.total_new_trivia_events} new trivia event{pluralize(self.total_new_private_events)}"
            )
        return summary

    def reset(self):
        """reset parameters"""
        self.game = None
        self.no_sound_game = None
        self.total_new_games = 0
        self.total_new_rounds = 0
        self.total_new_questions = 0


class TriviaGameFactory:
    """Produce multiple Trivia Events and collect all creation statistics"""

    def __init__(self, *frames, commit=True, private_event=PRIVATE_EVENT):
        raise NotImplementedError("The GameFactory class is not yet implemented")
        self.frames = frames
        self.private_event = private_event
        self.commit = commit
        self.stats = []
        self.validation_data_html = []

    def process(self):
        for frame in self.frames:
            game_data = TriviaGameCreator(frame, self.private_event)
            game_data.update_or_create(commit=self.commit)
            self.stats.append(game_data.summarize_transaction(verbose=False))
            validation = game_data.validation_data_html()
            if validation is not None:
                self.validation_data_html.append(validation)

    def get_statistics(self, verbose=False):
        dates_used = []
        total_new_games = 0
        total_new_rounds = 0
        total_new_questions = 0
        total_new_private_events = 0
        total_new_trivia_events = 0
        for s in self.stats:
            dates_used.append(s["date_used"])
            total_new_games += s["games_created"]
            total_new_rounds += s["rounds_created"]
            total_new_questions += s["questions_created"]
            total_new_private_events += s.get("private_events_created", 0)
            total_new_trivia_events += s.get("trivia_events_created", 0)

        if not verbose:
            data = {
                "dates_used": dates_used,
                "games_created": total_new_games,
                "rounds_created": total_new_rounds,
                "questions_created": total_new_questions,
            }
            if self.private_event:
                data.update(
                    {
                        "private_events_created": total_new_private_events,
                        "trivia_events_created": total_new_trivia_events,
                    }
                )
            return data

        if len(dates_used) == 1:
            date_text = f"for {dates_used[0]:%Y-%m-%d}"
        else:
            date_text = f"between dates {min(dates_used):%Y-%m-%d} and {max(dates_used):%Y-%m-%d}"

        summary = (
            f"Created {total_new_games} new game{pluralize(total_new_games)}, "
            + f"{total_new_rounds} new round{pluralize(total_new_rounds)}, and "
            + f"{total_new_questions} new question{pluralize(total_new_questions)} {date_text}"
        )

        if self.private_event:
            summary += (
                f" as well as {total_new_private_events} new private event{pluralize(total_new_private_events)} "
                + f"and {total_new_trivia_events} new trivia event{pluralize(total_new_trivia_events)}"
            )

        return summary


def create_games_from_airtable_data(
    private_event=PRIVATE_EVENT, commit=True, verbose=True, **kwargs
):
    """
    Convenience method which will import all airtable data for a given date range and create triva games from it.
    Extra keyword arguments (such as start and end) will be passed directly to the AirtableData class instance.
    """
    # should be a list of dataframes
    at_data = AirtableData(private_event=private_event, **kwargs).get_airtable_data()
    if isinstance(at_data, str):
        return {"stats": at_data}
    # probably validate that we have data then:
    factory = TriviaGameFactory(*at_data, commit=commit, private_event=private_event)
    factory.process()
    # this would be logged and displayed in the admin when running the import
    data = {
        "stats": factory.get_statistics(verbose=verbose),
        "validation": factory.validation_data_html,
    }
    return data
