from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.shortcuts import redirect, render

from .models import ConsultationRequest


def _validate(data):
    errors = {}
    name = data.get("name", "").strip()
    email = data.get("email", "").strip()
    topic = data.get("topic", "").strip()
    message = data.get("message", "").strip()

    if len(name) < 2:
        errors["name"] = "Укажите имя (не короче 2 символов)."
    if not email:
        errors["email"] = "Укажите электронную почту."
    else:
        try:
            validate_email(email)
        except ValidationError:
            errors["email"] = "Некорректный адрес электронной почты."
    if len(topic) < 3:
        errors["topic"] = "Укажите тему обращения."
    if len(message) < 10:
        errors["message"] = "Сообщение должно содержать не менее 10 символов."

    cleaned = {
        "name": name,
        "email": email,
        "topic": topic,
        "message": message,
    }
    return cleaned, errors


def _context(form=None, errors=None):
    return {
        "form": form or {},
        "errors": errors or {},
        "requests": ConsultationRequest.objects.all()[:5],
        "total": ConsultationRequest.objects.count(),
    }


def index(request):
    if request.method == "POST":
        cleaned, errors = _validate(request.POST)
        if not errors:
            ConsultationRequest.objects.create(**cleaned)
            messages.success(
                request, "Заявка отправлена. Преподаватель свяжется с вами."
            )
            return redirect("landing:index")
        messages.error(request, "Проверьте правильность заполнения формы.")
        return render(request, "landing/index.html", _context(cleaned, errors))

    return render(request, "landing/index.html", _context())
