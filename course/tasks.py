from datetime import datetime, timedelta, date

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

from course.models import Subscription
from users.models import User


@shared_task
def send_update_notification():
    for subscription in Subscription.objects.all():
        if subscription.course.last_updated:
            if date.today() - subscription.course.last_updated.date() < timedelta(days=2):

                send_mail(
                    subject='Course update',
                    message='Course in your subscription just got a new update',
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[subscription.user.email]
                )


