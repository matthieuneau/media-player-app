from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from django.contrib.auth.models import User


def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )
            return redirect("login")  # TODO: Implement login page later
    else:
        form = UserRegistrationForm()
    return render(request, "accounts/register.html", {"form": form})
