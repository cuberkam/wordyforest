from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout
from django.shortcuts import redirect, render
from main_page.models import Languages

from .forms import ChangeEmailForm, ChangePasswordForm


def setting_view(request):
    change_email_form = ChangeEmailForm(request.POST or None)
    change_password_form = ChangePasswordForm(request.POST or None)
    user = request.user
    languages = Languages.objects.all()

    context = {
        "change_email_form": change_email_form,
        "change_password_form": change_password_form,
        "current_email": user.email,
        "languages": languages,
    }

    if user.language is not None:
        context["destination_language"] = user.language

    if request.method == "POST":
        button_name = request.POST.get("button")

        if button_name == "select_language":
            destination_language = request.POST.get("destination_language")

            if destination_language is None:
                context["destination_language"] = None
            else:
                context["destination_language"] = destination_language
                get_user_model().objects.filter(id=user.id).update(
                    language=destination_language
                )

        if button_name == "change_email":
            if change_email_form.is_valid():
                email = change_email_form.cleaned_data.get("email")
                get_user_model().objects.filter(id=user.id).update(email=email)

                context["current_email"] = email
                context["change_email_form"] = ChangeEmailForm(None)
                user.email = email

                messages.success(request, "The email address was successfully changed.")

            else:
                form_errors = change_email_form.non_field_errors().as_text().strip("*")
                messages.error(request, form_errors)

        if button_name == "change_password":
            if change_password_form.is_valid():
                current_password = change_password_form.cleaned_data.get(
                    "current_password"
                )
                password = change_password_form.cleaned_data.get("password")

                is_password = user.check_password(current_password)
                if is_password is False:
                    messages.error(
                        request, "The current password you have provided is incorrect"
                    )
                else:
                    current_user = get_user_model().objects.get(id=user.id)
                    current_user.set_password(password)
                    current_user.save()
                    login(request, current_user)
                    messages.success(request, "The password was successfully changed.")

        if button_name == "delete_account":
            current_user = get_user_model().objects.get(id=user.id)
            logout(request)
            current_user.delete()
            messages.success(request, "The account was successfully deleted.")
            return redirect("index")

    return render(request, "settings.html", context=context)
