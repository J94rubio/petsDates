from django.db import models


class Cita(models.Model):

    ESTADOS = [
        ('Pendiente', 'Pendiente'),
        ('Confirmada', 'Confirmada'),
        ('Completada', 'Completada'),
        ('Cancelada', 'Cancelada'),
    ]

    mascota = models.ForeignKey(
        'mascotas.Mascota',
        on_delete=models.CASCADE,
        related_name='citas'
    )

    fecha = models.DateField()

    motivo = models.CharField(
        max_length=200
    )

    estado = models.CharField(
        max_length=50,
        choices=ESTADOS,
        default='Pendiente'
    )

    def __str__(self):
        return f"{self.mascota.nombre} - {self.fecha}"