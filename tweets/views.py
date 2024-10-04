from rest_framework.views import APIView
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from .models import Tweet
from .serializers import TweetSerializer


# Create your views here.
class TweetsView(APIView):
    def get(self, request):
        all_tweets = Tweet.objects.all()
        serializer = TweetSerializer(
            all_tweets,
            many=True,
        )
        return Response(serializer.data)


class TweetView(APIView):
    def get_tweet(self, pk):
        try:
            return Tweet.objects.get(pk=pk)
        except:
            raise NotFound

    def get(self, request, pk):
        serializer = TweetSerializer(self.get_tweet(pk))
        return Response(serializer.data)
