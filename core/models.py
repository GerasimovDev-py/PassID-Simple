from django.db import models
from django.utils import timezone
from datetime import timedelta

class Visitor(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидание'),
        ('approved', 'Допущен'),
        ('departed', 'Ушёл'),
    ]

    DOCUMENT_TYPE_CHOICES = [
        ('passport_rf', 'Паспорт РФ'),
        ('international_passport', 'Загранпаспорт'),
        ('driver_license', 'Водительское удостоверение'),
        ('other', 'Другой документ'),
    ]

    full_name = models.CharField("ФИО полностью", max_length=255)
    document_type = models.CharField("Тип документа", max_length=30, choices=DOCUMENT_TYPE_CHOICES, default='passport_rf')
    document_number = models.CharField("Номер документа", max_length=50)
    phone = models.CharField("Телефон", max_length=20, blank=True, null=True)

    escort = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='accompanied_visitors'
    )

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    arrival_time = models.DateTimeField("Время прихода", null=True, blank=True)
    departure_time = models.DateTimeField("Время ухода", null=True, blank=True)
    valid_until = models.DateTimeField("Действует до", null=True, blank=True)

    organization = models.CharField("Организация", max_length=255, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} — {self.document_number}"

    class Meta:
        verbose_name = "Посетитель"
        verbose_name_plural = "Посетители"
        ordering = ['-created_at']