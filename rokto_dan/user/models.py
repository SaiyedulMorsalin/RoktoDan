from django.db import models
from django.contrib.auth.models import User
from .constants import BLOOD_GROUP


# Create your models here.
# class UserRegister(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     image = models.ImageField(
#         upload_to="user/images/", default="user/images/default-user.png"
#     )
#     age = models.IntegerField()
#     address = models.CharField(max_length=255)
#     last_donation_date = models.DateField(null=True, blank=True)
#     is_available = models.BooleanField(default=True)
#     mobile_no = models.CharField(max_length=12)

#     def __str__(self):
#         return f"{self.user.first_name} {self.user.last_name}"


class DonorProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="donor_profile"
    )
    blood_group = models.CharField(max_length=4, choices=BLOOD_GROUP)
    district = models.CharField(max_length=100)
    date_of_donation = models.DateField(null=True, blank=True)  # Optional field
    donor_type = models.CharField(
        max_length=50
    )  # Example: 'regular', 'emergency', etc.
    is_available = models.BooleanField(default=True)  # Ensure this field is defined

    def __str__(self):
        return f"{self.user.username} - {self.blood_group}"
