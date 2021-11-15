from django.contrib.auth import authenticate

from rest_framework import serializers
from .models import User


class RegistrationSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password', 'token']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    """
    Separate serializer for login
    Nothing to change in database
    """

    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        """
        Validate login data
        """

        email = data.get('email', None)
        password = data.get('password', None)

        # email and password cannot be None
        if email is None:
            raise serializers.ValidationError(
                'An email address is required to log in.'
            )

        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )

        # try to find an existing user
        user = authenticate(username=email, password=password)

        # raise or return validated
        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password was not found.'
            )

        else:
            return {
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'token': user.token
            }
