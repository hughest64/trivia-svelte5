from django.contrib import admin

from .models import *


@admin.register(ChangeLog)
class ChangeLogAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at")


@admin.register(ChatMessage)
class ChatAdmin(admin.ModelAdmin):
    list_display = ["__str__", "team", "event"]


@admin.register(EventQuestionState)
class EventQuestionStateAdmin(admin.ModelAdmin):
    search_fields = ["event__game__title", "event__location__name"]


@admin.register(EventRoundState)
class EventRoundStateAdmin(admin.ModelAdmin):
    search_fields = ["event__game__title", "event__location__name"]


@admin.register(GameQuestion)
class GameQuestionAdmin(admin.ModelAdmin):
    search_fields = ["game__title"]


@admin.register(GameRound)
class GameRoundAdmin(admin.ModelAdmin):
    search_fields = ["game__title"]


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    search_fields = ("block_code",)
    list_display = ("title", "active_through")
    list_filter = ("block_code", "use_sound")


@admin.register(LeaderboardEntry)
class LeaderboardEntryAdmin(admin.ModelAdmin):
    search_fields = ["event__game__title", "team__name"]
    list_filter = ["leaderboard_type"]
    list_display = ["team", "event", "total_points", "rank", "leaderboard_type"]
    exclude = ["leaderboard", "event"]


# no real reason to display this in the admin
# admin.site.register(Leaderboard)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    search_fields = ["name", "address"]
    list_filter = ["active", "use_sound"]
    list_display = ["name", "address", "active", "use_sound"]


@admin.register(QuestionAnswer)
class QuestionAnserAdmin(admin.ModelAdmin):
    search_fields = ["text"]


@admin.register(QuestionResponse)
class QuestionResponseAdmin(admin.ModelAdmin):
    search_fields = [
        "recorded_answer",
        "event__game__title",
        "game_question__question__question_text",
    ]
    list_display = ["event", "team"]
    exclude = ["game_question", "event", "team"]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ["__str__", "question_type"]
    list_filter = ["question_type"]


# not currently used in the app
# admin.site.register(TeamNote)


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    search_fields = ["name", "password"]
    list_display = ["name", "password"]
    exclude = ["members"]


@admin.register(TiebreakerResponse)
class TiebreakerResponseAdmin(admin.ModelAdmin):
    search_fields = [
        "recorded_answer",
        "event__game__title",
        "game_question__question__question_text",
    ]
    list_display = ["event", "team"]
    exclude = ["game_question", "event", "team"]


admin.site.register(TriviaEvent)
