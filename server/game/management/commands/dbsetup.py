# dbsetup.py
"""
Create a custom staff user, guest user, and associated teams.
For use when running the demo app.
"""
import getpass
import json

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db.models import Q

from game.models import Team

User = get_user_model()


class Command(BaseCommand):
    help = "Create users and teams for the demo app."

    def handle(self, *args, **kwargs):
        try:
            user = None
            create_user = input("Create a Superuser? [y/n]: ")

            if create_user.lower().startswith("y"):
                username, email = self.get_username()
                password = self.get_password()

                user = User(username=username, email=email, is_staff=True, is_superuser=True)
                user.set_password(password)
                user.save()

            # get or create guest user
            guest_user, guest_user_created = User.objects.get_or_create(
                username="guest"
            )
            if guest_user_created:
                guest_user.set_password("guest")
                guest_user.save()

            # create a staff user for testing
            sample_admin, sample_admin_created = User.objects.get_or_create(
                username="sample_admin"
            )
            if sample_admin_created:
                sample_admin.set_password("sample_admin")
                sample_admin.is_staff = True
                sample_admin.save()

            with open(settings.BASE_DIR.parent / "data" / "teams.json", "r") as f:
                teams = json.load(f)

            created_teams = [Team.objects.get_or_create(**team)[0] for team in teams]

            for team in created_teams:
                if team.name == "guest":
                    team.members.add(guest_user.id)

                elif user is not None:
                    team.members.add(user.id)

            self.stdout.write("Successfully created data")

        except KeyboardInterrupt:
            self.stdout.write("\nCancelled database setup")

        except Exception as e:
            self.stdout.write(e)

    def get_username(self, prompt=None):
        """Ask a user for a username and email address and return it unless the user already exists.
        In that case, call the method recursively.
        """
        username = input(prompt or "Username: ")
        email = input("Email Address (Enter to skip): ")

        if email:
            user = User.objects.filter(Q(username=username) | Q(email=email))
        else:
            user = User.objects.filter(username=username)

        if user.exists():
            return self.get_username(
                prompt="A user with that username or email already exists, please try again: "
            )

        return username, email

    def get_password(self, prompt=None):
        """Ask a user for a password, then again to validate. If the two do not match,
        recursively call this method with an updated prompt
        """
        pass1 = getpass.getpass(prompt or "Password: ")
        pass2 = getpass.getpass("Password (again): ")

        if pass1 != pass2:
            return self.get_password(
                prompt="Oops! Your passwords didn't match, please re-enter:\n# "
            )

        return pass1
