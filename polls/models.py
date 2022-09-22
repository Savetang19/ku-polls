"""This module includes the Question and Choice models for the Polls app."""
import datetime
from django.db import models
from django.utils import timezone
from django.contrib import admin
from django.contrib.auth.models import User


class Question(models.Model):
    """Model for create poll questions."""

    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")
    end_date = models.DateTimeField("end date", null=True, blank=True)

    @admin.display(
        boolean=True,
        ordering="pub_date",
        description="Published recently?",
    )
    def __str__(self):
        """String representation for question."""
        return self.question_text

    def was_published_recently(self):
        """Return true if the question was published within the last day.
        Otherwise, return false.
        """
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def is_published(self):
        """Return true if the question was published.
        Otherwise return false.
        """
        now = timezone.now()
        return now >= self.pub_date

    def can_vote(self):
        """Return true if the current time falls between the publication date
        and the end date. Otherwise, return false.
        """
        now = timezone.now()
        if not self.end_date:
            return self.pub_date <= now
        return self.pub_date <= now <= self.end_date


class Choice(models.Model):
    """Model for crate question's choices."""

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)

    # votes = models.IntegerField(default=0)

    @property
    def votes(self):
        """ Count the number of votes for this choice."""
        return Vote.objects.filter(choice=self).count()

    def __str__(self):
        """String representation for choice."""
        return self.choice_text


class Vote(models.Model):
    """Model for collect contains vote the user to whom it belongs and
    the choice on which the user is voting.
    """
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)

    def __str__(self):
        """String representation for vote."""
        return f"{self.user.username} votes for {self.choice.choice_text}"
