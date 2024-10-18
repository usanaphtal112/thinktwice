from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from .models import OfficeVerification


@shared_task
def send_verification_email(property_verification_office_id):
    try:
        # Fetch the verification office and its details
        pvo = OfficeVerification.objects.get(id=property_verification_office_id)
        office_email = pvo.office.email
        property_verification = pvo.property_verification
        property_details = property_verification.property.details

        # Generate a unique URL for this office's verification link
        verification_link = reverse(
            "verify_property", kwargs={"token": pvo.verification_token}
        )
        full_link = f"{settings.SITE_URL}{verification_link}"

        # Email subject and message
        subject = f"Property Verification Request for {property_verification.property.property_type.name}"
        message = f"""
        Dear {pvo.office.name},

        A property verification request has been assigned to your office for verification.
        Property ID: {property_verification.property.id}
        Property Details: {property_details}

        Please click on the link below to review and verify the property:
        {full_link}

        Thank you,
        Rwanda Property Registration Team
        """

        # Send email
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [office_email],
            fail_silently=False,
        )
    except OfficeVerification.DoesNotExist:
        print(
            f"OfficeVerification with ID {property_verification_office_id} does not exist"
        )
