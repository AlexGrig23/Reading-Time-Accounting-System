# Description: Authorization views.
"""
Basic authorization is implemented here, so that it has a more complete form,
you need to add: roles, permissions, password change, reset token, forgot password, etc.
"""

from rest_framework import generics

from auth_api.serializers import RegisterSerializer


class RegisterView(generics.CreateAPIView):
    """
    Register a new user
    requared fields: username, email, password
    """

    serializer_class = RegisterSerializer
