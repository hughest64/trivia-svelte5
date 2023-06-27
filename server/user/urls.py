from django.urls import path, re_path
from . import views, oauth_views

app_name = "user"

urlpatterns = [
    path("", views.UserView.as_view()),
    re_path(r"create/?$", views.CreateView.as_view(), name="create"),
    re_path(r"reset/?$", views.ResetPasswordView.as_view(), name="reset"),
    re_path(r"refresh/?$", views.RefreshTokenView.as_view(), name="refresh"),
    re_path(r"forgot/?$", views.ForgotPasswordView.as_view(), name="forgot"),
    re_path(r"login/?$", views.LoginView.as_view(), name="login"),
    re_path(r"logout/?$", views.LogoutView.as_view(), name="logout"),
    re_path(r"google-login/?$", oauth_views.google_login, name="google_login"),
    re_path(r"google-auth/?$", oauth_views.google_auth, name="google_auth"),
]
