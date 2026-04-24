from django.db import models
from django.contrib.auth.models import User

class Visitor(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидание'),
        ('approved', 'Одобрено'),
        ('departed', 'Ушёл'),
    ]

    DOCUMENT_TYPE_CHOICES = [
        ('passport_rf', 'Паспорт РФ'),
        ('car_plate', 'Автомобильный номер'),
        ('other', 'Другой документ'),
    ]

    full_name = models.CharField("ФИО посетителя", max_length=255)
    document_type = models.CharField("Тип документа", max_length=50, choices=DOCUMENT_TYPE_CHOICES)
    document_number = models.CharField("Номер документа", max_length=50)
    
    escort_name = models.CharField("ФИО ответственного", max_length=255)
    escort_phone = models.CharField("Телефон ответственного", max_length=20, blank=True)
    
    valid_until = models.DateTimeField("Действует до")
    kpp = models.CharField("КПП", max_length=10, choices=[('kpp1', 'КПП-1'), ('kpp2', 'КПП-2')])
    comment = models.TextField("Комментарий", blank=True, null=True)
    
    status = models.CharField("Статус", max_length=20, choices=STATUS_CHOICES, default='pending')
    arrival_time = models.DateTimeField("Время прихода", null=True, blank=True)
    departure_time = models.DateTimeField("Время ухода", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} — {self.kpp}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    kpp = models.CharField(max_length=10, choices=[('kpp1', 'КПП-1'), ('kpp2', 'КПП-2')], default='kpp1', blank=True, null=True)
    is_responsible = models.BooleanField("Ответственный", default=False)
    responsible_full_name = models.CharField("ФИО ответственного", max_length=255, blank=True)
    responsible_phone = models.CharField("Телефон ответственного", max_length=20, blank=True)

    def __str__(self):
        role = "Ответственный" if self.is_responsible else "Охрана"
        return f"{self.user.username} — {role}"