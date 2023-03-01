from django.conf import settings
from rest_framework import serializers

from .models import User


class AuthSignUpSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=256)
    email = serializers.EmailField()

    class Meta:
        fields = (
            'email',
            'username'
        )
        model = User

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'You can not use \'me\' as username'
            )
        return value


class AuthTokenSerializer(serializers.Serializer):
    confirmation_code = serializers.CharField(
        max_length=settings.RND_STR_LENTH,
        required=True
    )
    username = serializers.CharField(
        max_length=150,
        required=True
    )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )
        model = User


class MeUserSerrializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )
        model = User
        read_only_fields = (
            'role',
        )
