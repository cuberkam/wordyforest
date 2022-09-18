from django import forms
from django.contrib.auth import get_user_model


class ChangeEmailForm(forms.Form):
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "New email"}
        ),
    )
    email2 = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "New email confirm"}
        ),
    )

    def clean(self):
        email = self.cleaned_data.get("email")
        email2 = self.cleaned_data.get("email2")

        if email and email2 and email != email2:
            raise forms.ValidationError("Emails do not match")

        is_user = get_user_model().objects.filter(email=email)

        if is_user.exists():
            raise forms.ValidationError("This email already in use")

        values = {"email": email}
        return values


class ChangePasswordForm(forms.Form):
    current_password = forms.CharField(
        max_length=16,
        min_length=8,
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                "type": "password",
                "class": "form-control",
                "placeholder": "Current password",
                "id": "InputPassword1",
            }
        ),
    )
    password = forms.CharField(
        max_length=16,
        min_length=8,
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                "type": "password",
                "class": "form-control",
                "placeholder": "Password",
                "id": "InputPassword2",
            }
        ),
    )
    password2 = forms.CharField(
        max_length=16,
        min_length=8,
        label="Password Check",
        widget=forms.PasswordInput(
            attrs={
                "type": "password",
                "class": "form-control",
                "placeholder": "Password Check",
                "id": "InputPassword3",
            }
        ),
    )

    def clean(self):
        current_password = self.cleaned_data.get("current_password")
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")

        if current_password and password and password2 and password != password2:
            raise forms.ValidationError("Passwords do not match")

        values = {"current_password": current_password, "password": password}
        return values
