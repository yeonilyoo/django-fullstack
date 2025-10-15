from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.utils.crypto import get_random_string

from common.forms import UserForm
from common.models import User


# Create your views here.
def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect("index")
    else:
        form = UserForm()
    return render(request, "common/signup.html", {"form": form})


def reset_with_temp_password(request):
    if request.method == "POST":
        username_or_email = request.POST.get("identifier")
        try:
            user = User.objects.get(email=username_or_email)
        except User.DoesNotExist:
            try:
                user = User.objects.get(username=username_or_email)
            except User.DoesNotExist:
                return render(request, "common/login.html")

        temp_password = get_random_string(length=10)
        user.password = make_password(temp_password)
        user.save()

        send_mail(
            subject="Your Temporary Password",
            message=f"Your temporary password is: {temp_password}",
            from_email="noreply@example.com",
            recipient_list=[user.email],
        )

        return render(request, "common/login.html")
    return render(request, "common/login.html")
