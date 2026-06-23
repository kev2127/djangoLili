from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    ROLE_CHOICES = [
        ('Administrador', 'Administrador'),
        ('Cliente', 'Cliente'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Cliente')

    def __str__(self):
        return f"{self.user.username} ({self.role})"

class Record(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='record')
    created_at = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Appointment(models.Model):
    record = models.ForeignKey(Record, on_delete=models.CASCADE, related_name='appointments')
    administrator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, limit_choices_to={'profile__role': 'Administrador'}, related_name='admin_appointments')
    fecha = models.DateField()
    hora = models.TimeField()
    descripcion = models.TextField(blank=True)
    creado_el = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.record} - {self.fecha} {self.hora}"