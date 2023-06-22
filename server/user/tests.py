import time

from django.test import TestCase

from rest_framework.test import APIClient

from user.models import User
from user.utils import Mailer, SITE_LINK


class UserViewsTestCase(TestCase):
    def setUp(self):
        self.existing_user = User.objects.create_user(
            username="p1", email="p1@no.no", password="12345"
        )
        self.client = APIClient()

    def tearDown(self) -> None:
        User.objects.all().delete()

    def test_create_user(self):
        user_data = {
            "username": "p1",
            "email": "p1@no.no",
            "pass": "12345",
            "pass2": "12346",
        }
        # post w/ a username that already exists
        response = self.client.post("/user/create", data=user_data)
        self.assertEqual(response.status_code, 400)

        # update the username, but the passwords don't match
        user_data.update({"username": "p2"})
        response = self.client.post("/user/create", data=user_data)
        self.assertEqual(response.status_code, 400)

        # update the passwords, but the email already exists
        user_data.update({"pass2": "12345"})
        response = self.client.post("/user/create", data=user_data)
        self.assertEqual(response.status_code, 400)

        # update the email and create the user
        user_data.update({"email": "p2@no.no"})
        response = self.client.post("/user/create", data=user_data)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.data.get("user_data"))
        self.assertIsNotNone(response.cookies.get("jwt"))

    def test_login(self):
        # bad password
        response = self.client.post(
            "/user/login", data={"username": "p1", "password": "12356"}
        )
        self.assertEqual(response.status_code, 403)

        # bad username
        response = self.client.post(
            "/user/login", data={"username": "p5", "password": "12345"}
        )
        self.assertEqual(response.status_code, 403)

        # success
        response = self.client.post(
            "/user/login", data={"username": "p1", "password": "12345"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.data.get("user_data"))
        self.assertIsNotNone(response.cookies.get("jwt"))

    def test_play_as_guest(self):
        response = self.client.post("/user/create", data={"guest_user": True})
        self.assertEqual(response.status_code, 200)
        self.assertTrue("jwt" in response.cookies)
        username = response.data.get("user_data", {}).get("username")
        self.assertTrue(username.startswith("_guest"))

        response = self.client.post("/user/create", data={"guest_user": True})
        username2 = response.data.get("user_data", {}).get("username")
        self.assertIsNotNone(username2)
        self.assertEqual(username2, username)

    def test_password_reset(self):
        # invoke the Mailer class directly to get the reset token and link (since we aren't getting an email)
        user = User.objects.create_user(
            username="reset_player", password="test_pass_one"
        )
        # expect the link to be the correct format (but don't post since it goes to the frontend app)
        mailer = Mailer(user)
        link = mailer.get_reset_link()
        token = mailer.reset_token

        # token and reset link are valid
        self.assertTrue(link.startswith(SITE_LINK))
        self.assertTrue(link.endswith(token))

        # post without a reset token
        post_data = {"pass1": "new_pass", "pass2": "new_pass"}
        response = self.client.post("/user/reset", post_data)
        self.assertEqual(response.status_code, 403)

        # post with mismatched passwords
        post_data.update({"token": token, "pass2": "not matched"})
        response = self.client.post("/user/reset", post_data)
        self.assertEqual(response.status_code, 403)

        # post with good data
        post_data.update({"pass2": "new_pass"})
        response = self.client.post("/user/reset", post_data)
        self.assertEqual(response.status_code, 200)

        # log in with new passwords
        response = self.client.post(
            "/user/login", {"username": "reset_player", "password": "new_pass"}
        )
        self.assertEqual(response.status_code, 200)

    def test_password_reset_expired_token(self):
        user = User.objects.create_user(
            username="reset_expired", password="test_pass_one"
        )
        mailer = Mailer(user)
        mailer.expires_in = 1
        mailer.set_reset_token()

        time.sleep(1)
        post_data = {"token": mailer.reset_token, "pass1": "abcd", "pass2": "abcd"}
        response = self.client.post("/user/reset", post_data)
        self.assertEqual(response.status_code, 403)
