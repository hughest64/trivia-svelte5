from django.urls import path, re_path
from . import host_views, player_views, views


urlpatterns = [
    # TODO: we may not keep this, needs experimentation
    # update trivia events
    re_path(r"^host/(?P<joincode>\d+)/lock/?$", host_views.RoundLockView.as_view()),
    re_path(r"^host/(?P<joincode>\d+)/reveal/?$", host_views.QuestionRevealView.as_view()),
    re_path(r"^host/(?P<joincode>\d+)/update-all/?$", host_views.UpdateAllView.as_view()),
    re_path(r"^host/(?P<joincode>\d+)/update/?$", host_views.UpdateView.as_view()),

    # host endpoints
    re_path(r"^host/event-setup/?$", views.EventSetupView.as_view()),
    re_path(r"^host/(?P<joincode>\d+)[/\w]*/?$", views.EventHostView.as_view()),

    # player endpoints
    re_path(r"^game/join/?$", views.EventJoinView.as_view()),
    re_path(r"^game/(?P<joincode>\d+)/response/?$", player_views.ResponseView.as_view()),
    re_path(r"^game/(?P<joincode>\d+)[/\w]*/?$", views.EventView.as_view()),
    re_path(r"^teamselect/?$", views.TeamView.as_view()),
    re_path(r"^team/?$", views.TeamView.as_view()),
]