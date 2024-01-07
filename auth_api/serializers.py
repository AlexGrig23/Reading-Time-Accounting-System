# Description: Serializers for the auth_api app.

from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for registering new users.
    Uses Django's default User model to create new users.
    Includes fields for username, email, password, first name, and last name.
    """

    password = serializers.CharField(
        write_only=True, required=True, style={"input_type": "password"}
    )
    email = serializers.EmailField(
        required=True, validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = ("username", "email", "password", "first_name", "last_name")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        """
        Creates a new user based on validated data.
        Uses the create_user method to correctly hash the password.
        :param validated_data:
        :return: object of type User
        """
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
        )

        return user
