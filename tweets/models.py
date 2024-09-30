from django.db import models
from common.models import CommonModel


class Tweet(CommonModel):
    payload = models.TextField(max_length=180)
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="tweets",
    )

    def __str__(self):
        return f"{self.user}'s Tweet"

    def total_likes(self):
        return self.likes.all().count()


class Like(CommonModel):
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="likes",
    )
    tweet = models.ForeignKey(
        "tweets.Tweet",
        on_delete=models.CASCADE,
        related_name="likes",
    )

    def __str__(self):
        return f"{self.user}'s Like"
