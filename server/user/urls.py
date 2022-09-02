from django.urls import path, re_path
from . import views


urlpatterns = [
    path("", views.UserView.as_view()),
    re_path(r"login/?$", views.LoginView.as_view()),
    re_path(r"logout/?$", views.LogoutView.as_view()),
    re_path(r"guest/?$", views.GuestView.as_view()),
    re_path(r"validate/?$", views.ValidateView.as_view()),
]