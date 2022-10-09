from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, UserCreationForm


class LoginForm(forms.Form):
    email = forms.CharField(
        max_length=100,
        min_length=4,
        label="Email",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Email"}),
    )
    password = forms.CharField(
        max_length=16,
        min_length=8,
        label="Password",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Password"}
        ),
    )
    rememberme = forms.BooleanField(
        label="Remember Me",
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
    )


class RegisterForm(forms.Form):
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Email"}
        ),
    )
    password = forms.CharField(
        max_length=16,
        min_length=8,
        label="Password",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Password"}
        ),
    )
    password2 = forms.CharField(
        max_length=16,
        min_length=8,
        label="Password Check",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Password Check"}
        ),
    )

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")

        if password and password2 and password != password2:
            raise forms.ValidationError("Passwords do not match")

        is_user = get_user_model().objects.filter(email=email)

        if is_user.exists():
            raise forms.ValidationError("This email already in use")

        values = {"email": email, "password": password}
        return values


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ("username", "email")


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ("username", "email")


class ForgotPassword(forms.Form):
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Email"}
        ),
    )

    def clean(self):
        email = self.cleaned_data.get("email")

        values = {"email": email}
        return values


class ResetPassword(forms.Form):
    password = forms.CharField(
        max_length=16,
        min_length=8,
        label="Password",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Password"}
        ),
    )
    password2 = forms.CharField(
        max_length=16,
        min_length=8,
        label="Password Check",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Password Check"}
        ),
    )

    def clean(self):
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")

        if password and password2 and password != password2:
            raise forms.ValidationError("Passwords do not match")

        values = {"password": password}
        return values
