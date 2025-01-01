import requests
import os
import dotenv
import json
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt

from .forms import UserRegistrationForm

dotenv.load_dotenv()


def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )
            return redirect("login")
    else:
        form = UserRegistrationForm()
    return render(request, "accounts/register.html", {"form": form})


@login_required
def welcome(request):
    return render(request, "accounts/welcome.html", {"username": request.user.username})


@csrf_exempt
def facebook_login(request):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed. Use POST"}, status=405)

    data = json.loads(request.body)

    access_token = data.get("accessToken")
    user_id = data.get("userID")

    app_id = os.getenv("app-id")
    app_secret = os.getenv("app-secret")
    debug_token_url = f"https://graph.facebook.com/debug_token?input_token={access_token}&access_token={app_id}|{app_secret}"

    response = requests.get(debug_token_url).json()

    if (
        response.get("data", {}).get("is_valid")
        and response["data"]["user_id"] == user_id
    ):
        # Fetch user details from fb
        user_info_url = f"https://graph.facebook.com/v16.0/me?fields=id,name,email&access_token={access_token}"
        user_info = requests.get(user_info_url).json()

        user, created = User.objects.get_or_create(
            username=user_info["id"],
            defaults={
                "email": user_info.get(
                    "email", ""
                ),  # Email may not always be available
                "first_name": user_info.get("name", "").split()[0]
                if user_info.get("name")
                else "",
                "last_name": " ".join(user_info.get("name", "").split()[1:])
                if user_info.get("name")
                else "",
            },
        )

        login(request, user)
        return JsonResponse({"success": True})
    else:
        return JsonResponse({"success": False})


if __name__ == "__main__":
    app_id = os.getenv("app-id")
    print(app_id)
