from django.core.management.base import BaseCommand

from game.processors import TeamQr

class Command(BaseCommand):
    def handle(self, *args, **options):
        svg = TeamQr('my-cool-team')
        string = svg.create()
        print(string)