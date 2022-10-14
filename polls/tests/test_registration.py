"""This module contain tests for registration pages."""
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class RegistrationTest(TestCase):
    """The test class for tests registration."""

    def setUp(self):
        """Create user for login."""
        # initialize new user
        self.user_1 = User.objects.create_user(
            username="testregis",
            password="hellotest123"
        )
        self.user_1.save()

    def test_login_page(self):
        """The visitor can login and can enter polls index from login page."""
        login = reverse("login")
        # get the login page
        response = self.client.get(login)
        self.assertEqual(response.status_code, 200)

        # login
        form_data = {"username": "testregis", "password": "hellotest123"}
        response2 = self.client.post(login, form_data)
        self.assertEqual(response2.status_code, 302)
        self.assertRedirects(response2, reverse("polls:index"))

    def test_signup_page(self):
        """The visitor can signup and when he/she already create an account,
        redirect him/her to login page again."""
        signup = reverse("signup")
        response = self.client.get(signup)
        self.assertEqual(response.status_code, 200)

        form_data = {"username": "new_acc", "password1": "newacc1452",
                     "password2": "newacc1452"}
        response2 = self.client.post(signup, form_data)
        self.assertEqual(response2.status_code, 200)
