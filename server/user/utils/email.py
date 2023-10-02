from datetime import date
import logging

from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string

from game.models import Team
from user.models import User
from user.authentication import create_token

logger = logging.getLogger(__name__)

SITE_LINK = settings.EMAIL_REDIRECT_HOST


class Mailer:
    template = "email/notify.html"
    password_reset_text = "email/password_reset_email.txt"
    team_welcome_text = "email/team_welcome_email.txt"

    def __init__(self, user: User, team: Team = None):
        self.user = user
        self.team = team
        self.reset_token = None
        # cannot be added to the init, but can be set manually after initilization
        self.expires_in = 600  # in seconds

    def send_team_welcome(self):
        if not self.user.email:
            logger.warning(f"no email registered for {self.user}")
            return

        subject = f"Trivia Mafia welcomes you to Team {self.team.name}"

        send_mail(
            subject,
            render_to_string(
                self.team_welcome_text,
                {
                    "username": self.user.username,
                    "team_name": self.team.name,
                    "password": self.team.password,
                },
            ),
            settings.DEFAULT_FROM_EMAIL,
            [self.user.email],
            html_message=self.configure_team_welome_email(subject),
        )

    def configure_team_welome_email(self, subject):
        subheading = f"Bring your friends, {self.user.username}! Forward them this email and use the button below to join, or tell them your three-word join code:"

        return render_to_string(
            self.template,
            {
                "email_aria_label": subject,
                "header_link": SITE_LINK,
                "title": f"Team {self.team.name} is ready to play!",
                "title_link": SITE_LINK,
                "subheading": subheading,
                "cta_text": self.team.password,
                "cta_link": SITE_LINK,
                "hero_image_link": SITE_LINK,
                "hero_image_alt": "Play Trivia With Us Tonight",
                "footer_text": f"Copyright {date.today():%Y}, Trivia Mafia",
            },
        )

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
