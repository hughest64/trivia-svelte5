from django.urls import path
from . import views


urlpatterns = [
    path("userteams/", views.UserTeamsView.as_view()),
    path("eventdata/", views.EventSelectView.as_view()),
]