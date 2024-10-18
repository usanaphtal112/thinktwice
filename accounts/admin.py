from django.contrib import admin
from .models import CustomUser


class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "first_name",
        "last_name",
        "role",
        "is_staff",
        "is_active",
        "date_joined",
        "profile_image",
    )
    search_fields = ("email", "first_name", "last_name", "role")
    list_filter = ("role", "is_staff", "is_active")
    readonly_fields = ("date_joined",)

    fieldsets = (
        (
            "User Information",
            {"fields": ("email", "first_name", "last_name", "role", "profile_image")},
        ),
        (
            "Permissions",
            {"fields": ("is_active", "is_staff", "groups", "user_permissions")},
        ),
        ("Dates", {"fields": ("date_joined",)}),
    )


admin.site.register(CustomUser, CustomUserAdmin)
