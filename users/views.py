from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from . import forms
from .models import CustomUser


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
