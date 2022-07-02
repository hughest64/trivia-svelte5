from django.urls import path
from . import views


urlpatterns = [
    path("eventsetup/", views.EventSetupView.as_view()),
    path("event/<int:joincode>/", views.EventView.as_view()),
    path("host-event/<int:joincode>/", views.EventHostView.as_view()),
    path("teamselect/", views.TeamSelectView.as_view())
]