from django.urls import reverse_lazy
from django.views.generic import FormView
from django.core import signing
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, DetailView, DeleteView
from .models import OfficeVerification, PropertyVerification, Office, PropertyType
from .forms import (
    RequestVerificationForm,
    PropertyVerificationForm,
    OfficeForm,
    PropertyTypeForm,
)
from .tasks import send_verification_email


class PropertyVerificationView(FormView):
    template_name = "verification/property_verification_form.html"
    form_class = PropertyVerificationForm
    success_url = (
        "/verification-success/"  # Or wherever you want to redirect after submission
    )

    def get_object(self):
        # Use token to fetch the verification office instance
        return get_object_or_404(
            OfficeVerification, verification_token=self.kwargs["token"]
        )

    def form_valid(self, form):
        pvo = self.get_object()
        # Process the form and update the verification status for this office
        pvo.status = form.cleaned_data["status"]
        pvo.verifier_name = form.cleaned_data["verifier_name"]
        pvo.verification_message = form.cleaned_data["verification_message"]
        pvo.save()
        return super().form_valid(form)


class PropertyVerificationListView(LoginRequiredMixin, ListView):
    model = PropertyVerification
    template_name = "property_verification/my_verifications.html"
    context_object_name = "verifications"

    def get_queryset(self):
        return PropertyVerification.objects.filter(user=self.request.user)


class PropertyVerificationCreateView(LoginRequiredMixin, CreateView):
    model = PropertyVerification
    form_class = RequestVerificationForm
    template_name = "property_verification/create_verification.html"
    success_url = reverse_lazy("my_verifications")

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)

        # Get the newly created PropertyVerification object
        property_verification = form.instance

        # Create OfficeVerification objects for each office involved
        offices = Office.objects.filter(
            property_types=property_verification.property_type
        )
        print("OFFICES: ", offices)
        for office in offices:
            office_verification = OfficeVerification.objects.create(
                office=office, property_verification=property_verification
            )

            # Trigger the Celery task to send the email to each office
            send_verification_email.delay(office_verification.id)

        return response


class PropertyVerificationDetailView(LoginRequiredMixin, DetailView):
    model = PropertyVerification
    template_name = "property_verification/verification_detail.html"
    context_object_name = "verification"

    def get_queryset(self):
        return PropertyVerification.objects.filter(user=self.request.user)


class OfficeListView(LoginRequiredMixin, ListView):
    model = Office
    template_name = "office/office_list.html"
    context_object_name = "offices"


class OfficeCreateView(LoginRequiredMixin, CreateView):
    model = Office
    form_class = OfficeForm
    template_name = "office/office_form.html"
    success_url = reverse_lazy("office_list")


class OfficeDetailView(LoginRequiredMixin, DetailView):
    model = Office
    template_name = "office/office_detail.html"
    context_object_name = "office"


class OfficeDeleteView(LoginRequiredMixin, DeleteView):
    model = Office
    template_name = "office/office_confirm_delete.html"
    success_url = reverse_lazy("office_list")


class PropertyTypeListView(LoginRequiredMixin, ListView):
    model = PropertyType
    template_name = "property_type/property_type_list.html"
    context_object_name = "property_types"


class PropertyTypeCreateView(LoginRequiredMixin, CreateView):
    model = PropertyType
    form_class = PropertyTypeForm
    template_name = "property_type/property_type_form.html"
    success_url = reverse_lazy("property_type_list")

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.offices.set(form.cleaned_data["offices"])
        return response


class PropertyTypeDetailView(LoginRequiredMixin, DetailView):
    model = PropertyType
    template_name = "property_type/property_type_detail.html"
    context_object_name = "property_type"


class PropertyTypeDeleteView(LoginRequiredMixin, DeleteView):
    model = PropertyType
    template_name = "property_type/property_type_confirm_delete.html"
    success_url = reverse_lazy("property_type_list")
