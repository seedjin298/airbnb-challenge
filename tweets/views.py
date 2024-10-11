from rest_framework.views import APIView
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST
from .models import Tweet
from . import serializers


# Create your views here.
class TweetsView(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        all_tweets = Tweet.objects.all()
        serializer = serializers.TweetsSerializer(
            all_tweets,
            many=True,
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = serializers.TweetSerializer(
            data=request.data,
        )
        if serializer.is_valid():
            tweet = serializer.save(user=request.user)
            serializer = serializers.TweetSerializer(
                tweet,
                context={"user": request.user},
            )
            return Response(serializer.data)
        else:
            return Response(
                serializer.errors,
                status=HTTP_400_BAD_REQUEST,
            )


class TweetView(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_tweet(self, pk):
        try:
            return Tweet.objects.get(pk=pk)
        except:
            raise NotFound

    def get(self, request, pk):
        tweet = self.get_tweet(pk)
        serializer = serializers.TweetSerializer(
            tweet,
            context={"user": request.user},
        )
        return Response(serializer.data)

    def put(self, request, pk):
        tweet = self.get_tweet(pk)
        if tweet.user != request.user:
            raise PermissionDenied

    def delete(self, request, pk):
        pass
