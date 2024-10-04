from rest_framework.views import APIView
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from .models import User
from .serializers import UsersSerializer, UserSerializer
from tweets.serializers import TweetSerializer


# Create your views here.
class UsersView(APIView):
    def get(self, request):
        all_users = User.objects.all()
        serializer = UsersSerializer(
            all_users,
            many=True,
        )
        return Response(serializer.data)


class UserView(APIView):
    def get_user(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        serializer = UserSerializer(self.get_user(pk))
        return Response(serializer.data)


class UserTweetsView(UserView):
    def get(self, request, pk):
        serializer = TweetSerializer(
            self.get_user(pk).tweets.all(),
            many=True,
        )
        return Response(serializer.data)
