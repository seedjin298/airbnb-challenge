from django.urls import path
from . import views

urlpatterns = [
    path("", views.TweetsView.as_view()),
    path("<int:pk>/", views.TweetView.as_view()),
]
