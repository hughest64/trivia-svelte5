from django.urls import path, re_path
from . import views

app_name = "user"

urlpatterns = [
    path("", views.UserView.as_view()),
    re_path(r"login/?$", views.LoginView.as_view(), name="login"),
    re_path(r"logout/?$", views.LogoutView.as_view(), name="logout"),
    re_path(r"guest/?$", views.GuestView.as_view(), name="guest"),
]
