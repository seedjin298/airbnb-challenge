from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User
from .serializers import UsersSerializer, UserSerializer
from tweets.serializers import TweetSerializer


# Create your views here.
@api_view()
def users(request):
    users = User.objects.all()
    serializer = UsersSerializer(users, many=True)
    return Response(
        {
            "ok": True,
            "users": serializer.data,
        },
    )


@api_view()
def user(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
        serializer = UserSerializer(user)
        return Response(
            {
                "ok": True,
                "user_info": serializer.data,
            },
        )
    except User.DoesNotExist:
        return Response(
            {
                "ok": False,
            },
        )


@api_view()
def user_tweets(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
        all_user_tweets = user.tweets.all()
        serializer = TweetSerializer(all_user_tweets, many=True)
        return Response(
            {
                "ok": True,
                "user_tweets": serializer.data,
            },
        )
    except User.DoesNotExist:
        return Response(
            {
                "ok": False,
            },
        )
