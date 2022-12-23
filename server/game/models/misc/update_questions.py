"""
Helper file to update questions to use the QuestionAnswer model
"""

import json
from django.conf import settings
from game.models import *

fp = settings.BASE_DIR / "fixtures/dbdump.json"


def parse_q_data(q_data):
    fields = q_data.get("fields", {})
    return (q_data.get("pk"), fields.get("display_answer"))


def get_question_list():
    with open(fp, "r") as f:
        db_data = json.load(f)

    return [
        parse_q_data(q_data)
        for q_data in db_data
        if q_data.get("model") == "game.question"
    ]


def reindex_questions():
    questions = Question.objects.all()
    print(f"reindexing {questions.count()} quesitons")
    for i, q in enumerate(questions, start=1):
        q.id = i
        q.save()
    print("done")


def update_question_answers():
    q_list = get_question_list()
    for pk, text in q_list:
        try:
            quest = Question.objects.get(id=pk)
        except Question.DoesNotExist:
            print(f"could not find question with pk {pk}")
            continue

        answer, _ = QuestionAnswer.objects.get_or_create(text=text)
        quest.display_answer = answer
        quest.accepted_answers.set([answer])
        quest.save()
        print(f"updated question with text {pk}")
