from django.db import models


class ConsultationRequest(models.Model):
    """Заявка на консультацию по курсу «Технологии внедрения ПО»."""

    name = models.CharField("Имя", max_length=100)
    email = models.EmailField("Электронная почта")
    topic = models.CharField("Тема", max_length=200)
    message = models.TextField("Сообщение")
    created_at = models.DateTimeField("Создана", auto_now_add=True)

    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} <{self.email}>: {self.topic}"
