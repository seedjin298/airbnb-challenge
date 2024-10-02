from django.shortcuts import render
from .models import Tweet


# Create your views here.
def tweets(request):
    tweets = Tweet.objects.all()
    return render(
        request,
        "all_tweets.html",
        {
            "tweets": tweets,
            "title": "Tweets",
        },
    )


def tweet(request, pk):
    try:
        tweet = Tweet.objects.get(pk=pk)
        return render(
            request,
            "one_tweet.html",
            {
                "tweet": tweet,
            },
        )
    except Tweet.DoesNotExist:
        return render(
            request,
            "one_tweet.html",
            {
                "not_found": True,
            },
        )
