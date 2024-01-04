import pytest
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError

from auth_api.serializers import RegisterSerializer


@pytest.mark.django_db
def test_register_serializer_valid_data(new_user_payload):
    serializer = RegisterSerializer(data=new_user_payload)
    assert serializer.is_valid()

    user = serializer.save()
    assert User.objects.filter(username=new_user_payload["username"]).exists()
    assert user.first_name == new_user_payload["first_name"]
    assert user.check_password(new_user_payload["password"])


@pytest.mark.django_db(transaction=True)
def test_register_serializer_invalid_data(new_user_payload):
    invalid_data = new_user_payload.copy()
    invalid_data["email"] = "invalidemail"
    serializer = RegisterSerializer(data=invalid_data)
    with pytest.raises(ValidationError):
        serializer.is_valid(raise_exception=True)


@pytest.mark.django_db(transaction=True)
def test_register_serializer_duplicate_email(new_user_payload, create_user):
    new_user_payload["email"] = create_user.email
    serializer = RegisterSerializer(data=new_user_payload)

    assert not serializer.is_valid()
    assert "email" in serializer.errors
