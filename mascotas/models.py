from django.db import models

class Mascota(models.Model):
    nombre = models.CharField(max_length=100)
    especie = models.CharField(max_length=50)
    raza = models.CharField(max_length=100)
    edad = models.PositiveIntegerField()
    propietario = models.CharField(max_length=150)

    def __str__(self):
        return self.nombre