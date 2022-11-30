from django.urls import path, re_path
from django.shortcuts import redirect

from .views import common, host, player

def redirect_to_admin(_):
    return redirect('/admin/')


urlpatterns = [
    # nothing at the root, go to the admin
    path('', redirect_to_admin, name="redirect_to_admin"),

    # update trivia events
    re_path(r"^host/(?P<joincode>\d+)/lock/?$", host.RoundLockView.as_view()),
    re_path(r"^host/(?P<joincode>\d+)/reveal/?$", host.QuestionRevealView.as_view()),
    re_path(r"^host/(?P<joincode>\d+)/update-all/?$", host.UpdateAllView.as_view()),
    re_path(r"^host/(?P<joincode>\d+)/update/?$", host.UpdateView.as_view()),

    # host endpoints
    re_path(r"^host/event-setup/?$", host.EventSetupView.as_view()),
    re_path(r"^host/(?P<joincode>\d+)[/\w]*/?$", host.EventHostView.as_view()),

    # player endpoints
    re_path(r"^game/join/?$", player.EventJoinView.as_view()),
    re_path(r"^game/(?P<joincode>\d+)/response/?$", player.ResponseView.as_view()),
    re_path(r"^game/(?P<joincode>\d+)[/\w]*/?$", player.EventView.as_view()),
    re_path(r"^teamselect/?$", player.TeamView.as_view()),
    re_path(r"^team/?$", player.TeamView.as_view()),

    # for testing only!
    re_path(r"^reset-event-data/?$", common.ClearEventDataView.as_view()),
]