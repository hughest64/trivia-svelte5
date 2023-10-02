from datetime import date
import logging

from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string

from user.models import User
from user.authentication import create_token

logger = logging.getLogger(__name__)

SITE_LINK = settings.EMAIL_REDIRECT_HOST


class Mailer:
    template = "email/notify.html"
    password_reset_text = "email/password_reset_email.txt"

    def __init__(self, user: User):
        self.user = user
        self.reset_token = None
        # cannot be added to the init, but can be set manually after initilization
        self.expires_in = 600  # in seconds

    def send_password_reset(self):
        if not self.user.email:
            logger.warning(f"no email registered for {self.user}")
            return
        subject = "Reset your Trivia Mafia Password"
        reset_link = self.get_reset_link()

        send_mail(
            subject,
            render_to_string(
                self.password_reset_text,
                {"usernname": self.user.username, "password_reset_link": reset_link},
            ),
            settings.DEFAULT_FROM_EMAIL,
            [self.user.email],
            html_message=self.configure_password_email(
                subject=subject, password_reset_link=reset_link
            ),
        )

    def set_reset_token(self):
        self.reset_token = create_token(self.user, expires_in=self.expires_in)

    def get_reset_link(self):
        if self.reset_token is None:
            self.set_reset_token()

        return f"{SITE_LINK}/user/reset/{self.reset_token}"

    def configure_password_email(self, subject, password_reset_link):
        return render_to_string(
            self.template,
            {
                "email_aria_label": subject,
                "header_link": SITE_LINK,
                "title": subject,
                "title_link": password_reset_link,
                "subheading": "Please click the link below to reset the password on your account:",
                "cta_text": "Reset your Password",
                "cta_link": password_reset_link,
                "disclaimer": "If you didn't request a password reset, just ignore this email. This link will expire soon!",
                "hero_image_link": SITE_LINK,
                "hero_image_alt": "Play Trivia With Us Tonight",
                "footer_text": f"Copyright {date.today():%Y}, Trivia Mafia",
            },
        )
