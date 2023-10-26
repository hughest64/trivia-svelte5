"""
celery cli:

celery -A server worker -l INFO -P solo --without-gossip --without-mingle
celery -A server beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler
"""

from celery import shared_task

from django.contrib.sessions.models import Session
from django.core import management

from game.models import *


@shared_task
def anonymize_join_codes(days=30):
    management.call_command("db_cleanup", job="joincodes", days=days)


@shared_task
def purge_anonymous_users(days=7):
    management.call_command("db_cleanup", job="users", days=days)


@shared_task
def purge_empty_leaderboard_entries(days=7):
    management.call_command("db_cleanup", job="leaderboard", days=days)


# @shared_task
def purge_empty_games():
    pass


@shared_task
def purge_expired_sessions():
    all_sessions = Session.objects.all().count()
    management.call_command("clearsessions")
    remaining_sessions = Session.objects.all().count()

    return {
        "results": f"Deleted {all_sessions - remaining_sessions} expired of {all_sessions} total sessions."
    }
