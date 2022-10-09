import logging
import random

from django.http.response import HttpResponse
from django.shortcuts import render
from django.views import View
from googletrans import Translator
from utils.messages import HtmxMessage
from word_lists.models import WordsList
from word_lists.views import user_subscribed_lists

from .models import Dictionary, Languages, Synonyms

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


def word_synonyms(dictionary_id):
    return Synonyms.objects.filter(dictionary_id=dictionary_id).all()


def next_word(request):
    languages = Languages.objects.all()
    context = {"languages": languages}
    user = request.user

    if user.is_authenticated:
        user_language = user.language
        context["destination_language"] = user_language

    selected_words_list_id = request.POST.get("selected_words_list_id")
    context["selected_words_list_id"] = selected_words_list_id

    selected_words_list_name = request.POST.get("selected_words_list_name")
    context["selected_words_list_name"] = selected_words_list_name

    if selected_words_list_name == "default_words_list":
        word = give_random_word_from_words_list()

    else:
        words_list = WordsList.objects.filter(pk=selected_words_list_id)[0]
        if words_list.words == []:
            context["languages"] = None
            context["destination_language"] = None

            message = f"{words_list.name} words list is empty"
            logger.error(message)

            response = render(request, "partials/word_and_translate.html", context)

            response[HtmxMessage.HEADER] = HtmxMessage.error(message=message)

            return response
        word = give_random_word_from_words_list(words_list.words)

    context["word"] = word
    context["synonyms"] = word_synonyms(word["id"])
    logger.info("Word: " + word.get("word"))
    return render(request, "partials/word_and_translate.html", context)


def translate_word(request):
    languages = Languages.objects.all()
    context = {"languages": languages}
    htmx_message = None

    selected_words_list_name = request.POST.get("selected_words_list_name")
    context["selected_words_list_name"] = selected_words_list_name

    selected_words_list_id = request.POST.get("selected_words_list_id")
    context["selected_words_list_id"] = selected_words_list_id

    word_id = request.POST.get("word_id")
    destination_language = request.POST.get("destination_language")
    translated_data = None

    if word_id == "":
        context["languages"] = None

    try:
        word = Dictionary.objects.get(id=word_id)
        context["word"] = word

        translated_data = replace_translate_result(word.word, destination_language)
        context["translated_data"] = translated_data
        context["synonyms"] = word_synonyms(word.id)

        if destination_language is None:
            return render(request, "partials/word_and_translate.html", context)

        logger.info(
            "Language: {}\nWord: {}".format(
                destination_language, translated_data.get("word")
            )
        )
    except Exception:
        htmx_message = HtmxMessage.error(message="Not Found")
        logger.info(
            "Language: {}\nWord: {}".format(destination_language, translated_data)
        )

    context["destination_language"] = destination_language

    response = render(request, "partials/word_and_translate.html", context)
    response[HtmxMessage.HEADER] = htmx_message
    return response


class Index(View):
    def get(self, request):
        context = list_of_words_list(request)
        context["selected_words_list_name"] = "default_words_list"

        return render(request, "index.html", context)

    def post(self, request):
        context = list_of_words_list(request)
        button_name = request.POST.get("button")

        if button_name == "choose_words_list":

            words_list_id = request.POST.get("words_list_id")
            context["selected_words_list_id"] = words_list_id

            words_list_name = request.POST.get("words_list_name")
            context["selected_words_list_name"] = words_list_name

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
    all_words_list = {"default_words_lists": WordsList.objects.filter(is_private=False)}

    if request.user.is_authenticated:
        all_words_list["user_words_list"] = WordsList.objects.filter(user=request.user)
        all_words_list["user_subscribed_list"] = user_subscribed_lists(request)

    return all_words_list


def page_not_found_view(request, exception):
    return render(request, "404.html", status=404)


def clear_messages(request):
    return HttpResponse("")
