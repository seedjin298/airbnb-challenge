from django.contrib import admin
from django.db.models.query import QuerySet
from .models import Tweet, Like


class ElonMuskFilter(admin.SimpleListFilter):
    title = "Check if Tweet Contains Elon Musk!"

    parameter_name = "word"

    def lookups(self, request, model_admin):
        return [
            ("contain", "Contain"),
            ("not_contain", "Don't Contain"),
        ]

    def queryset(self, request, tweets):
        is_contain = self.value()
        if is_contain == "contain":
            return tweets.filter(payload__icontains="Elon Musk")
        if is_contain == "not_contain":
            return tweets.exclude(payload__icontains="Elon Musk")
        else:
            tweets


@admin.register(Tweet)
class TweetAdmin(admin.ModelAdmin):
    list_display = (
        "payload",
        "total_likes",
        "user",
        "updated_at",
    )
    list_filter = (
        ElonMuskFilter,
        "created_at",
    )
    search_fields = (
        "payload",
        "user__username",
    )


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "tweet",
        "updated_at",
    )
    list_filter = ("created_at",)
    search_fields = ("user__username",)
