from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from course.models import Course, Lesson, Payment, Subscription
from course.services import get_session
from course.validators import UrlValidator


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [UrlValidator(field='url')]


class CourseSerializer(serializers.ModelSerializer):
    lesson_count = serializers.IntegerField(source='lesson_set.all.count', read_only=True)
    lessons = LessonSerializer(source='lesson_set', many=True, read_only=True)
    subscribed = serializers.SerializerMethodField()

    def get_subscribed(self, obj):
        return Subscription.objects.filter(user=self.context['request'].user, course=obj).exists()

    class Meta:
        model = Course
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    payment_url = serializers.SerializerMethodField(read_only=True)
    def get_payment_url(self, obj: Payment):
        if obj.session:
            session = get_session(obj.session)
            return session.url
        return None

    class Meta:
        model = Payment
        fields = '__all__'


class SubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscription
        fields = '__all__'
        validators = [UniqueTogetherValidator(queryset=Subscription.objects.all(),
                                              fields=['user', 'course'],
                                              message='Вы уже подписаны на этот курс')]
