from django.contrib.auth.forms import (
    UserCreationForm as DjangoUserCreationForm,
    UserChangeForm as DjangoUserChangeForm
)
from .models import User


class UserCreationForm(DjangoUserCreationForm):
    """
    This uses Django’s built-in UserCreationForm but adapted
    to work with your custom User model (email as username).
    """
    class Meta(DjangoUserCreationForm.Meta):
        model = User
        fields = ("email", "username")  # custom fields


class UserChangeForm(DjangoUserChangeForm):
    """
    This form is used when editing a user in the admin panel.
    Django automatically handles password hashing and read-only display.
    """
    class Meta:
        model = User
        fields = ("email", "username", "password",
                  "is_active", "is_staff", "is_superuser")


# from django import forms
# from django.contrib.auth.forms import ReadOnlyPasswordHashField
# from .models import User


# class UserCreationForm(forms.ModelForm):
#     password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
#     password2 = forms.CharField(
#         label="Confirm Password", widget=forms.PasswordInput)

#     class Meta:
#         model = User
#         fields = ("email", "username")

#     def clean_password2(self):
#         p1 = self.cleaned_data.get("password1")
#         p2 = self.cleaned_data.get("password2")
#         if p1 and p2 and p1 != p2:
#             raise forms.ValidationError("Passwords do not match")
#         return p2

#     def save(self, commit=True):
#         user = super().save(commit=False)

#         # VERY IMPORTANT: HASH PASSWORD HERE
#         user.set_password(self.cleaned_data["password1"])

#         if commit:
#             user.save()
#         return user


# class UserChangeForm(forms.ModelForm):
#     password = ReadOnlyPasswordHashField()

#     class Meta:
#         model = User
#         fields = ("email", "username", "password",
#                   "is_active", "is_staff", "is_superuser")

#     def clean_password(self):
#         return self.initial["password"]
