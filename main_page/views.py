import random

from django.shortcuts import render

from .models import Dictionary


def give_random_word(queryset):
    dictionary = queryset
    dictionary_length = dictionary.count()
    random_dictionary_id = random.randint(2, dictionary_length)
    word = dictionary.filter(id=random_dictionary_id).values()[0]

    return word


def index(request):
    context = {"word_list": "all_word"}

    if request.method == "POST":
        button_name = request.POST.get("button")
        if button_name == "next":
            word_list = request.POST.get("word_list")
            word_id = request.POST.get("word_id")

            if word_list == "all_word":
                if word_id != "":
                    queryset = Dictionary.objects.all().exclude(id=word_id)
                else:
                    queryset = Dictionary.objects.all()

                word = give_random_word(queryset)
                context = {
                    "word": word,
                    "word_list": "all_word",
                }
                return render(request, "index.html", context)

    return render(request, "index.html", context)


def page_not_found_view(request, exception):
    return render(request, "404.html", status=404)
