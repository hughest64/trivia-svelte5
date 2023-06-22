from django.core.mail import send_mail
from django.conf import settings

from user.models import User
from user.authentication import create_token

# TODO: get from env variable via settings
SITE_LINK = "http://127.0.0.1:5173/user/reset"


class Mailer:
    def __init__(self, user: User):
        self.user = user
        self.reset_token = None
        # cannot be added to the init, but can be set manually after initilization
        self.expires_in = 600  # in seconds

    def send_password_reset(self):
        # TODO: log?
        if not self.user.email:
            return

        send_mail(
            "Reset your Trivia Mafia Password",
            "Did you request a password reset?",
            settings.DEFAULT_FROM_EMAIL,
            [self.user.email],
            html_message=f"Click <a href={self.get_reset_link()}>this link</a> to reset your password",
        )

    def set_reset_token(self):
        self.reset_token = create_token(self.user, expires_in=self.expires_in)

    def get_reset_link(self):
        if self.reset_token is None:
            self.set_reset_token()

        return f"{SITE_LINK}/{self.reset_token}"
