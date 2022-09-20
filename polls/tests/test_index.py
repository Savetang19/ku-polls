"""This module contain tests for index views"""
import datetime
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from polls.models import Question


def create_question(question_text, days, end=None):
    """Create a question with the given text and published day offset to now"""
    time = timezone.now() + datetime.timedelta(days=days)
    if end is not None:
        end_time = timezone.now() + datetime.timedelta(days=end)
        return Question.objects.create(question_text=question_text,
                                       pub_date=time, end_date=end_time)
    return Question.objects.create(question_text=question_text, pub_date=time)


class IndexViewTests(TestCase):
    """The test class for test index view."""
    def test_no_question(self):
        """An message is displayed, if no question exist."""
        response = self.client.get(reverse("polls:index"))
        self.assertIs(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])

    def test_past_question(self):
        """Questions with a pub_date in the past are displayed on the
        index page.
        """
        question = create_question(question_text="Past question", days=-30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["latest_question_list"],
                                 [question], )

    def test_future_question(self):
        """Questions with a pub_date in the future are not displayed on the
        index page.
        """
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        """Even if both past and future questions exist, only past questions
        are displayed.
        """
        question = create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'],
                                 [question], )

    def test_two_past_questions(self):
        """The questions index page may display multiple questions."""
        question1 = create_question(question_text="Past question 1.", days=-30)
        question2 = create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'],
                                 [question2, question1], )
