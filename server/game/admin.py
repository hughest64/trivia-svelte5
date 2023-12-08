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
    list_filter = ["leaderboard_type"]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ["__str__", "question_type"]
    list_filter = ["question_type"]


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ("name", "password")


admin.site.register(Leaderboard)
admin.site.register(Location)
admin.site.register(QuestionAnswer)
admin.site.register(QuestionResponse)
admin.site.register(TeamNote)
admin.site.register(TiebreakerResponse)
admin.site.register(TriviaEvent)
