# serializers.py

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import DonorProfile
from .constants import BLOOD_GROUP


# Serializer for the User model
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "email"]


# Serializer for user registration, including validation for password confirmation
class RegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(required=True)
    mobile_number = serializers.CharField(max_length=12, required=True)
    blood_group = serializers.ChoiceField(choices=BLOOD_GROUP, required=True)

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "mobile_number",
            "blood_group",
            "password",
            "confirm_password",
        ]

    def save(self, **kwargs):
        # Extract the data from validated_data
        username = self.validated_data["username"]
        first_name = self.validated_data["first_name"]
        last_name = self.validated_data["last_name"]
        email = self.validated_data["email"]
        mobile_number = self.validated_data["mobile_number"]
        blood_group = self.validated_data["blood_group"]
        password = self.validated_data["password"]
        password2 = self.validated_data["confirm_password"]

        # Check if passwords match
        if password != password2:
            raise serializers.ValidationError({"error": "Passwords don't match"})

        # Check if the email is already registered
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"error": "Email already exists"})

        # Create the User account
        account = User(
            username=username, email=email, first_name=first_name, last_name=last_name
        )
        account.set_password(password)
        account.is_active = False  # Account is inactive until email verification
        account.save()
        return account


# Serializer for user login
class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)


# Serializer for DonorProfile, including nested fields for user details
class DonorProfileSerializer(serializers.ModelSerializer):
    # Nested fields to display user information
    username = serializers.CharField(source="user.username", read_only=True)
    email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = DonorProfile
        fields = [
            "id",
            "username",
            "email",
            "blood_group",
            "district",
            "date_of_donation",
            "donor_type",
            "is_available",
        ]

    def create(self, validated_data):
        """
        Creates a DonorProfile instance with the associated user.
        """
        # Extract the user from the request context
        user = (
            self.context["request"].user
            if self.context["request"].user.is_authenticated
            else None
        )
        # Ensure the user is provided when creating the profile
        if not user:
            raise serializers.ValidationError({"user": "User must be authenticated"})

        # Create the DonorProfile instance with the validated data
        donor_profile = DonorProfile.objects.create(user=user, **validated_data)
        return donor_profile

    def update(self, instance, validated_data):
        """
        Updates the DonorProfile fields.
        """
        # Update each field in the instance with the provided validated data
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
