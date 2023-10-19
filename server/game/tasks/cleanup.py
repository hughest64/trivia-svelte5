"""
celery cli:

celery -A server worker -l INFO -P solo --without-gossip --without-mingle
celery -A server beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler
"""

from datetime import timedelta

from celery import shared_task

from django.contrib.sessions.models import Session
from django.core import management
from django.utils import timezone

from game.models import *
from user.models import User


@shared_task
def anonymize_join_codes(days=30):
    management.call_command("db_cleanup", job="joincodes", days=30)


@shared_task
def purge_anonymous_users(days=7):
    start_date = timezone.now() - timedelta(days=7)
    anonymous_users = User.objects.filter(created_at__lte=start_date, is_guest=True)
    user_count = anonymous_users.count()

    if user_count < 1:
        return {
            "results": f"No active anonymous users found created before {start_date:%Y-%m-%d}"
        }
    anonymous_users.delete()

    return {
        "results": f"deleted {user_count} anonymous user(s) created before {start_date:%Y-%m-%d}"
    }


@shared_task
def purge_empty_leaderboard_entries(days=7):
    management.call_command("db_cleanup", job="leaderboard", days=7)


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
