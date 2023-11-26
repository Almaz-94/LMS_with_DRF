from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics, status
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from course.models import Course, Lesson, Payment, Subscription
from course.paginators import LessonPaginator, CoursePaginator
from course.permissions import IsOwner, IsModerator
from course.serializers import CourseSerializer, LessonSerializer, PaymentSerializer, SubscriptionSerializer


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    pagination_class = CoursePaginator

    def perform_create(self, serializer):
        new_course = serializer.save()
        new_course.creator = self.request.user
        new_course.save()

    def get_queryset(self):
        queryset = Course.objects
        if not self.request.user.has_perms(perm_list=['course.change_course', 'course.change_lesson']):
            return queryset.filter(creator=self.request.user)
        return queryset.all()

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsAuthenticated]
        elif self.action == 'list' or self.action == 'retrieve':
            permission_classes = [IsOwner | IsModerator]
        elif self.action == 'update':
            permission_classes = [IsOwner | IsModerator]
        elif self.action == 'destroy':
            permission_classes = [IsOwner]
        return [permission() for permission in permission_classes]


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        new_lesson = serializer.save()
        new_lesson.creator = self.request.user
        new_lesson.save()


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsOwner | IsModerator]
    pagination_class = LessonPaginator

    def get_queryset(self):
        queryset = Lesson.objects
        if not self.request.user.has_perms(perm_list=['course.change_course', 'course.change_lesson']):
            return queryset.filter(creator=self.request.user)
        return queryset.all()


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsOwner | IsModerator]


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsOwner | IsModerator]


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsOwner]


class PaymentRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    permission_classes = [IsAuthenticated]


class PaymentListAPIView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('course', 'lesson', 'type',)
    ordering_fields = ['date', ]
    permission_classes = [IsAuthenticated]


class PaymentCreateAPIView(generics.CreateAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]


class SubscriptionCreateAPIView(generics.CreateAPIView):
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        course_pk = self.kwargs.get('course_pk')

        serializer = self.get_serializer(data={'user': request.user.pk, 'course': course_pk})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({'Вы подписались на курс.'}, status=status.HTTP_201_CREATED)


class SubscriptionDestroyAPIView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Subscription.objects.all()

    def get_object(self):
        course_pk = self.kwargs.get('course_pk')
        course = Course.objects.get(pk=course_pk)
        return Subscription.objects.get(user=self.request.user, course=course)

    def destroy(self, request, *args, **kwargs):
        obj = self.get_object()
        self.perform_destroy(obj)
        return Response('Вы отписались от курса.', status=status.HTTP_200_OK)