from django.urls import path
from . import views

urlpatterns = [
    path("", views.UsersView.as_view()),
    path("<int:pk>/", views.UserView.as_view()),
    path("<int:pk>/tweets/", views.UserTweetsView.as_view()),
    path("password/", views.UserChangePassword.as_view()),
    path("login/", views.UserLogIn.as_view()),
    path("logout/", views.UserLogOut.as_view()),
]
