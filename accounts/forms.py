from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ("email", "first_name", "middle_name", "last_name")


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ("email", "first_name", "middle_name", "last_name", "role")


class ProfileForm(forms.ModelForm):

    class Meta:
        model = CustomUser
        fields = ["first_name", "middle_name", "last_name", "profile_image"]
