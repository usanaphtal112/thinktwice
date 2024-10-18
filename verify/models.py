from django.db import models
from django.contrib.auth import get_user_model

CustomUser = get_user_model()


class PropertyType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Office(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    property_types = models.ManyToManyField(PropertyType, related_name="offices")

    def __str__(self):
        return self.name


class PropertyVerification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    id_passport = models.CharField(max_length=50)
    tel = models.CharField(max_length=15)
    property_type = models.ForeignKey(PropertyType, on_delete=models.CASCADE)
    property_details = models.TextField()
    fee = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    request_type = models.CharField(max_length=50, default="Verification")
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.property_type.name}"

    @property
    def overall_status(self):
        office_verifications = self.office_verifications.all()
        if all(v.status == "Approved" for v in office_verifications):
            return "Approved by all"
        elif any(v.status == "Rejected" for v in office_verifications):
            return "Rejected by some"
        else:
            return "Pending"


class OfficeVerification(models.Model):
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Approved", "Approved"),
        ("Rejected", "Rejected"),
    ]

    property_verification = models.ForeignKey(
        PropertyVerification,
        related_name="office_verifications",
        on_delete=models.CASCADE,
    )
    office = models.ForeignKey(Office, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="Pending")
    verifier_name = models.CharField(max_length=100, blank=True)
    verifier_message = models.TextField(null=True, blank=True)
    token = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.office.name} - {self.property_verification.property_type.name}"
