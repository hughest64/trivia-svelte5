from django.contrib import admin

from .models import *

admin.site.register(Team)
admin.site.register(Question)
admin.site.register(QuestionAnswer)
admin.site.register(GameQuestion)
admin.site.register(TiebreakerQuestion)
admin.site.register(GameRound)
admin.site.register(Game)
admin.site.register(TriviaEvent)
admin.site.register(EventQuestionState)
admin.site.register(EventRoundState)
admin.site.register(Location)
admin.site.register(QuestionResponse)
admin.site.register(Leaderboard)
admin.site.register(LeaderboardEntry)
