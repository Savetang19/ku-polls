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
        return Question.objects.create(question_text=question_text, pub_date=time, end_date=end_time)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        """Returns False for questions whose pub_date is in the future."""
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """Return False for question whose pub_date is older than 1 day."""
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """Returns True for questions whose pub_date is within the last day."""
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59,
                                                   seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

    def test_is_published_with_past_question(self):
        """If question already published, `is_published` return true."""
        question = create_question("", -4)
        self.assertIs(question.is_published(), True)

    def test_is_published_with_future_question(self):
        """If question is unpublished, `is_published` return false."""
        question = create_question("", 4)
        self.assertIs(question.is_published(), False)

    def test_can_vote_on_voting_period(self):
        """If question is on voting period, `can_vote` return true."""
        # poll with end date.
        question = create_question("", 0, 10)
        self.assertIs(question.can_vote(), True)

        # poll with out end date.
        question = create_question("", 0)
        self.assertIs(question.can_vote(), True)

    def test_can_not_vote_after_end_date(self):
        """After question's end date, `can_vote` return false."""
        question = create_question("", -10, -1)
        self.assertIs(question.can_vote(), False)

    def test_can_not_vote_on_unpublished_poll(self):
        """If question is unpublished, `can_vote` return false."""
        question = create_question("", 2)
        self.assertIs(question.can_vote(), False)
