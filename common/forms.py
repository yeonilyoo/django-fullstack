from django import forms
from django.contrib.auth.forms import UserCreationForm

from common.models import User


class UserForm(UserCreationForm):
    email = forms.EmailField(label="Email Address")
    phone = forms.CharField(label="phone", required=False)
    address = forms.CharField(label="address", required=False)
    nickname = forms.CharField(label="nickname", required=False)

    class Meta:
        model = User
        fields = ("username", "email", "phone", "address", "nickname")
