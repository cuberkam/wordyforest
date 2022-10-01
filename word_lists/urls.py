from django.urls import path

from . import views

urlpatterns = [
    path("my_lists/", views.my_lists, name="my_lists"),
    path("my_lists/<pk>/", views.words_list_details, name="words_list_details"),
]

htmx_urlpatterns = [
    path("my_lists/<pk>/list_name/", views.change_list_name, name="list_name"),
    path(
        "my_lists/<pk>/change_name",
        views.change_list_name_form,
        name="change_list_name",
    ),
    path(
        "my_lists/<pk>/delete_word/<word_pk>/",
        views.delete_word_from_words_list,
        name="delete_word",
    ),
    path(
        "search_words/",
        views.search_words,
        name="search_words",
    ),
    path(
        "my_lists/<pk>/add_words/<word_pk>/",
        views.add_words,
        name="add_words",
    ),
    path(
        "delete_list/<pk>/",
        views.delete_list,
        name="delete_list",
    ),
    path(
        "my_lists/<pk>/toggle_words_list_status/",
        views.toggle_words_list_status,
        name="toggle_words_list_status",
    ),
]

urlpatterns += htmx_urlpatterns
