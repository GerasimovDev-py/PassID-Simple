from django.db import models
import uuid

class StaffMember(models.Model):
    name = models.CharField("ФИО сотрудника", max_length=100)
    token = models.CharField("Ключ доступа", max_length=100, unique=True, default=uuid.uuid4)

    def __str__(self):
        return self.name

class Visitor(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидание'),
        ('approved', 'Одобрено'),
        ('rejected', 'Отказано')
    ]
    
    full_name = models.CharField(max_length=255)
    passport = models.CharField("Серия и номер паспорта", max_length=50, unique=False)
    phone = models.CharField(max_length=20)
    organization = models.CharField(max_length=255)

    escort = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)
    
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} — {self.passport}"
