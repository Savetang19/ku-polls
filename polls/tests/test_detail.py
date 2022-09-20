"""This module contain tests for detail views."""
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


class DetailViewTests(TestCase):
    """The test class for tests detail view."""

    def test_future_question(self):
        """The detail view of a question with a pub_date in the future should
        return to index page.
        """
        future_question = create_question(question_text='Future question.',
                                          days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("polls:index"))

    def test_past_question(self):
        """The detail view of a question with a pub_date in the past displays
        the question's text.
        """
        past_question = create_question(question_text='Past Question.',
                                        days=-5)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)
