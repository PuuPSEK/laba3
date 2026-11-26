# Одностраничный проект на Django — курс «Технологии внедрения ПО»

Учебный проект для практической работы №3 (CI/CD).

## Что это

Одностраничный сайт курса «Технологии внедрения программного обеспечения»:
программа, список лабораторных работ и форма заявки на консультацию.
Заявки сохраняются в SQLite и доступны в админке Django.

## Стек

- Python 3.11+
- Django 5.2+ (SQLite)
- Gunicorn + WhiteNoise
- flake8, unittest (Django TestCase)
- GitHub Actions (self-hosted runner)

## Локальный запуск

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Сайт: http://127.0.0.1:8000

## Тесты и линтер

```bash
python -m flake8 --max-line-length=120 --exclude=.git,__pycache__,.venv .
python manage.py test -v 2
```

## CI/CD

`push` в `main` запускает:

1. **Lint & tests** — flake8 и тесты Django.
2. **Deploy to production** — публикация в `/opt/tvepo-site`,
   миграции, сбор статики, перезапуск systemd-сервиса
   и smoke-тест на порту 8001.
