from django.urls import path, re_path
from . import views


urlpatterns = [
    # host endpoints
    re_path(r"^host/event-setup/?$", views.EventSetupView.as_view()),
    re_path(r"^host/(?P<joincode>\d+)[/\w]*/?$", views.EventHostView.as_view()),

    # player endpoints
    re_path(r"^game/join/?$", views.EventJoinView.as_view()),
    # TODO: consider the [/\w]* group a temp workaround for a frontend issue (I think)
    re_path(r"^game/(?P<joincode>\d+)[/\w]*/?$", views.EventView.as_view()),
    re_path(r"^teamselect/?$", views.TeamView.as_view()),
    re_path(r"^team/?$", views.TeamView.as_view()),
]