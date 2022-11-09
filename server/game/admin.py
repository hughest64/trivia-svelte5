from django.contrib import admin

from .models import *

admin.site.register(Team)
admin.site.register(Question)
admin.site.register(GameQuestion)
admin.site.register(GameRound)
admin.site.register(Game)
admin.site.register(TriviaEvent)
admin.site.register(EventQuestionState)
admin.site.register(EventRoundState)
