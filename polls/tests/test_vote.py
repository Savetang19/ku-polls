"""This module contain tests for voting."""
import datetime
from django.test import TestCase
from django.utils import timezone
from polls.models import Choice, Question
from django.urls import reverse
from django.contrib.auth.models import User


def create_question(question_text, days, end=None):
    """Create a question with the given text and published day offset to now"""
    time = timezone.now() + datetime.timedelta(days=days)
    if end is not None:
        end_time = timezone.now() + datetime.timedelta(days=end)
        return Question.objects.create(question_text=question_text,
                                       pub_date=time, end_date=end_time)
    return Question.objects.create(question_text=question_text, pub_date=time)


class VotesTest(TestCase):
    def setUp(self):
        """Create questions and a user, then login."""
        # initialize new questions
        self.recent_question = create_question("Random select1", 0)
        self.past_question = create_question("Random select2", -10, -5)
        self.future_question = create_question("Random select3", 20)

        # initialize new user
        self.user_1 = User.objects.create_user(
            username="testvote",
            password="hellotest123"
        )
        self.user_1.save()

        # login
        form_data = {'username': "testvote", 'password': "hellotest123"}
        self.client.post(reverse("login"), form_data)

    def test_vote_on_recent_question(self):
        """Vote should count correctly if the question is on voting period."""
        # create new choices for recent question
        choice_1 = self.recent_question.choice_set.create(choice_text='1')
        choice_2 = self.recent_question.choice_set.create(choice_text='2')

        # vote on choice 2
        response = self.client.post(reverse('polls:vote', kwargs={
            'question_id': self.recent_question.id}), {'choice': choice_2.id})

        choice_1 = Choice.objects.get(id=choice_1.id)
        choice_2 = Choice.objects.get(id=choice_2.id)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(0, choice_1.votes)
        self.assertEqual(1, choice_2.votes)

    def test_vote_on_past_question(self):
        """If voting period is end, the polls is not longer accepting vote."""
        # create new choices for past(ended) question
        choice_1 = self.past_question.choice_set.create(choice_text='3')
        choice_2 = self.past_question.choice_set.create(choice_text='4')

        # vote on choice 2
        response = self.client.post(reverse('polls:vote', kwargs={
            'question_id': self.past_question.id}), {'choice': choice_2.id})

        choice_1 = Choice.objects.get(id=choice_1.id)
        choice_2 = Choice.objects.get(id=choice_2.id)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(0, choice_1.votes)
        self.assertEqual(0, choice_2.votes)

    def test_vote_on_future_question(self):
        """The user can not vote if the polls question is not published yet."""
        # create new choices for future question
        choice_1 = self.future_question.choice_set.create(choice_text='5')
        choice_2 = self.future_question.choice_set.create(choice_text='6')

        # vote on choice 2
        response = self.client.post(reverse('polls:vote', kwargs={
            'question_id': self.future_question.id}), {'choice': choice_2.id})

        choice_1 = Choice.objects.get(id=choice_1.id)
        choice_2 = Choice.objects.get(id=choice_2.id)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(0, choice_1.votes)
        self.assertEqual(0, choice_2.votes)

    def test_no_choice_selected(self):
        """If user did not selected any choice, error message will show up."""
        self.recent_question.choice_set.create(choice_text='7')
        response = self.client.post(reverse('polls:vote', kwargs={
            'question_id': self.recent_question.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Please select some choice!")

    def test_not_login_vote(self):
        """If user did not login yet, after hitting vote button it should
        redirect to login page and the redirect to polls details again."""
        self.client.post(reverse("logout"))

        # create new choices for recent question
        choice_1 = self.recent_question.choice_set.create(choice_text='8')

        # vote on choice 1
        response = self.client.post(reverse('polls:vote', kwargs={
            'question_id': self.recent_question.id}), {'choice': choice_1.id})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/accounts/login/?next=/polls/1/vote/")
