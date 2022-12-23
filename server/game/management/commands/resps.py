import json

from django.conf import settings
from django.core.management.base import BaseCommand

from game.tests.utils import GameCreator

response_fp = settings.BASE_DIR / "game/fixtures/twitch_resps.json"


class Command(BaseCommand):
    help = "Create a boat load of responses for event 9998.\
        pulled from Twitch, 20221208 - C - Sound with jc 7137"

    def handle(self, *args, **kwargs):
        self.stdout.write("creating resonses for event 9998")
        with open(response_fp, "r") as f:
            responses = json.load(f)

        creator = GameCreator(responses)
        self.stdout.write("creating game")
        creator.create_game()
        self.stdout.write("creating event")
        creator.create_event()
        self.stdout.write("creating questions")
        creator.create_question_data()
        self.stdout.write("creating responses")
        creator.create_responses()
        self.stdout.write("done")
