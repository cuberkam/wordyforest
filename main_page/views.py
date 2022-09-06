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
    if request.method == "POST":
        button_name = request.POST.get("button")
        if button_name == "next":
            word_list = request.POST.get("word_list")
            word_id = request.POST.get("word_id")

            if word_list == "all_word":
                queryset = Dictionary.objects.all().exclude(id=word_id)
                word = give_random_word(queryset)
                context = {
                    "word": word,
                    "next_word_list": "all_word",
                    "prev_word_id": word_id,
                }
                return render(request, "index.html", context)

    queryset = Dictionary.objects.all()
    word = give_random_word(queryset)
    context = {"word": word, "word_list": "all_word"}
    return render(request, "index.html", context)
