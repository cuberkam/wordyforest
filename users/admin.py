from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = (
        "username",
        "email",
        "date_joined",
        "last_login",
        "is_admin",
        "is_staff",
    )
    search_fields = (
        "username",
        "email",
    )
    readonly_fields = ("id", "date_joined", "last_login")
    ordering = (
        "username",
        "email",
    )

    filter_horizontal = ()
    list_filter = ()
    fieldsets = (
        (
            "Fields",
            {
                "fields": (
                    "id",
                    "username",
                    "email",
                    "password",
                    "date_joined",
                    "last_login",
                    "is_admin",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )


admin.site.register(CustomUser, CustomUserAdmin)
