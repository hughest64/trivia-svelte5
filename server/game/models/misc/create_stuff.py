import json
from django.conf import settings
from ..trivia_event import *

"""
NOTE: Keeping this for now just for reference, it may be useful when creating utititles
such as creating events
"""


def get_question_type_value(string_value):
    """return the int value from the tuple if the strings match or 0 by default"""
    # QUESTION_TYPES is a list of tuples (int, string) imported from .trivia_event
    for value, string in QUESTION_TYPES:
        if string == string_value:
            return value

    return 0

def q_types():
    print (QUESTION_TYPES)

def get_data():
    with open(settings.BASE_DIR.parent / "data" / "game_data_merged.json", 'r') as f:
        data = json.load(f)
        rounds = data.get("rounds", [])
    return rounds


def check_data_file():
    data = get_data()
    print(data)


def delete_the_things():
    """delete all the things to start clean"""
    EventQuestionState.objects.all().delete()
    EventRoundState.objects.all().delete()
    GameQuestion.objects.all().delete()
    GameRound.objects.all().delete()
    Question.objects.all().delete()


def create_the_things():
    """create the things"""
    delete_the_things()
    game = Game.objects.all().first()
    event = TriviaEvent.objects.all().first()
    rounds = get_data()

    for round in rounds:
        GameRound.objects.create(
            game=game,
            title=round.get("title", ""),
            round_description=round.get("round_description", ""),
            round_number=round.get("round_number", ""),
        )
        EventRoundState.objects.create(
            event=event,
            round_number=round.get("round_number", 1),
        )
        for question in round["questions"]:
            quest = Question.objects.create(
                question_type = get_question_type_value(question.get("question_type", "General Knowledge")),
                question_text = question.get("text", ""),
                question_url = question.get("questin_url", ""),
                display_answer = question.get("answer", ""),
                # we don't have any of these
                answer_notes = question.get("quesion_notes", ""),
            ) 
            GameQuestion.objects.create(
                game=game,
                question=quest,
                round_number = round.get("round_number", 1),
                question_number = question.get("question_number", 1)
            )
            EventQuestionState.objects.create(
                event=event,
                round_number = round.get("round_number", 1),
                question_number = question.get("question_number", 1),
            )

    with open(settings.BASE_DIR.parent / "data" / "event_data.json", "w") as f:
        json.dump(event.to_json(), f, indent=4)
