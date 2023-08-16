from datetime import datetime, timedelta
import json

from django.conf import settings
from django.test import TestCase
from django.utils import timezone

import pandas as pd

from game.processors.airtable_importer import (
    AirtableData,
    COLUMN_LABEL_MAP,
    PE_COLUMNS,
    get_request_dates,
)

from game.models import *
from game.processors.game_creator import TriviaGameCreator, TriviaGameFactory


class AirtableImportTestCase(TestCase):
    def setUp(self):
        # or run a separate class for private?
        self.private_event = settings.PRIVATE_EVENT
        self.column_labels = {col["label"] for col in COLUMN_LABEL_MAP.values()}
        with open(settings.BASE_DIR / "game/tests/sample_data.json", "r") as gd:
            self.test_data = json.load(gd)

    @staticmethod
    def formatDate(date_string):
        return date_string.strftime("%Y-%m-%dT00:00:00")

    @staticmethod
    def dateToDatetime(d):
        striptz = d.split("T")[0]
        return datetime.strptime(striptz, "%Y-%m-%d")

    def getDateUsedSet(self, airtable_data):
        return {self.dateToDatetime(row.get("date_used", "")) for row in airtable_data}

    def test_dataframe_gets_proper_columns(self):
        """
        Ensures that all required columns in the dataframe before processing.
        It does not check for or remove extra columns.
        """
        df = pd.DataFrame(self.test_data)
        # ensure that the data is missing a needed column
        self.assertTrue("answer_notes" in df.columns)
        df.drop(columns=["answer_notes"], inplace=True)
        self.assertFalse("answer_notes" in df.columns)

        # ensure the missing column was added and that all requred columns are present
        cleaned_df = AirtableData()._validate_columns(df)
        self.assertTrue("answer_notes" in cleaned_df.columns)
        common_cols = cleaned_df.columns.intersection(set(self.column_labels))
        self.assertEqual(len(common_cols), len(self.column_labels))

    def test_proper_date_handling(self):
        """
        Ensure that dates passed to the the airtable query are handled properly
        """
        # expect a 9 day span around the current date if no dates are provided
        now = timezone.now()
        start = now - timedelta(days=now.weekday() + 1)
        end = start + timedelta(days=8)
        importer = AirtableData()
        self.assertEqual(
            importer.get_validated_lookup_dates(),
            (self.formatDate(start), (self.formatDate(end))),
        )

        # expect a delta of 1 day on either side of start and end
        monday = self.formatDate(datetime(2022, 10, 10))
        sunday = self.formatDate(datetime(2022, 10, 16))
        importer = AirtableData(start=monday, end=sunday)
        full_week = importer.get_validated_lookup_dates()
        self.assertEqual(full_week, ("2022-10-09T00:00:00", "2022-10-17T00:00:00"))
        importer = AirtableData(start="2022/10/19", end="2022/10/19")
        single_date = importer.get_validated_lookup_dates()
        self.assertEqual(single_date, ("2022-10-18T00:00:00", "2022-10-20T00:00:00"))

        self.assertEqual(
            AirtableData(start="2022-10/9").get_validated_lookup_dates(),
            ("2022-10-08T00:00:00", "2022-10-10T00:00:00"),
        )
        self.assertEqual(
            AirtableData(end="2022-10/9").get_validated_lookup_dates(),
            ("2022-10-08T00:00:00", "2022-10-10T00:00:00"),
        )

    def test_get_airtable_data(self):
        # test with various date ranges (single, start-end, full-week)
        # single date
        atdata = AirtableData(start="2022-10-5").get_airtable_data(raw=True)
        atdata_dates_used = self.getDateUsedSet(atdata)
        self.assertTrue(self.dateToDatetime("2022-10-5") <= min(atdata_dates_used))
        self.assertTrue(self.dateToDatetime("2022-10-5") >= max(atdata_dates_used))

        # start and end dates
        atdata = AirtableData(start="2022-10-5", end="2022-10-10").get_airtable_data(
            raw=True
        )
        atdata_dates_used = self.getDateUsedSet(atdata)
        self.assertTrue(self.dateToDatetime("2022-10-5") <= min(atdata_dates_used))
        self.assertTrue(self.dateToDatetime("2022-10-10") >= max(atdata_dates_used))

        # full week is a special case as it may not have any data or only have some data for the week
        full_start, full_end = get_request_dates()
        full_week_data = AirtableData().get_airtable_data(raw=True)
        row_count = len(full_week_data)
        if row_count == 0:
            print("no data found for full week test, skipping")
            return

        full_week_dates_used = self.getDateUsedSet(full_week_data)
        self.assertTrue(self.dateToDatetime(full_start) <= min(full_week_dates_used))
        self.assertTrue(self.dateToDatetime(full_end) >= max(full_week_dates_used))

    def test_process_airtable_data(self):
        # fetch data but do not split into multiple frames
        importer = AirtableData()
        at_data = importer.get_airtable_data(split=False)
        if len(at_data) == 0:
            print(f"No data found for dates {importer.get_validated_lookup_dates()}")
            # use the fallback spreadsheet
            at_data = importer.process_airtable_data(self.test_data)

        self.assertIsInstance(at_data, pd.DataFrame)
        # all columns are represented
        for col in COLUMN_LABEL_MAP.values():
            # skip pe only columns if it's not pe
            if not importer.private_event and col["label"] in PE_COLUMNS:
                continue
            self.assertTrue(col["label"] in at_data.columns)

    # TODO:
    # - test the private event parameter to the AirtableData class
    # - ensure the proper airtable base id and table names are used for the import


