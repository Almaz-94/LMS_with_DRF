from django.urls import path

from course.apps import CourseConfig
from rest_framework.routers import DefaultRouter

from course.views import CourseViewSet, LessonCreateAPIView, LessonListAPIView, LessonRetrieveAPIView, \
    LessonUpdateAPIView, LessonDestroyAPIView, PaymentCreateAPIView, PaymentListAPIView, PaymentRetrieveAPIView, \
    SubscriptionCreateAPIView, SubscriptionDestroyAPIView

app_name = CourseConfig.name


router = DefaultRouter()
router.register(r'course', CourseViewSet, basename='course')
urlpatterns = [
    path('lesson/create/', LessonCreateAPIView.as_view(), name='lesson_create'),
    path('lesson/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lesson'),
    path('lesson/list/', LessonListAPIView.as_view(), name='lesson_list'),
    path('lesson/update/<int:pk>/', LessonUpdateAPIView.as_view(), name='lesson_update'),
    path('lesson/delete/<int:pk>/', LessonDestroyAPIView.as_view(), name='lesson_delete'),

    path('payment/<int:pk>/', PaymentRetrieveAPIView.as_view(), name='payment'),
    path('payment/list/', PaymentListAPIView.as_view(), name='payment_list'),
    path('payment/create/', PaymentCreateAPIView.as_view(), name='payment_create'),

    path('subscribe/<int:course_pk>/', SubscriptionCreateAPIView.as_view(), name='subscribe'),
    path('unsubscribe/<int:course_pk>/', SubscriptionDestroyAPIView.as_view(), name='unsubscribe'),

] + router.urls
