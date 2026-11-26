from django.test import TestCase
from django.urls import reverse

from .models import ConsultationRequest

VALID_FORM = {
    "name": "Никита",
    "email": "zai.nikita@mail.ru",
    "topic": "Вопрос по CI/CD",
    "message": "Как настроить автодеплой на продуктовый сервер?",
}


class LandingPageTests(TestCase):
    def test_page_opens(self):
        """Главная страница открывается и содержит заголовок."""
        response = self.client.get(reverse("landing:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Технологии внедрения")

    def test_valid_form_saves_request(self):
        """Корректная заявка сохраняется в базу."""
        response = self.client.post(reverse("landing:index"), VALID_FORM)
        self.assertRedirects(response, reverse("landing:index"))
###
        self.assertEqual(ConsultationRequest.objects.count(), 2)
###

    def test_invalid_form_shows_errors(self):
        """Пустая форма не сохраняется и показывает ошибки."""
        response = self.client.post(
            reverse("landing:index"),
            {"name": "", "email": "bad", "topic": "", "message": ""},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ConsultationRequest.objects.count(), 0)
        self.assertContains(response, "Укажите имя")

    def test_model_string(self):
        """Строковое представление заявки."""
        item = ConsultationRequest.objects.create(
            name="Анна",
            email="anna@example.com",
            topic="Docker",
            message="Как собрать образ приложения?",
        )
        self.assertEqual(str(item), "Анна <anna@example.com>: Docker")
