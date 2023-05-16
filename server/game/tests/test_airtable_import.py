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
        # TODO: used fixed dates which will likely always have data (last week?)
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

    # TODO: this test isn't really useful as is, maybe upate to test for failure?
    # i.e force another game title into the data and assert that an error is raised
    def test_game_dataframes(self):
        importer = AirtableData()
        at_data = importer.get_airtable_data(split=False)
        if len(at_data) == 0:
            print(f"No data found for dates {importer.get_validated_lookup_dates()}")
            # use the fallback spreadsheet
            at_data = importer.process_airtable_data(self.test_data)

        frames = importer.create_date_frames(at_data)

        self.assertIsInstance(frames, list)

        # TODO: _game_name is no longer a method of the AirtableData class
        # unique_games = set(map(importer._game_name, at_data["date_used"], at_data["block_code"]))
        # self.assertEqual(len(unique_games), len(frames))

    # TODO:
    # - test the private event parameter to the AirtableData class
    # - ensure the proper airtable base id and table names are used for the import


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
        self.assertEqual(total_rounds, GameRound.objects.all().count())
        # 2 games were created
        self.assertEqual(2, Game.objects.all().count())

        # summary data shows the correct number of creations
        summary = gc.summarize_transaction()
        self.assertEqual(total_questions, summary.get("questions_created"))
        self.assertEqual(total_rounds, summary.get("rounds_created"))
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

        # no new data was created
        self.assertEqual(total_questions, Question.objects.all().count())
        # TODO: FAIL 10 != 18
        self.assertEqual(total_rounds, GameRound.objects.all().count())
        self.assertEqual(2, Game.objects.all().count())
        rnd = GameRound.objects.get(round_number=2)
        quest = Question.objects.get(question_number=1, round=rnd)

        # round title and question text should be updated
        self.assertEqual(updated_question_text, quest.question_text)
        self.assertEqual(rnd.title, updated_title)

        # the summary reports 0 creations
        summary = gc.summarize_transaction()
        self.assertEqual(0, summary.get("questions_created"))
        self.assertEqual(0, summary.get("rounds_created"))
        self.assertEqual(0, summary.get("games_created"))

    # def test_private_event_game_creation(self):
    #     """Test that the private event and trivia event ojbects are also created for private events"""
    #     # TODO: this test (and other pe tests) will likely fail on the standard event server as the pe tables don't exist there
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

    def test_round_reuse(self):
        """Test that round question data may be reused in a different game with a different round number"""
        # borrow round 3 from the first game and use it as round 5 in the second game
        f1 = self.standard_frames[0]
        new_rd = pd.DataFrame(f1[f1.round_number == 3])
        new_rd.round_number = 5
        f2 = self.standard_frames[1]
        f3 = f2[f2.round_number != 5]
        joined_f3 = pd.concat([f3, new_rd]).sort_values(
            ["round_number", "question_number"]
        )

        # validate the df rework
        self.assertEqual(len(joined_f3[joined_f3.round_number == 5]), 5)
        self.assertEqual(len(joined_f3[joined_f3.round_number == 3]), 5)

        gf = TriviaGameFactory(f1, joined_f3, private_event=False)
        gf.process()
        stats = gf.get_statistics()
        # each frame has a sound and and no sound game
        self.assertEqual(stats["games_created"], 4)
        # TODO: FAIL 36 != 20
        # each frame should create 10 rounds
        self.assertEqual(stats["rounds_created"], 20)

        f1_title = f1.iloc[0].game_title
        f1_game = Game.objects.get(title=f1_title + " - Sound")
        f1_rd3 = GameRound.objects.get(game=f1_game, round_number=3)

        f3_title = f3.iloc[0].game_title
        f3_game = Game.objects.get(title=f3_title + " - Sound")
        f3_rd5 = GameRound.objects.get(game=f3_game, round_number=5)
        # round titles are the same between games
        self.assertEqual(f1_rd3.title, f3_rd5.title)
        # question text is the same between games
        for f1q in f1_rd3.questions.all():
            f3q = f3_rd5.questions.filter(
                question_number=f1q.question_number, question_text=f1q.question_text
            )
            # text and question number should match in the duplicated round
            self.assertEqual(f3q.count(), 1)

        # the game with the duplication has the correct rounds
        self.assertEqual(f3_game.rounds.filter(round_number=3).count(), 1)
        self.assertEqual(f3_game.rounds.filter(round_number=5).count(), 1)

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

    # TODO: (nice to haves)
    # - test the create helper?
    # -- test return value (no validation data) when there is no data vs when there is data (has validation data)
    # - test the management command?
    # - test the airtable view?
    # -- auth, query params, etc
