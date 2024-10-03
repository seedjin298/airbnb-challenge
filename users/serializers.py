from rest_framework import serializers


class UsersSerializer(serializers.Serializer):

    name = serializers.CharField(
        max_length=150,
        read_only=True,
    )
    gender = serializers.CharField()


class UserSerializer(serializers.Serializer):

    pk = serializers.IntegerField(
        read_only=True,
    )
    first_name = serializers.CharField(
        max_length=150,
        read_only=True,
    )
    last_name = serializers.CharField(
        max_length=150,
        read_only=True,
    )
    name = serializers.CharField(
        max_length=150,
        read_only=True,
    )
    gender = serializers.CharField(
        max_length=10,
    )
