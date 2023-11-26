from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView


from users.models import User
from users.permissions import IsProfileOwner
from users.serializers import UserSerializer, MyTokenObtainPairSerializer


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserRetrieveAPIView(RetrieveAPIView):

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]


class UserUpdateAPIView(UpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsProfileOwner]


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
