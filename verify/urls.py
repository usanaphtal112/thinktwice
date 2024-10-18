from django.urls import path
from .views import (
    PropertyVerificationView,
    PropertyVerificationListView,
    PropertyVerificationCreateView,
    PropertyVerificationDetailView,
    OfficeListView,
    OfficeCreateView,
    OfficeDetailView,
    OfficeDeleteView,
    PropertyTypeListView,
    PropertyTypeCreateView,
    PropertyTypeDetailView,
    PropertyTypeDeleteView,
)

urlpatterns = [
    path(
        "verify/<str:token>/",
        PropertyVerificationView.as_view(),
        name="verify_property",
    ),
    path(
        "my-verifications/",
        PropertyVerificationListView.as_view(),
        name="my_verifications",
    ),
    path(
        "create-verification/",
        PropertyVerificationCreateView.as_view(),
        name="create_verification",
    ),
    path(
        "verification/<int:pk>/",
        PropertyVerificationDetailView.as_view(),
        name="verification_detail",
    ),
    # Office URLs
    path("offices/", OfficeListView.as_view(), name="office_list"),
    path("offices/create/", OfficeCreateView.as_view(), name="office_create"),
    path("offices/<int:pk>/", OfficeDetailView.as_view(), name="office_detail"),
    path("offices/<int:pk>/delete/", OfficeDeleteView.as_view(), name="office_delete"),
    # Property Type URLs
    path("property-types/", PropertyTypeListView.as_view(), name="property_type_list"),
    path(
        "property-types/create/",
        PropertyTypeCreateView.as_view(),
        name="property_type_create",
    ),
    path(
        "property-types/<int:pk>/",
        PropertyTypeDetailView.as_view(),
        name="property_type_detail",
    ),
    path(
        "property-types/<int:pk>/delete/",
        PropertyTypeDeleteView.as_view(),
        name="property_type_delete",
    ),
]
