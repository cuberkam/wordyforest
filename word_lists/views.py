from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import QueryDict
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods
from main_page.models import Dictionary

from .models import WordsList


@login_required
def my_lists(request):
    user_word_list = WordsList.objects.filter(user=request.user).all()

    if request.method == "POST":
        button_name = request.POST.get("button")

        if button_name == "create_list":
            list_name = request.POST.get("list_name")

            try:
                created_list = WordsList.objects.create(
                    name=list_name, user=request.user
                )
                return redirect("words_list_details", pk=created_list.id)
            except IntegrityError:
                messages.error(request, "This list name already exist.")

    context = {"user_word_list": user_word_list}
    return render(request, "my_lists.html", context)


@login_required
def words_list_details(request, pk):
    words_list = WordsList.objects.filter(pk=pk)
    list_of_words = Dictionary.objects.filter(pk__in=words_list.get().words)

    context = {
        "words_list": words_list.get(),
        "list_of_words": list_of_words,
    }
    return render(request, "words_list_details.html", context)


@login_required
def change_list_name(request, pk):
    if request.method == "PUT":
        put_data = QueryDict(request.body).dict()
        WordsList.objects.filter(pk=pk).update(name=put_data["new_list_name"])

    words_list = get_object_or_404(WordsList, pk=pk)

    context = {"words_list": words_list}
    return render(request, "partials/list_name.html", context)


@login_required
def change_list_name_form(request, pk):
    words_list = get_object_or_404(WordsList, pk=pk)

    context = {"words_list": words_list}
    return render(request, "partials/change_list_name_form.html", context)


@login_required
@require_http_methods(["DELETE"])
def delete_word_from_words_list(request, pk, word_pk):
    words_list = WordsList.objects.filter(pk=pk)

    list_of_words_in_words_list = words_list.get().words
    list_of_words_in_words_list.remove(int(word_pk))

    words_list.update(words=list_of_words_in_words_list)

    list_of_words = Dictionary.objects.filter(pk__in=list_of_words_in_words_list).all()

    context = {
        "words_list": words_list.get(),
        "list_of_words": list_of_words,
    }
    return render(request, "partials/list_of_words.html", context)


@login_required
def search_words(request):
    search_text = request.POST.get("search")
    words_list_id = request.POST.get("words_list_id")
    user_words_list_words = (
        WordsList.objects.filter(pk=words_list_id, user=request.user).first().words
    )

    if search_text == "":
        return HttpResponse("")

    results = Dictionary.objects.filter(word__icontains=search_text).exclude(
        pk__in=user_words_list_words
    )[:10]

    context = {
        "results": results,
        "words_list_id": words_list_id,
    }
    return render(request, "partials/search_results.html", context)


@login_required
def add_words(request, pk, word_pk):
    list_of_words_in_words_list = []

    words_list = WordsList.objects.filter(pk=pk)
    word = Dictionary.objects.filter(pk=word_pk)

    if words_list.exists() and word.exists():
        list_of_words_in_words_list = words_list.get().words

        if int(word_pk) in list_of_words_in_words_list:
            messages.error(request, "The word has already been added to the list.")
        else:
            list_of_words_in_words_list.append(int(word_pk))
            words_list.update(words=list_of_words_in_words_list)
            messages.success(
                request, "The word has been successfully added to the list."
            )

    list_of_words = Dictionary.objects.filter(pk__in=list_of_words_in_words_list).all()
    context = {
        "words_list": words_list.get(),
        "list_of_words": list_of_words,
    }
    return render(request, "partials/list_of_words.html", context)


@login_required
@require_http_methods(["DELETE"])
def delete_list(request, pk):
    words_list = WordsList.objects.filter(pk=pk, user=request.user)

    if words_list.exists():
        words_list.delete()

        user_words_list = WordsList.objects.filter(user=request.user)
        context = {
            "user_word_list": user_words_list,
        }

    return render(request, "partials/words_list_list.html", context)


@login_required
def toggle_words_list_status(request, pk):
    is_private = request.POST.get("private")
    if is_private == "True":
        WordsList.objects.filter(pk=pk, user=request.user).update(is_private=False)
    else:
        WordsList.objects.filter(pk=pk, user=request.user).update(is_private=True)
    return HttpResponse("")
