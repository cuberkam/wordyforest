import uuid

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import QueryDict
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods
from main_page.models import Dictionary
from utils.messages import HtmxMessage

from .models import SubscribedList, WordsList


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

    context = {
        "user_word_list": user_word_list,
        "user_subscribed_lists": user_subscribed_lists(request),
    }
    return render(request, "my_lists.html", context)


@login_required
def words_list_details(request, pk):
    return render(request, "words_list_details.html", words_list_with_list_of_words(pk))


def words_list_with_list_of_words(pk):
    words_list = WordsList.objects.filter(pk=pk)
    list_of_words = Dictionary.objects.filter(pk__in=words_list.get().words)

    context = {
        "words_list": words_list.get(),
        "list_of_words": list_of_words,
    }
    return context


@login_required
def change_list_name(request, pk):
    htmx_message = None

    if request.method == "PUT":
        put_data = QueryDict(request.body).dict()
        try:
            WordsList.objects.filter(pk=pk).update(name=put_data["new_list_name"])
        except IntegrityError:
            htmx_message = HtmxMessage.error(message="This list name already exist.")

    words_list = get_object_or_404(WordsList, pk=pk)

    context = {"words_list": words_list}

    response = render(request, "partials/list_name.html", context)
    response[HtmxMessage.HEADER] = htmx_message
    return response


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
    )

    context = {
        "results": results,
        "words_list_id": words_list_id,
    }
    return render(request, "partials/search_results.html", context)


@login_required
def add_words(request, pk, word_pk):
    list_of_words_in_words_list = []
    htmx_message = None

    words_list = WordsList.objects.filter(pk=pk)
    word = Dictionary.objects.filter(pk=word_pk)

    if words_list.exists() and word.exists():
        list_of_words_in_words_list = words_list.get().words

        if int(word_pk) in list_of_words_in_words_list:
            htmx_message = HtmxMessage.error(
                message="The word has already been added to the list."
            )
        else:
            list_of_words_in_words_list.append(int(word_pk))
            words_list.update(words=list_of_words_in_words_list)
            htmx_message = HtmxMessage.success(
                message="The word has been successfully added to the list."
            )

    list_of_words = Dictionary.objects.filter(pk__in=list_of_words_in_words_list).all()
    context = {
        "words_list": words_list.get(),
        "list_of_words": list_of_words,
    }

    response = render(request, "partials/list_of_words.html", context)
    response[HtmxMessage.HEADER] = htmx_message
    return response


@login_required
@require_http_methods(["DELETE"])
def delete_list(request, pk):
    words_list = WordsList.objects.filter(pk=pk, user=request.user)

    if words_list.exists():
        sub_list = SubscribedList.objects.filter(words_list_id=pk).all()
        if sub_list.exists():
            for item in sub_list:
                item.delete()

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


@login_required
def subscribe_list(request):
    post_data = QueryDict(request.body).dict()
    share_code = post_data["share_code"].split()[0]
    htmx_message = None
    context = {"user_subscribed_lists": user_subscribed_lists(request)}

    try:
        uuid.UUID(share_code)
    except ValueError:
        htmx_message = HtmxMessage.error(message="This is an invalid key.")
        response = render(request, "partials/subscribed_lists_list.html", context)
        response[HtmxMessage.HEADER] = htmx_message
        return response

    words_list_queryset = WordsList.objects.filter(share_id=share_code, is_private=True)

    if words_list_queryset.filter(user=request.user):
        htmx_message = HtmxMessage.error(
            message="You are unable to subscribe to your lists."
        )
        response = render(request, "partials/subscribed_lists_list.html", context)
        response[HtmxMessage.HEADER] = htmx_message
        return response

    if not words_list_queryset.exists():
        htmx_message = HtmxMessage.error(message="Such a list does not exist.")
        response = render(request, "partials/subscribed_lists_list.html", context)
        response[HtmxMessage.HEADER] = htmx_message
        return response

    for item in words_list_queryset:
        words_list = item

    try:
        SubscribedList.objects.create(user=request.user, words_list=words_list)
    except IntegrityError:
        htmx_message = HtmxMessage.error(
            message="You cannot resubscribe to the list you subscribed to."
        )

    context = {"user_subscribed_lists": user_subscribed_lists(request)}

    response = render(request, "partials/subscribed_lists_list.html", context)
    response[HtmxMessage.HEADER] = htmx_message
    return response


@login_required
def user_subscribed_lists(request):
    subscribed_list_ids = SubscribedList.objects.filter(user=request.user).values_list(
        "words_list_id", flat=True
    )
    return WordsList.objects.filter(pk__in=subscribed_list_ids)


@login_required
def unsubscribe_list(request, pk):
    htmx_message = None
    subscribed_list = SubscribedList.objects.filter(user=request.user, words_list_id=pk)

    if subscribed_list.exists():
        subscribed_list.delete()
        htmx_message = HtmxMessage.success(
            message="You has been successfully unsubscribe."
        )

    context = {"user_subscribed_lists": user_subscribed_lists(request)}

    response = render(request, "partials/subscribed_lists_list.html", context)
    response[HtmxMessage.HEADER] = htmx_message
    return response


@login_required
def subscribed_list_details(request, pk):
    return render(
        request,
        "subscribed_list_details.html",
        words_list_with_list_of_words(pk),
    )
