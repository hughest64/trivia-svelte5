from django.core.mail import send_mail
from django.conf import settings

from user.models import User
from user.authentication import create_token

SITE_LINK = "http://127.0.0.1:5173/user/reset"


class Mailer:
    def __init__(self):
        pass

    def send_password_reset(self, user: User, expires_in=None):
        if not user.email:
            # TODO: log?
            return

        if expires_in is None:
            expires_in = 600

        reset_token = create_token(user, expires_in=expires_in)
        reset_link = f"{SITE_LINK}/{reset_token}"

        send_mail(
            "Reset your Trivia Mafia Password",
            "Did you request a password reset?",
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            html_message=f"Click <a href={reset_link}>this link</a> to reset your password",
        )
