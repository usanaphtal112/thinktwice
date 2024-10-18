from django.contrib import admin
from .models import Office, PropertyType, PropertyVerification, OfficeVerification


@admin.register(Office)
class OfficeAdmin(admin.ModelAdmin):
    list_display = ("name", "email")
    search_fields = ("name", "email")


@admin.register(PropertyType)
class PropertyTypeAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(PropertyVerification)
class PropertyVerificationAdmin(admin.ModelAdmin):
    list_display = ("user", "property_type", "created_at", "overall_status")
    list_filter = ("property_type",)
    search_fields = ("user__email", "property_type__name", "id_passport")


@admin.register(OfficeVerification)
class OfficeVerificationAdmin(admin.ModelAdmin):
    list_display = (
        "property_verification",
        "office",
        "status",
        "verifier_name",
        "created_at",
    )
    list_filter = ("status", "office")
    search_fields = ("verifier_name", "property_verification__user__email")
