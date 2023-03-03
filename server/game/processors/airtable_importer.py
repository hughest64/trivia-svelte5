import datetime
from dateutil.parser import ParserError
import logging
import os
import time
from typing import List

import pandas as pd
import requests

from django.conf import settings

logger = logging.getLogger(__name__)

COLUMN_LABEL_MAP = {
    "pe_name": {"label": "pe_name", "default_value": str},  # PE only
    "join_code": {"label": "join_code", "default_value": str},  # PE only
    "Block Code": {"label": "block_code", "default_value": str},
    "date_used": {"label": "date_used", "default_value": str},
    "round_number": {"label": "round_number", "default_value": str},
    "question_number": {"label": "question_number", "default_value": str},
    "round_title": {"label": "round_title", "default_value": str},
    "round_description": {"label": "round_description", "default_value": str},
    "round_description_player": {
        "label": "round_description_player",
        "default_value": str,
    },
    "question": {"label": "question_text", "default_value": str},
    "answer": {"label": "display_answer", "default_value": str},
    "question_notes": {"label": "question_notes", "default_value": str},
    "answer_notes": {"label": "answer_notes", "default_value": str},
    "alternate_answers": {"label": "answers", "default_value": str},
    # "Era" # - this not currently handled by the script or database
    "round_type": {"label": "question_type", "default_value": str},
    # TODO: Do we actually need this for triva events?
    "Slideshow": {"label": "slideshow", "default_value": str},
    "Image URL": {"label": "image_url", "default_value": str},
    "Sound URL": {"label": "sound_url", "default_value": str},
    "airtable_id": {"label": "airtable_id", "default_value": str},
}

PRIVATE_EVENT = bool(settings.PRIVATE_EVENT)
AIRTABLE_API_TOKEN = os.environ.get("AIRTABLE_API_TOKEN")
# TODO: these should all be env variables so the app doesn't need to be updated if something changes
BASE_URL = "https://api.airtable.com/v0"
BASE_ID = "appn2NrdqfRDv6eHC"
TABLE_NAME = "The Everything Box (Question Database)"
PE_TABLE_NAME = "tblD2FocmowArRhOA"
PE_BASE_ID = "appnqaagDcrCoFGdG"
# columns only required by private events
PE_COLUMNS = ["pe_name", "join_code"]


def get_request_dates():
    """Set start and end dates one day prior to Monday and one day after Sunday
    for the current week, which is necessary for airtable's date filters
    dates are in iso format without the timestamp. i.e. "2021-07-18"
    """
    today = pd.to_datetime(datetime.date.today())
    start_timestamp = (
        today
        if today.day_name().lower() == "monday"
        else today - pd.offsets.Week(weekday=0)
    ) - pd.Timedelta(1, unit="days")
    end_timestamp = (
        today
        if today.day_name().lower() == "sunday"
        else today + pd.offsets.Week(weekday=6)
    ) + pd.Timedelta(1, unit="days")

    start_date = start_timestamp.isoformat()
    end_date = end_timestamp.isoformat()

    return (start_date, end_date)


