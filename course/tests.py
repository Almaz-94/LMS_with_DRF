from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from course.models import Lesson, Course, Subscription
from users.models import User


class LessonTestCase(APITestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = User.objects.create(email='user@t.ru', password='test')
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(name='MFTI')
        self.lesson1 = Lesson.objects.create(name='Math', course=self.course, creator=self.user)
        self.lesson2 = Lesson.objects.create(name='Geometry', course=self.course, creator=self.user)

    def test_create_lesson(self):
        response = self.client.post(
            '/lesson/create/',
            data={'name': 'English',
                  'course': self.course.pk}
        )

        self.assertEqual(response.status_code,
                         status.HTTP_201_CREATED)

        self.assertEqual(response.json(),
                         {
                             "id": 3,
                             "name": "English",
                             "description": None,
                             "preview": None,
                             "url": None,
                             "course": self.course.pk,
                             "creator": self.user.pk
                         }
                         )

    def test_retrieve_lesson(self):
        response = self.client.get(f'/lesson/{self.lesson1.pk}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(),
                         {
                             'id': self.lesson1.pk,
                             'name': self.lesson1.name,
                             'description': None,
                             'preview': None,
                             'url': None,
                             'course': self.lesson1.course.pk,
                             'creator': self.lesson1.creator.pk
                         }
                         )

    def test_list_lesson(self):
        response = self.client.get('/lesson/list/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()['results']), Lesson.objects.all().count())

    def test_delete_lesson(self):
        lesson1_pk = self.lesson1.pk
        response = self.client.delete(f'/lesson/delete/{lesson1_pk}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(f'/lesson/{lesson1_pk}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        response = self.client.get(f'/lesson/list/')
        self.assertEqual(len(response.json()['results']), Lesson.objects.all().count())

    def test_update_lesson(self):
        response = self.client.put(f'/lesson/update/{self.lesson1.pk}/', data={'name': 'Updated math'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['id'], self.lesson1.pk)
        self.assertEqual(response.json()['name'], 'Updated math')


class SubscriptionTestCase(APITestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = User.objects.create(email='usr@t.ru', password='test123')
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(name='MFTI', creator=self.user)

    def test_create_subscription(self):
        response = self.client.post(f'/subscribe/{self.course.pk}/')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(f'/course/{self.course.pk}/')
        self.assertEqual(response.json()['subscribed'], True)

    def test_delete_subscription(self):
        self.sub = Subscription.objects.create(user=self.user, course=self.course)
        response = self.client.delete(f'/unsubscribe/{self.course.pk}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(f'/course/{self.course.pk}/')
        self.assertEqual(response.json()['subscribed'], False)
