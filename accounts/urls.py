from django.urls import path, include
from .views import facebook_login, register, welcome
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path("register/", register, name="register"),
    path(
        "login/", LoginView.as_view(template_name="accounts/login.html"), name="login"
    ),
    path("welcome/", welcome, name="welcome"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("", include("allauth.urls")),
    path("facebook-login/", facebook_login, name="facebook_login"),
]
