from django import forms
from .models import PropertyVerification, Office, PropertyType


class RequestVerificationForm(forms.ModelForm):
    class Meta:
        model = PropertyVerification
        fields = ["id_passport", "tel", "property_type", "property_details", "message"]
        widgets = {
            "message": forms.Textarea(attrs={"rows": 4}),
        }


class PropertyVerificationForm(forms.Form):
    status_choices = [
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]

    status = forms.ChoiceField(choices=status_choices)
    verifier_name = forms.CharField(max_length=100)
    verification_message = forms.CharField(widget=forms.Textarea, required=False)


class OfficeForm(forms.ModelForm):
    class Meta:
        model = Office
        fields = ["name", "email"]


class PropertyTypeForm(forms.ModelForm):
    offices = forms.ModelMultipleChoiceField(
        queryset=Office.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
    )

    class Meta:
        model = PropertyType
        fields = ["name", "description", "offices"]
