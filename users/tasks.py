from datetime import date, timedelta

from celery import shared_task

from users.models import User


@shared_task
def deactivate_user():
    for user in User.objects.all():
        if user.last_login and date.today() - user.last_login.date() > timedelta(days=30):
            user.is_active = False
            user.save()
