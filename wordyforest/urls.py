"""wordyforest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import handler404
from django.contrib import admin
from django.urls import include, path
from main_page.views import clear_messages

handler404 = "main_page.views.page_not_found_view"

urlpatterns = [
    path("admin/", admin.site.urls, name="admin"),
    path("", include("main_page.urls")),
    path("auth/", include("users.urls")),
    path("settings/", include("settings.urls")),
    path("word_lists/", include("word_lists.urls")),
    path("clear_messages/", clear_messages, name="clear_messages"),
]
