from rest_framework import serializers
from .models import Tweet
from users.serializers import UsersSerializer


class TweetsSerializer(serializers.ModelSerializer):
    user = serializers.CharField()

    class Meta:
        model = Tweet
        fields = (
            "id",
            "user",
            "payload",
            "updated_at",
        )


class TweetSerializer(serializers.ModelSerializer):
    user = UsersSerializer(read_only=True)
    is_user = serializers.SerializerMethodField()

    class Meta:
        model = Tweet
        fields = "__all__"

    def get_is_user(self, tweet):
        user = self.context["user"]
        return tweet.user == user
