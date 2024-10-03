from django.urls import path
from . import views

urlpatterns = [
    path("", views.tweets),
    path("<int:tweet_id>", views.tweet),
]
