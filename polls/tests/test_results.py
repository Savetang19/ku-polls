"""This module contain tests for results view."""
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


class ResultsViewTests(TestCase):
    """The test class for tests result view."""

    def test_future_question_result(self):
        """If question is not published yet, It should not show result page"""
        question = create_question("Future", 3)
        url = reverse('polls:results', args=(question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
