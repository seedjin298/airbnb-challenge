from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Tweet
from .serializers import TweetSerializer


# Create your views here.
@api_view()
def tweets(request):
    tweets = Tweet.objects.all()
    serializer = TweetSerializer(tweets, many=True)
    return Response(
        {
            "ok": True,
            "tweets": serializer.data,
        },
    )


@api_view()
def tweet(request, tweet_id):
    try:
        tweet = Tweet.objects.get(pk=tweet_id)
        serializer = TweetSerializer(tweet)
        return Response(
            {
                "ok": True,
                "tweet": serializer.data,
            },
        )
    except Tweet.DoesNotExist:
        return Response(
            {
                "ok": False,
            },
        )
