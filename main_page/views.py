import random

from django.shortcuts import render
from googletrans import Translator

from .models import Dictionary, Languages


def give_random_word(queryset):
    dictionary = queryset
    dictionary_length = dictionary.count()
    random_dictionary_id = random.randint(2, dictionary_length)
    word = dictionary.filter(id=random_dictionary_id).values()[0]

    return word


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
    context = {"word_list": "all_word", "translated_data": ""}
    user = request.user
    if user.is_authenticated:
        user_language = user.language

    if request.method == "POST":
        context["languages"] = languages
        button_name = request.POST.get("button")
        word_list = request.POST.get("word_list")
        word_id = request.POST.get("word_id")
        if button_name == "next":
            if user.is_authenticated and user_language is not None:
                context["destination_language"] = user_language

            if word_list == "all_word":
                if word_id != "":
                    queryset = Dictionary.objects.all().exclude(id=word_id)
                else:
                    queryset = Dictionary.objects.all()

                word = give_random_word(queryset)
                context["word"] = word
                return render(request, "index.html", context)
        if button_name == "translate":
            destination_language = request.POST.get("destination_language")
            try:
                word = Dictionary.objects.get(id=word_id)
            except Exception:
                word = ""
            context["word"] = word
            if destination_language is None:
                return render(request, "index.html", context)

            translated_data = replace_translate_result(word.word, destination_language)

            context["translated_data"] = translated_data
            context["destination_language"] = destination_language

            return render(request, "index.html", context)

    return render(request, "index.html", context)


def page_not_found_view(request, exception):
    return render(request, "404.html", status=404)
