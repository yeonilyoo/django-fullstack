from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import get_jwt_after_login, is_session_valid

app_name = "common"

urlpatterns = [
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="common/login.html"),
        name="login",
    ),
    path("auth/get-token/", get_jwt_after_login, name="get_jwt_after_login"),
    path("auth/session-check", is_session_valid, name="is_session_valid"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("signup/", views.signup, name="signup"),
    path(
        "reset-temp-password/",
        views.reset_with_temp_password,
        name="reset_temp_password",
    ),
]
