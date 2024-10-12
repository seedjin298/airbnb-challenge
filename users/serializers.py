from rest_framework import serializers
from .models import User


class UsersSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            "username",
            "gender",
        )


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "name",
            "email",
            "gender",
        )