class AirtableData:
    """Import data from airtable and optionally convert to a cleaned Pandas Dataframe"""

    private_event = PRIVATE_EVENT

    def __init__(
        self,
        private_event=None,
        token=AIRTABLE_API_TOKEN,
        base_url=BASE_URL,
        base_id=None,
        headers=None,
        table_name=None,
        start=None,
        end=None,
    ):
        # only update if explicitly passed a value
        if private_event is not None:
            self.private_event = private_event
        self.token = token
        self.headers = {"Authorization": token}
        if isinstance(headers, dict):
            self.headers.update(headers)
        self.base_url = base_url
        # prefer a user provided base/table name, else use a default depending on the private event setting
        self.base_id = base_id or (BASE_ID if not self.private_event else PE_BASE_ID)
        self.table_name = table_name or (
            TABLE_NAME if not self.private_event else PE_TABLE_NAME
        )
        self.request_url = f"{self.base_url}/{self.base_id}/{self.table_name}"
        self.start = start
        self.end = end
        self._validate_init()
        self._validate_lookup_dates()

    # TODO: this could be expanded a good deal
    def _validate_init(self) -> None:
        if not self.token:
            message = "Missing Airtable API Token"
            # TODO: better error message handling
            logger.error(message)
            raise ValueError(message)

    def _validate_lookup_dates(self) -> None:
        """validate and start and end dates to be used in an airtable query. Dates are rolled
        one day on either side of the input date in order to account for the fact that airible
        queries are non-inclusve of the date provided
        - when neither param is provided a defualt 9 day range representing the current week is returned
        - when only start or end is provided a 3 day range around the provided is returned
        - when both parms are provided start returns 1 day prior and end retuns one day later
        """

        if self.start is None and self.end is None:
            start_date, end_date = get_request_dates()

        else:
            try:
                start_date = (
                    pd.to_datetime(self.start or self.end)
                    - pd.Timedelta(1, unit="days")
                ).isoformat()
                end_date = (
                    pd.to_datetime(self.end or self.start)
                    + pd.Timedelta(1, unit="days")
                ).isoformat()
            except ParserError:
                message = "please pass dates in month/day/year or year/month/day format"
                logger.error(
                    f"bad date(s) passed to create_game() start: {self.start}, end: {self.end}"
                )
                raise ValueError(message)

        self.start = start_date
        self.end = end_date

    def get_validated_lookup_dates(self):
        """convenience method which returns cleaned start and end dates as a two tuple"""
        return (self.start, self.end)

    def get_airtable_data(self, raw=False, split=True):
        """Request data from airtable for the provided start and end dates. If raw == True a list of dictionaires (one dict per row)
        is returned and the split parameter is ignored. If raw == false (the default) a cleaned Pandas Dataframe is created. from
        the imported data. If split == True a list of DataFrames split by block code is returned, Otherwise the entire Dataframe is returned.

        If start and end dates are not provided the beginning and end of the current week are used. NOTE: start and end dates are rolled
        one day before and one day after the dates for which data is needed as the Airtiable Query is non-inclusive.
        """
        logger.info(f"Beginning Airtable import at {datetime.datetime.now()}\n")

        date_filter = f"AND(IS_AFTER({{date_used}},{self.start!r}),IS_BEFORE({{date_used}},{self.end!r}))"
        logger.info(f"Airtable API date filter:\n{date_filter}")
        params = {"filterByFormula": date_filter}
        session = requests.session()

        records_list = []
        has_next_page = True
        loop_count = 0
        # Airtable has a rate limit of 5 requests/second, if we exceed that we get locked out for 30 seconds
        while has_next_page:
            if loop_count <= 5:
                logger.info(f"request loop count: {loop_count}")
                try:
                    resp = session.get(
                        url=self.request_url, headers=self.headers, params=params
                    )
                    resp.raise_for_status()

                except requests.exceptions.HTTPError as e:
                    logger.error(f"{resp.status_code}, {resp.reason}\n{resp.text}")
                    has_next_page = False
                    raise SystemExit(e)

                else:
                    logger.info(f"{resp.status_code}, {resp.reason}")
                    data = resp.json()
                    records_list.extend(data.get("records"))
                    offset = data.get("offset")

                    if offset:
                        logger.info(f"updating the offset to: {offset}")
                        params.update({"offset": data.get("offset")})
                    else:
                        has_next_page = False
                    loop_count += 1
            else:
                # wait a bit, then proceed
                time.sleep(0.5)
                loop_count = 0

        logger.info(f"Fetched {len(records_list)} record(s) from Airtable")

        df_row_data = []
        for record in records_list:
            fields = record.get("fields")
            # add the airtable id to the dataframe
            fields["airtable_id"] = record.get("id")
            df_row_data.append(fields)

        if len(df_row_data) == 0:
            return f"No airtable data was found for dates: {self.start or 'N/A'} and {self.end or 'N/A'}."

        if raw == True:
            return df_row_data
        else:
            cleaned_df = self.process_airtable_data(df_row_data)
        if split == True:
            return self.create_date_frames(cleaned_df)
        return cleaned_df

    @classmethod
    def _validate_columns(cls, df: pd.DataFrame) -> pd.DataFrame:
        """rename existing columns to match database table columns and add dummy columns for missing data"""
        data_cols = {
            k: v["label"] for k, v in COLUMN_LABEL_MAP.items() if k in df.columns
        }
        df.rename(columns=data_cols, inplace=True)

        missing_cols = []
        for i, col_data in enumerate(COLUMN_LABEL_MAP.values()):
            label = col_data["label"]
            # skip these if it's not a private event
            if label in PE_COLUMNS and not cls.private_event:
                continue
            # add default data for missing columns
            col_value = col_data["default_value"]()
            if label not in df.columns:
                missing_cols.append((i, label))
                df.insert(i, label, col_value)
        # TODO: log properly
        print("added the following columns to the dataframe:", missing_cols)
        return df

    @classmethod
    def _map_answers_list(cls, answers: str):
        """Split a comma (and/or space) separated string of accepted answers into an array"""
        if not isinstance(answers, str):
            raise ValueError(
                f"Cannot parse additional accepted answers for value {answers}"
            )
        cleaned_string = (
            str(answers).replace(", ", ",").replace("[", "").replace("]", "")
        )
        return cleaned_string.split(",") if cleaned_string else []

    @classmethod
    def _map_question_url(cls, url_type, image_url, sound_url):
        """map url columns to a single url column"""
        return image_url if url_type == "Image Round" else sound_url

    @classmethod
    def process_airtable_data(cls, airtable_data: dict) -> pd.DataFrame:
        """convert a list of dicts (airtable records) to a dataframe and clean the data"""
        df = cls._validate_columns(pd.DataFrame(airtable_data).fillna(""))

        df["question_url"] = list(
            map(cls._map_question_url, df.question_type, df.image_url, df.sound_url)
        )

        # add 0 for missing round/question numbers and convert to int
        df["round_number"] = df["round_number"].replace("", 0).apply(int)
        df["question_number"] = df["question_number"].replace("", 0).apply(int)

        # keep date used as a datetime index
        df["date_used"] = df["date_used"].apply(pd.to_datetime)

        try:
            df["answers"] = df["answers"].apply(cls._map_answers_list)
        except ValueError as e:
            df.drop("answers", axis=1)
            logger.error(f"error in processing alternate answers column\n{e}")

        # strip whitespace from all columns, set and sort the index
        df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x).sort_values(
            ["date_used", "round_number", "question_number"]
        )
        return df

    @classmethod
    def _game_title(cls, date, block_code):
        return f"{date:%Y%m%d} - {block_code}"

    @classmethod
    def _round_question(cls, round, question):
        return f"{round}.{question}"

    @classmethod
    def create_date_frames(cls, df):
        """Break the dataframe in to a list of dataframes by a combination of date_used and
        block code. sort by round number first, then question number. For each game, validate
        that the combination of round and question number is unique. If not, throw an error
        to let the user know there may be an issue.
        """
        # use combination of date and block code to identify a game
        df["game_title"] = list(map(cls._game_title, df["date_used"], df["block_code"]))

        # used to ensure a frame (game) does not contain duplicate round/question combinations
        df["rd_quest"] = list(
            map(cls._round_question, df["round_number"], df["question_number"])
        )

        date_frames = []
        for title in set(df.game_title):
            frame = df[df.game_title == title].sort_values(
                by=["round_number", "question_number"]
            )
            # all tie breakers have 0.0 as the question number, so allow duplicates for them
            not_unique = {
                val
                for val in (frame[frame.rd_quest.duplicated()].rd_quest)
                if val != "0.0"
            }

            if len(not_unique) == 0:
                date_frames.append(frame)
            else:
                err_msg = f"Game {title} may have duplicates for the following question(s):\n{', '.join(not_unique)}."
                logger.error(err_msg)
                raise ValueError(
                    err_msg + " Please correct the error(s) and try the import again."
                )

        # sort  the frames by date
        return sorted(date_frames, key=lambda f: f.iloc[0].date_used)
