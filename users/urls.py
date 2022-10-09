from django.urls import path

from . import views

urlpatterns = [
    path("login/", views.login_user, name="login"),
    path("register/", views.register, name="register"),
    path("logout/", views.logout_user, name="logout"),
    path("forgot_password/", views.forgot_password, name="forgot_password"),
    path("reset_password/<pk>/", views.reset_password, name="reset_password"),
]
