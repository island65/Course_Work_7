from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from habits.models import Habit
from users.models import User


class HabitTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="admin@example.com")
        self.user.set_password("123123")
        self.user.save()
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.habit = Habit.objects.create(
            owner=self.user,
            action="Сделать зарядку",
            pleasant_habit_sign=True,
            time="2024-07-13T10:00:00Z",
            place="Дом",
        )

    def test_create_habit(self):
        url = reverse("habits:create")
        data = {
            "owner": self.user.pk,
            "action": "Убрать лишние вещи",
            "pleasant_habit_sign": True,
            "time": "2024-07-13T10:00:00Z",
            "place": "Дом",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.count(), 2)
        self.assertTrue(Habit.objects.all().exists())

    def test_habit_list(self):
        url = reverse("habits:habits_list")
        response = self.client.get(url)
        data = response.json()
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "action": "Сделать зарядку",
                    "duration": "00:02:00",
                    "id": self.habit.pk,
                    "is_published": True,
                    "owner": self.user.pk,
                    "periodicity": 1,
                    "place": "Дом",
                    "pleasant_habit_sign": True,
                    "related_habit": None,
                    "reward": None,
                    "time": "2024-07-13T10:00:00Z",
                }
            ],
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)

    def test_habit_retrieve(self):
        url = reverse("habits:habit_retrieve", args=(self.habit.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["place"], self.habit.place)

    def test_habit_update(self):
        url = reverse("habits:habit_update", args=(self.habit.pk,))
        data = {
            "action": "Побегать на дорожке",
        }
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["action"], "Побегать на дорожке")

    def test_habit_delete(self):
        url = reverse("habits:habit_delete", args=(self.habit.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.count(), 0)
