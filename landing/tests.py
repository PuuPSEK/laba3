from django.test import TestCase
from django.urls import reverse

from .models import ConsultationRequest


class LandingPageTests(TestCase):
    def test_index_page_opens(self):
        response = self.client.get(reverse("landing:index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "landing/index.html")
        self.assertContains(response, "Технологии внедрения")

    def test_valid_request_is_saved(self):
        response = self.client.post(
            reverse("landing:index"),
            {
                "name": "Никита",
                "email": "zai.nikita@mail.ru",
                "topic": "Вопрос по CI/CD",
                "message": "Как настроить автодеплой на продуктовый сервер?",
            },
        )
        self.assertRedirects(response, reverse("landing:index"))
        self.assertEqual(ConsultationRequest.objects.count(), 1)
        item = ConsultationRequest.objects.get()
        self.assertEqual(item.name, "Никита")
        self.assertEqual(item.topic, "Вопрос по CI/CD")

    def test_invalid_request_is_not_saved(self):
        response = self.client.post(
            reverse("landing:index"),
            {
                "name": "A",
                "email": "not-an-email",
                "topic": "ok",
                "message": "short",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ConsultationRequest.objects.count(), 0)
        self.assertContains(response, "Укажите имя")
        self.assertContains(response, "Некорректный адрес")

    def test_counter_shows_number_of_requests(self):
        ConsultationRequest.objects.create(
            name="Иван",
            email="ivan@example.com",
            topic="Тема первая",
            message="Сообщение достаточной длины",
        )
        ConsultationRequest.objects.create(
            name="Пётр",
            email="petr@example.com",
            topic="Тема вторая",
            message="Ещё одно сообщение для теста",
        )
        response = self.client.get(reverse("landing:index"))
        self.assertContains(response, "2</strong>")

    def test_model_string_representation(self):
        item = ConsultationRequest.objects.create(
            name="Анна",
            email="anna@example.com",
            topic="Docker",
            message="Как собрать образ приложения?",
        )
        self.assertEqual(str(item), "Анна <anna@example.com>: Docker")

    def test_last_requests_are_shown(self):
        ConsultationRequest.objects.create(
            name="Олег",
            email="oleg@example.com",
            topic="Kubernetes",
            message="Как создать ConfigMap в кластере?",
        )
        response = self.client.get(reverse("landing:index"))
        self.assertContains(response, "Олег")
        self.assertContains(response, "Kubernetes")
