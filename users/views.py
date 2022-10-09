import logging

from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils import timezone
from utils.send_mail import send_mail_reset_password

from users.models import ResetPassword

from . import forms
from .models import CustomUser

logger = logging.getLogger(__name__)


def login_user(request):
    form = forms.LoginForm(request.POST or None)

    context = {"form": form}

    if form.is_valid():
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")

        user = authenticate(email=email, password=password)

        if user is None:
            messages.error(request, "Wrong email or password")
            return render(request, "login.html", context)

        if form.cleaned_data.get("rememberme"):
            request.session.set_expiry(1209600)  # 2 Weeks

        login(request, user)
        return redirect("index")

    return render(request, "login.html", context)


def register(request):
    form = forms.RegisterForm(request.POST or None)

    if form.is_valid():
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")

        new_user = CustomUser(email=email)
        new_user.set_password(password)

        new_user.save()
        login(request, new_user)

        return redirect("index")

    elif form.errors != {}:
        form_errors = form.non_field_errors().as_text()
        messages.error(request, form_errors)
    context = {"form": form}
    return render(request, "register.html", context)


@login_required
def logout_user(request):
    logout(request)
    return redirect("index")


def forgot_password(request):
    form = forms.ForgotPassword(request.POST or None)

    if form.is_valid():
        email = form.cleaned_data.get("email")

        user = get_user_model().objects.filter(email=email)
        if user.exists():
            user_id = user.values()[0]["id"]
            reset_password_instance = ResetPassword.objects.create(user_id=user_id)

            send_mail_reset_password(email, reset_password_instance.url_id)

        messages.success(request, "Email sent")

    context = {"form": form}
    return render(request, "forgot_password.html", context)


def reset_password(request, pk):
    form = forms.ResetPassword(request.POST or None)
    reset_password_instance = ResetPassword.objects.filter(url_id=pk)

    if reset_password_instance.exists():
        expire_date = reset_password_instance.values()[0]["expire_date"]

        if expire_date >= timezone.now():

            if form.is_valid():
                user_id = reset_password_instance.values()[0]["user_id"]
                user = get_user_model().objects.get(pk=user_id)

                password = form.cleaned_data.get("password")

                user.set_password(password)
                user.save()
                login(request, user)
                messages.success(request, "Your password was successfully reset.")

                reset_password_instance.delete()

                return redirect("index")

            elif form.errors != {}:
                form_errors = form.non_field_errors().as_text()
                messages.error(request, form_errors)
                logger.error(form_errors)

            context = {"form": form}
            return render(request, "reset_password.html", context)

        reset_password_instance.delete()

    messages.error(request, "This link has expired or has been used.")
    return redirect("index")
