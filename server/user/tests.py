from django.test import TestCase

from rest_framework.test import APIClient

from user.models import User


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
        username = response.data.get("user_data").get("username")
        self.assertTrue(username.startswith("_guest"))

        response = self.client.post("/user/create", data={"guest_user": True})
        username2 = response.data.get("user_data").get("username")
        self.assertIsNotNone(username2)
        self.assertEqual(username2, username)

    # TODO once implemented
    def test_password_reset(self):
        pass
