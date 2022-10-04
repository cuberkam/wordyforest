import logging
import random

from django.contrib import messages
from django.http.response import HttpResponse
from django.shortcuts import render
from googletrans import Translator
from word_lists.models import WordsList
from word_lists.views import user_subscribed_lists

from .models import Dictionary, Languages

logger = logging.getLogger(__name__)


def replace_translate_result(word, dest):
    translator = Translator()
    replaced_result = {"translate": []}
    word_with_synonyms = ""

    try:
        translate_result = translator.translate(word, dest=dest)
        all_translations = translate_result.extra_data["all-translations"]
        possible_translations = translate_result.extra_data["possible-translations"][0][
            2
        ]
        replaced_result["word"] = translate_result.text

        if all_translations is None:
            for data in possible_translations:
                word_with_synonyms = (
                    word_with_synonyms + f"<li><strong>{data[0]}</strong></li>"
                )
            replaced_result["translate"].append(
                {
                    "type": "",
                    "words": word_with_synonyms,
                }
            )
            return replaced_result
        if all_translations is None and possible_translations is None:
            return None

        for item in all_translations:
            for data in item[2]:
                word_with_synonyms = (
                    word_with_synonyms + f"<li><strong>{data[0]}</strong>: "
                )
                for i in data[1]:
                    word_with_synonyms = word_with_synonyms + f"{i}, "

                word_with_synonyms = word_with_synonyms[:-2] + "</li>"

            replaced_result["translate"].append(
                {
                    "type": item[0],
                    "words": word_with_synonyms,
                }
            )
        return replaced_result

    except Exception:
        return None


def index(request):
    languages = Languages.objects.all()
    context = {
        "selected_words_list_name": "default_words_list",
        "list_of_words_list": list_of_words_list(request),
        "translated_data": "",
    }
    user = request.user
    if user.is_authenticated:
        user_language = user.language

    if request.method == "POST":
        context["languages"] = languages
        button_name = request.POST.get("button")

        selected_words_list_name = request.POST.get("selected_words_list_name")
        context["selected_words_list_name"] = selected_words_list_name

        selected_words_list_id = request.POST.get("selected_words_list_id")
        context["selected_words_list_id"] = selected_words_list_id

        word_id = request.POST.get("word_id")

        if button_name == "choose_words_list":
            context["languages"] = None

            words_list_id = request.POST.get("words_list_id")
            context["selected_words_list_id"] = words_list_id

            words_list_name = request.POST.get("words_list_name")
            context["selected_words_list_name"] = words_list_name

        if button_name == "next":
            if user.is_authenticated and user_language is not None:
                context["destination_language"] = user_language

            if selected_words_list_name == "default_words_list":
                word = give_random_word_from_words_list()

            else:
                words_list = WordsList.objects.filter(pk=selected_words_list_id)[0]
                if words_list.words == []:
                    messages.error(request, f"{words_list.name} words list is empty")
                    logger.error(f"{words_list.name} words list is empty")
                    return render(request, "index.html", context)
                word = give_random_word_from_words_list(words_list.words)

            context["word"] = word
            logger.info("Word: " + word.get("word"))
            return render(request, "index.html", context)

        if button_name == "translate":
            destination_language = request.POST.get("destination_language")
            translated_data = None
            try:
                word = Dictionary.objects.get(id=word_id)

                translated_data = replace_translate_result(
                    word.word, destination_language
                )
                context["translated_data"] = translated_data

                if destination_language is None:
                    return render(request, "index.html", context)

                logger.info(
                    "Language: {}\nWord: {}".format(
                        destination_language, translated_data.get("word")
                    )
                )
            except Exception:
                logger.info(
                    "Language: {}\nWord: {}".format(
                        destination_language, translated_data
                    )
                )
            context["word"] = word

            context["destination_language"] = destination_language

            return render(request, "index.html", context)

    return render(request, "index.html", context)


def give_random_word_from_words_list(ids_list=None):

    if ids_list is None:
        dictionary = Dictionary.objects.all()
        dictionary_length = dictionary.count()
        random_dictionary_id = random.SystemRandom().randint(2, dictionary_length)

    else:
        dictionary = Dictionary.objects.filter(pk__in=ids_list)
        random_dictionary_id = random.SystemRandom().choice(ids_list)

    word = dictionary.filter(id=random_dictionary_id).values()[0]

    return word


def list_of_words_list(request):
    all_words_list = WordsList.objects.filter(is_private=False)

    if request.user.is_authenticated:
        user_words_list = WordsList.objects.filter(user=request.user)
        user_subscribed_list = user_subscribed_lists(request)
        all_words_list = all_words_list | user_words_list | user_subscribed_list

    return all_words_list


def page_not_found_view(request, exception):
    return render(request, "404.html", status=404)


def clear_messages(request):
    return HttpResponse("")
