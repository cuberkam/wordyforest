from django.urls import path

from . import views

urlpatterns = [
    path("my-lists/", views.my_lists, name="my_lists"),
    path("my-lists/<pk>/", views.words_list_details, name="words_list_details"),
]

htmx_urlpatterns = [
    path("my-lists/<pk>/list-name/", views.change_list_name, name="list_name"),
    path(
        "my-lists/<pk>/change-name",
        views.change_list_name_form,
        name="change_list_name",
    ),
    path(
        "my-lists/<pk>/delete-word/<word_pk>/",
        views.delete_word_from_words_list,
        name="delete_word",
    ),
    path(
        "search-words/",
        views.search_words,
        name="search_words",
    ),
    path(
        "my-lists/<pk>/add-words/<word_pk>/",
        views.add_words,
        name="add_words",
    ),
    path(
        "delete-list/<pk>/",
        views.delete_list,
        name="delete_list",
    ),
    path(
        "my-lists/<pk>/toggle-words-list-status/",
        views.toggle_words_list_status,
        name="toggle_words_list_status",
    ),
    path(
        "subscribe-list/",
        views.subscribe_list,
        name="subscribe_list",
    ),
    path(
        "subscribe-list/<pk>/",
        views.subscribed_list_details,
        name="subscribed_list_details",
    ),
    path(
        "unsubscribe-list/<pk>/",
        views.unsubscribe_list,
        name="unsubscribe_list",
    ),
]

urlpatterns += htmx_urlpatterns
