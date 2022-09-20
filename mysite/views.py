from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages


def signup(request):
    """Register a new user."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.error(request, "Create account success! Please login!!!")
            return redirect("login")
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})