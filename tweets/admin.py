from django.contrib import admin
from .models import Tweet, Like


@admin.register(Tweet)
class TweetAdmin(admin.ModelAdmin):
    list_display = (
        "payload",
        "user",
        "created_at",
        "updated_at",
    )
    list_filter = (
        "payload",
        "user",
        "created_at",
        "updated_at",
    )


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "tweet",
        "created_at",
        "updated_at",
    )
    list_filter = (
        "user",
        "tweet",
        "created_at",
        "updated_at",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )
