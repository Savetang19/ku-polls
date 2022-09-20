from urllib import request
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class RegiatrationTest(TestCase):
    def setUp(self):
        # initailize new user
        self.user_1 = User.objects.create_user(
            username="testregis",
            password="hellotest123"
        )
        self.user_1.save()

    def test_login_page(self):
        login = reverse("login")
        response = self.client.get(login)
        self.assertEqual(response.status_code, 200)

        form_data = {"username": "testregis", "password": "hellotest123"}
        response2 = self.client.post(login, form_data)
        self.assertEqual(response2.status_code, 302)
        self.assertRedirects(response2, reverse("polls:index"))
    
    def test_signup_page(self):
        signup = reverse("signup")
        response = self.client.get(signup)
        self.assertEqual(response.status_code, 200)

        form_data = {"username": "new_acc", "password1": "newacc1452", "password2":  "newacc1452"}
        response2 = self.client.post(signup, form_data)
        self.assertEqual(response2.status_code, 302)
        self.assertRedirects(response2, reverse("login"))
