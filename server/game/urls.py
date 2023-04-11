from django.urls import path, re_path
from django.shortcuts import redirect

from .views import common, game, host, team

app_name = "game"


def redirect_to_admin(_):
    return redirect("/admin/")


urlpatterns = [
    # nothing at the root, go to the admin
    path("", redirect_to_admin, name="redirect_to_admin"),
    # host endpoints
    re_path(r"^host/(?P<joincode>\d+)/lock/?$", host.RoundLockView.as_view()),
    re_path(
        r"^host/(?P<joincode>\d+)/score(/(?P<round_number>\d+))?/?$",
        host.ScoreRoundView.as_view(),
        name="score_round",
    ),
    re_path(
        r"^host/(?P<joincode>\d+)/updatelb/?$",
        host.UpdatePublicLeaderboardView.as_view(),
    ),
    re_path(
        r"^host/(?P<joincode>\d+)/revealanswers/?$",
        host.RevealAnswersView.as_view(),
    ),
    re_path(r"^host/(?P<joincode>\d+)/reveal/?$", host.QuestionRevealView.as_view()),
    re_path(r"^host/event-setup/?$", host.EventSetupView.as_view()),
    re_path(r"^host/(?P<joincode>\d+)[/\w]*/?$", host.EventHostView.as_view()),
    # player endpoints
    re_path(r"^game/join/?$", game.EventJoinView.as_view()),
    re_path(r"^game/(?P<joincode>\d+)/response/?$", game.ResponseView.as_view()),
    re_path(r"^game/(?P<joincode>\d+)[/\w]*/?$", game.EventView.as_view()),
    re_path(r"^team/join/?$", team.TeamJoinView.as_view()),
    re_path(r"^team/select/?$", team.TeamSelectView.as_view()),
    re_path(r"^team/create/?$", team.TeamCreateView.as_view()),
    re_path(r"^team/?$", team.TeamView.as_view()),
    # for testing only!
    re_path(r"^reset-event-data/?$", common.ClearEventDataView.as_view()),
]
