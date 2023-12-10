from datetime import datetime, timedelta

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

from course.models import Subscription
from users.models import User


@shared_task
def send_update_notification():
    for subscription in Subscription.objects.all():
        if datetime.now() - subscription.last_updated < timedelta(hours=24):

            send_mail(
                subject='Course update',
                message='Course in your subscription just got a new update',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[subscription.user.email]
            )


@shared_task
def deactivate_user():
    for user in User.objects.all():
        if user.last_login and datetime.now() - user.last_login > timedelta(days=30):
            user.is_active = False
            user.save()
