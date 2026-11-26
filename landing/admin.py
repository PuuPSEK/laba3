from django.contrib import admin

from .models import ConsultationRequest


@admin.register(ConsultationRequest)
class ConsultationRequestAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "topic", "created_at")
    search_fields = ("name", "email", "topic")
    list_filter = ("created_at",)
