from django.contrib import admin

from course.models import Course, Lesson, Subscription


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'creator',)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'course', 'creator',)


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'course',)
