from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.create(
            email='user@m.ru',
            first_name='user',
            last_name='userov',
            is_staff=False,
            is_superuser=False
        )
        user.set_password('1233')
        user.save()
