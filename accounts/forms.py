from django import forms
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import InMemoryUploadedFile

from .models import User


class UserStoreForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "avatar",
            "password1",
            "password2"
        ]

    def __init__(self, *args, **kwargs):
        super(UserStoreForm, self).__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control px-3 py-2"


class UserForm(forms.ModelForm):
    current_password = forms.CharField(required=False, widget=forms.PasswordInput, label="Current Password")
    new_password1 = forms.CharField(required=False, widget=forms.PasswordInput, label="New Password")
    new_password2 = forms.CharField(required=False, widget=forms.PasswordInput, label="Confirm New Password")
    delete_avatar = forms.BooleanField(required=False, label="Delete Avatar")

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "avatar",
            "current_password",
            "new_password1",
            "new_password2"
        ]

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control px-3 py-2"

    def clean(self):
        cleaned_data = super().clean()
        current_password = cleaned_data.get("current_password")
        new_password1 = cleaned_data.get("new_password1")
        new_password2 = cleaned_data.get("new_password2")

        if current_password and not self.instance.check_password(current_password):
            self.add_error("current_password", "Incorrect current password")
            self.add_error("current_password", "Incorrect current password2")

        if new_password1 and new_password1 != new_password2:
            self.add_error("new_password2", "Passwords do not match")

        return cleaned_data

    def clean_avatar(self):
        avatar = self.cleaned_data.get("avatar")

        if avatar and isinstance(avatar, InMemoryUploadedFile):
            if avatar.content_type not in ["image/jpeg", "image/png"]:
                raise ValidationError("File type is not supported. Only JPG and PNG are allowed.")

            if avatar.size > 800 * 1024:  # 800K
                raise ValidationError("Max file size is 800K.")

        return avatar

    def save(self, commit=True, request=None):
        user = super().save(commit=False)

        password_changed = False
        new_password1 = self.cleaned_data.get("new_password1")

        if new_password1:
            user.set_password(new_password1)
            password_changed = True

        if self.cleaned_data.get("delete_avatar"):
            user.avatar.delete(save=False)

        if commit:
            user.save()

            if password_changed and request:
                update_session_auth_hash(request, user)

        return user
