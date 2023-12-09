from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.create(
            email='al@m.ru',
            first_name='user',
            last_name='userov',
            is_staff=True,
            is_superuser=True
        )
        user.set_password('1233')
        user.save()
