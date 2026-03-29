from django.db import models
import uuid

class StaffMember(models.Model):
    name = models.CharField("ФИО сотрудника", max_length=100)
    token = models.CharField("Ключ доступа", max_length=100, unique=True, default=uuid.uuid4)

    def __str__(self):
        return self.name

from django.db import models

class Visitor(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидание'),
        ('approved', 'Одобрено'),
    ]
    
    full_name = models.CharField(max_length=255)
    passport = models.CharField("Серия и номер паспорта", max_length=50)
    phone = models.CharField(max_length=20)
    organization = models.CharField(max_length=255)

    escort = models.ForeignKey(
        'self', 
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name='accompanied_visitors'
    )
    
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} — {self.passport}"
