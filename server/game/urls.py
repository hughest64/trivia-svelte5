from django.urls import path, re_path
from django.shortcuts import redirect

from .views import game, host, team, airtable

app_name = "game"


def redirect_to_admin(_):
    return redirect("/admin/")


urlpatterns = [
    # nothing at the root, go to the admin
    path("", redirect_to_admin, name="redirect_to_admin"),
    # host endpoints
    re_path(
        r"^host/(?P<joincode>\d+)/leaderboard/responses/(?P<team_id>\d+)/?$",
        host.EventTeamResponsesView.as_view(),
        name="team_responses",
    ),
    re_path(
        r"^host/(?P<joincode>\d+)/lock/?$",
        host.RoundLockView.as_view(),
        name="round_lock",
    ),
    re_path(
        r"^host/(?P<joincode>\d+)/finishgame/?$",
        host.FinishGameview.as_view(),
        name="finish_game",
    ),
    re_path(
        r"^host/(?P<joincode>\d+)/pointsadjustment/?$",
        host.UpdateAdjustmentPointsView.as_view(),
        name="update_adjustment_points",
    ),
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
    re_path(
        r"^host/(?P<joincode>\d+)/reveal/?$",
        host.QuestionRevealView.as_view(),
        name="host",
    ),
    re_path(r"^host/event-setup/?$", host.EventSetupView.as_view(), name="event_setup"),
    re_path(
        r"^host/(?P<joincode>\d+)[/\w]*/?$",
        host.EventHostView.as_view(),
        name="host_view",
    ),
    # player endpoints
    re_path(r"^game/join/?$", game.EventJoinView.as_view(), name="event_join"),
    re_path(
        r"^game/(?P<joincode>\d+)/response/?$",
        game.ResponseView.as_view(),
        name="response",
    ),
    re_path(
        r"^game/(?P<joincode>\d+)/megaround/?$",
        game.MegaRoundView.as_view(),
        name="megaround",
    ),
    re_path(
        r"^game/(?P<joincode>\d+)[/\w]*/?$", game.EventView.as_view(), name="game_view"
    ),
    re_path(r"^team/join/?$", team.TeamJoinView.as_view(), name="team_join"),
    re_path(r"^team/select/?$", team.TeamSelectView.as_view(), name="team_select"),
    re_path(r"^team/create/?$", team.TeamCreateView.as_view(), name="team_create"),
    re_path(
        r"^team/updateteamname/?$",
        team.TeamUpdateName.as_view(),
        name="teamname_update",
    ),
    re_path(r"^team/?$", team.TeamView.as_view(), name="team"),
    re_path(r"^airtable-import/?$", airtable.airtable_import, name="airtable_import"),
]
