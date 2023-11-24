from django.urls import path

from users.apps import UsersConfig
from users.views import UserCreateAPIView, MyTokenObtainPairView, UserRetrieveAPIView, UserUpdateAPIView

app_name = UsersConfig.name


urlpatterns = [
    path('register/', UserCreateAPIView.as_view(), name='user_register'),
    path('<int:pk>/', UserRetrieveAPIView.as_view(), name='user'),
    path('update/<int:pk>/', UserUpdateAPIView.as_view(), name='user_update'),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),

]