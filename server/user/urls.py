from django.urls import path, re_path
from . import views

appname = "user"

urlpatterns = [
    path("", views.index, name="index"),
    re_path(r"login/?$", views.login_user, name="login_user"),
    re_path(r"logout/?$", views.logout_user, name="logout_user"),
]