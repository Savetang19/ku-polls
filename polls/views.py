"""This module contains polls app views."""
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages
from .models import Question, Choice, Vote
from django.contrib.auth.decorators import login_required


class IndexView(generic.ListView):
    """View for index page which displays the most recent 5 questions."""

    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last 5 published questions (not include future published
        question(s)).
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    """View for each question."""

    model = Question
    template_name = "polls/detail.html"

    def get_queryset(self):
        """Exclude any question that are not published yet."""
        return Question.objects.filter(pub_date__lte=timezone.now())

    def get(self, request, *args, **kwargs):
        """Handel the Get request for the detail view."""
        try:
            question = get_object_or_404(Question, pk=kwargs["pk"])
        except Http404:
            messages.error(request, f"Poll number {kwargs['pk']} does not exists.")
            return redirect("polls:index")
        
        try:
            vote = Vote.objects.get(user=request.user, choice__in=question.choice_set.all())
            previous_vote = vote.choice.choice_text
        except (Vote.DoesNotExist, TypeError):
            previous_vote = ""

        if question.can_vote():
            return render(request, self.template_name, {"question": question, "previous_vote":previous_vote})
        else:
            messages.error(request, f"Poll number {question.id} is not available to vote")
            return redirect("polls:index")
    



class ResultsView(generic.DetailView):
    """View for each question's result."""

    model = Question
    template_name = "polls/results.html"

    def get(self, request, *args, **kwargs):
        """Handel the Get request for the results view."""
        try:
            question = get_object_or_404(Question, pk=kwargs["pk"])
        except Http404:
            messages.error(request,
                           f"Poll number {kwargs['pk']} does not exists.")
            return redirect("polls:index")
        
        # check if this question is already published or not.
        if question.is_published():
            return render(request, self.template_name, {"question": question})
        else:
            messages.error(request, f"Poll number {question.id} results are not available.")
            return redirect("polls:index")


@login_required
def vote(request, question_id):
    """Voting process on detail view."""
    question = get_object_or_404(Question, pk=question_id)
    user = request.user

    if not question.can_vote():
        messages.error(request, f"Poll number {question.id} is not available to vote")
        return redirect("polls:index")
    
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(request, "polls/detail.html", {
            "question": question,
            "error_message": "Please select some choice!",
        })
    else:
        try:
            vote = Vote.objects.get(user=user, choice__question=question)
            vote.choice = selected_choice
            vote.save()
        except Vote.DoesNotExist:
            Vote.objects.create(user=user, choice=selected_choice).save()
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
