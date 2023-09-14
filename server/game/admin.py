from django.contrib import admin

from .models import *


class ChatAdmin(admin.ModelAdmin):
    list_display = ["__str__", "team", "event"]


class LeaderboardEntryAdmin(admin.ModelAdmin):
    list_filter = ["leaderboard_type"]


class QuestionAdmin(admin.ModelAdmin):
    list_display = ["__str__", "question_type"]
    list_filter = ["question_type"]


class GameAdmin(admin.ModelAdmin):
    search_fields = ("block_code",)
    list_display = ("title", "active_through")
    list_filter = ("block_code", "use_sound")


admin.site.register(ChatMessage, ChatAdmin)
admin.site.register(Team)
admin.site.register(Question, QuestionAdmin)
admin.site.register(QuestionAnswer)
admin.site.register(GameQuestion)
admin.site.register(TeamNote)
admin.site.register(GameRound)
admin.site.register(Game, GameAdmin)
admin.site.register(TriviaEvent)
admin.site.register(TiebreakerResponse)
admin.site.register(EventQuestionState)
admin.site.register(EventRoundState)
admin.site.register(Location)
admin.site.register(QuestionResponse)
admin.site.register(Leaderboard)
admin.site.register(LeaderboardEntry, LeaderboardEntryAdmin)
