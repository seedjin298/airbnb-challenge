from django.conf import settings
from django.contrib.auth import authenticate, login, logout

from rest_framework.views import APIView
from rest_framework.exceptions import NotFound, ParseError, PermissionDenied
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from .models import User
from . import serializers
from tweets.serializers import TweetsSerializer


# Create your views here.
class UsersView(APIView):
    def get(self, request):
        all_users = User.objects.all()
        serializer = serializers.UsersSerializer(
            all_users,
            many=True,
        )
        return Response(serializer.data)

    def post(self, request):
        password = request.data.get("password")
        if not password:
            raise ParseError
        serializer = serializers.UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(password)
            user.save()
            serializer = serializers.UserSerializer(user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserView(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_user(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        serializer = serializers.UserSerializer(self.get_user(pk))
        return Response(serializer.data)

    def put(self, request, pk):
        user = self.get_user(pk)
        if user != request.user:
            raise PermissionDenied
        serializer = serializers.UserSerializer(
            user,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            keys = list(request.data.keys())
            available_keys = ["username", "name", "email", "gender"]
            for key in keys:
                if key not in available_keys:
                    return Response(
                        {
                            "error": "Please update from username, name, email, and gender"
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            user = serializer.save()
            serializer = serializers.UserSerializer(user)
            return Response(serializer.data)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )


class UserTweetsView(UserView):
    def get(self, request, pk):
        serializer = TweetsSerializer(
            self.get_user(pk).tweets.all(),
            many=True,
        )
        return Response(serializer.data)


class UserChangePassword(APIView):

    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")
        if not old_password or not new_password:
            raise ParseError
        if user.check_password(old_password) and old_password != new_password:
            user.set_password(new_password)
            user.save()
            return Response(status=status.HTTP_200_OK)
        else:
            raise ParseError


class UserLogIn(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            raise ParseError
        user = authenticate(
            request,
            username=username,
            password=password,
        )
        if user:
            login(request, user)
            return Response({"ok": "Welcome!"})
        else:
            return Response(
                {"error": "wrong password"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class UserLogOut(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"ok": "bye!"})