# TODO: add test for the use_sound field
class GameCreatorTestCase(TestCase):
    def setUp(self) -> None:
        # game data from the week of 1/16/23 = 1/22/23
        with open(settings.BASE_DIR / "game/tests/game_data.json", "r") as gd:
            standard_game_data = json.load(gd)

        with open(settings.BASE_DIR / "game/tests/pe_data.json", "r") as ped:
            pe_data = json.load(ped)

        # to avoid running exta at imports, read raw at data in from files
        self.standard_frames = AirtableData.create_date_frames(
            AirtableData.process_airtable_data(standard_game_data)
        )
        self.pe_frames = AirtableData.create_date_frames(
            AirtableData.process_airtable_data(pe_data)
        )

        # create private event location
        Location.objects.create(name="Private Event Location")

    def tearDown(self) -> None:
        Location.objects.all().delete()
        TriviaEvent.objects.all().delete()
        # PrivateEvent.objects.all().delete()
        Question.objects.all().delete()
        GameRound.objects.all().delete()
        Game.objects.all().delete()

    def test_standard_game_creation(self):
        """Test the creation and updating of a trivia game from airtable data"""
        game_frame = self.standard_frames[0]
        total_questions = len(game_frame)
        total_rounds = len(set(game_frame.round_number))
        gc = TriviaGameCreator(game_frame, private_event=False)
        gc.update_or_create()

        # total questions and rounds match what is in the data frame
        self.assertEqual(total_questions, Question.objects.all().count())
        # 2 games * 9 rounds each (0-8)
        self.assertEqual(18, GameRound.objects.all().count())
        # 2 games were created
        self.assertEqual(2, Game.objects.all().count())

        # summary data shows the correct number of creations
        summary = gc.summarize_transaction()
        # 45 regular and 3 tiebreakers for each of 2 games = 96 GameQuestions created
        self.assertEqual(96, summary.get("questions_created"))
        self.assertEqual(18, summary.get("rounds_created"))
        self.assertEqual(2, summary.get("games_created"))

        # no game data is missing
        self.assertIsNone(gc.validation_data_html())

        updated_title = "Updated Title"
        updated_question_text = "different question text"
        rd2_indicies = game_frame[game_frame.round_number == 2].index
        rd2_q1_index = game_frame[
            (game_frame.round_number == 2) & (game_frame.question_number == 1)
        ].index
        game_frame.loc[rd2_indicies, "round_title"] = updated_title
        game_frame.loc[rd2_q1_index, "question_text"] = updated_question_text
        gc = TriviaGameCreator(game_frame, private_event=False)
        gc.update_or_create()

        # a new question was created
        self.assertEqual(total_questions + 1, Question.objects.all().count())
        # no new GameQuestions
        self.assertEqual(96, summary.get("questions_created"))

        # 2 games * 9 rounds each (0-8)
        self.assertEqual(18, GameRound.objects.all().count())
        self.assertEqual(2, Game.objects.all().count())

        rnd = GameRound.objects.filter(round_number=2)[0]
        quest = GameQuestion.objects.filter(
            question_number=1, round_number=rnd.round_number
        )[0]

        # round title and question text should be updated
        self.assertEqual(updated_question_text, quest.question.question_text)
        self.assertEqual(rnd.title, updated_title)

        # the summary reports 0 creations
        summary = gc.summarize_transaction()
        self.assertEqual(0, summary.get("questions_created"))
        self.assertEqual(0, summary.get("rounds_created"))
        self.assertEqual(0, summary.get("games_created"))

    # TODO: open this back up after private event implementation
    # def test_private_event_game_creation(self):
    #     """Test that the private event and trivia event ojbects are also created for private events"""
    #     # this test (and other pe tests) will likely fail on the standard event server as the pe tables don't exist there
    #     if not settings.PRIVATE_EVENT:
    #         print("skipping private event test")
    #         return

    #     pe_frame = self.pe_frames[0]
    #     gc = TriviaGameCreator(pe_frame, private_event=True)
    #     gc.update_or_create()
    #     # only one game should be created (sound vs. no sound is not considered)
    #     self.assertEqual(1, PrivateEvent.objects.all().count())
    #     self.assertEqual(1, Event.objects.all().count())
    #     summary = gc.summarize_transaction()
    #     self.assertEqual(1, summary.get("trivia_events_created"))
    #     self.assertEqual(1, summary.get("private_events_created"))

    #     # re-running the creator does not create new data
    #     gc = TriviaGameCreator(pe_frame, private_event=True)
    #     gc.update_or_create()
    #     # only one game should be created (sound vs. no sound is not considered)
    #     self.assertEqual(1, PrivateEvent.objects.all().count())
    #     self.assertEqual(1, Event.objects.all().count())
    #     summary = gc.summarize_transaction()
    #     self.assertEqual(0, summary.get("trivia_events_created"))
    #     self.assertEqual(0, summary.get("private_events_created"))

    def test_one_rd_8_per_game(self):
        """Test that standard data creates to games each with a different round 8"""
        game_frame = self.standard_frames[0]
        gc = TriviaGameCreator(game_frame, private_event=False)
        gc.update_or_create()

        # 2 games total, one each for sound and no sound
        games = Game.objects.all()
        self.assertEqual(len(games), 2)
        sound_games = games.filter(title__endswith="- Sound")
        self.assertEqual(len(sound_games), 1)
        no_sound_games = games.filter(title__endswith=" - xNoSound")
        self.assertEqual(len(no_sound_games), 1)

        sg = sound_games[0]
        nsg = no_sound_games[0]
        sg_rd_numbers = [r.round_number for r in sg.game_rounds.all()]
        nsg_rd_numbers = [r.round_number for r in nsg.game_rounds.all()]

        # each game ends with round 8
        self.assertEqual(max(sg_rd_numbers), 8)
        self.assertEqual(max(nsg_rd_numbers), 8)

        # each game only has one round 8
        self.assertEqual(len(sg.game_rounds.filter(round_number=8)), 1)
        self.assertEqual(len(nsg.game_rounds.filter(round_number=8)), 1)

    def test_missing_and_duplicate_data(self):
        """Test that the validator properly reports missing and duplicate data"""
        game_frame = self.standard_frames[0]
        r3_q2_index = game_frame[
            (game_frame.round_number == 3) & (game_frame.question_number == 2)
        ].index
        game_frame.loc[
            r3_q2_index, "question_number"
        ] = 3  # dupilcate a question number for
        mod_frame = game_frame[game_frame.round_number != 2]  # drop round 2
        gc = TriviaGameCreator(mod_frame, private_event=False)
        gc.update_or_create()
        # print(gc.validation_data)
        val_data = gc.validation_data
        # round 2 is misssing
        self.assertEqual(val_data["round_validation"]["missing"], ["2"])
        # round 3 has a duplicate and missing question number
        quest_val = val_data["question_validation"]
        rd_3 = [data for data in quest_val if data.get("rd_num") == 3][0]
        self.assertEqual(rd_3["missing"], ["2"])
        self.assertEqual(rd_3["duplicated"], ["3"])

    def test_commit_false(self):
        """Test that commit=False runs the creator but does not commit anything to the database"""
        frame = self.standard_frames[0]
        gc = TriviaGameCreator(frame, private_event=False)
        gc.update_or_create(commit=False)
        summary = gc.summarize_transaction()
        # summary shows things created
        self.assertGreater(summary.get("questions_created"), 0)
        self.assertGreater(summary.get("rounds_created"), 0)
        self.assertGreater(summary.get("games_created"), 0)
        # but nothing exists in the database
        self.assertFalse(Question.objects.all().exists())
        self.assertFalse(GameRound.objects.all().exists())
        self.assertFalse(Game.objects.all().exists())

    def test_tiebreaker_questions(self):
        """Test to ensure that tiebreaker questions are not duplicated on rerun of the creator"""
        frame = self.standard_frames[0]
        gc = TriviaGameCreator(frame, private_event=False)
        gc.update_or_create()
        # self.assertEqual(GameQuestion.objects.filter(question_number=0).count(), 3)
        print(GameQuestion.objects.filter(question_number=0))
        # gc = TriviaGameCreator(frame, private_event=False)
        # gc.update_or_create()
        # self.assertEqual(GameQuestion.objects.filter(question_number=0).count(), 3)
