from django.urls import path

from . import views

urlpatterns = [
    path("", views.Index.as_view(), name="index"),
]

htmx_urlpatterns = [
    path("next-word/", views.next_word, name="next_word"),
    path("translate-word/", views.translate_word, name="translate_word"),
]

urlpatterns += htmx_urlpatterns
