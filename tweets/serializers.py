from rest_framework import serializers
from .models import Tweet


class TweetSerializer(serializers.ModelSerializer):
    user = serializers.CharField()

    class Meta:
        model = Tweet
        fields = (
            "id",
            "user",
            "payload",
            "updated_at",
        )
