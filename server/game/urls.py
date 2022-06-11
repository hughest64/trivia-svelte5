from django.urls import path
from . import views


urlpatterns = [
    path("userteams/", views.UserTeamsView.as_view()),
    path("eventsetup/", views.EventSetupView.as_view()),
    path("event/", views.EventView.as_view()),
    path("teamselect/", views.TeamSelectView.as_view())
]