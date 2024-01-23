# devcmd.py
"""
A management command for testing out utility features under development
"""

from django.core.management.base import BaseCommand

from game.models import *
from game.utils.number_convertor import NumberConvertor, NumberConversionException

gq_id = 581
event_id = 2
team_id = 8

ans = "65,0000"


class Command(BaseCommand):
    def handle(self, *args, **options):
        resp, _ = TiebreakerResponse.objects.update_or_create(
            game_question_id=gq_id,
            event_id=event_id,
            team_id=team_id,
            defaults={"recorded_answer": ans, "round_number": 1},
        )

        print(resp.grade)
