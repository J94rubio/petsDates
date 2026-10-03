from django.contrib import admin

from .models import Cita


@admin.register(Cita)
class CitaAdmin(admin.ModelAdmin):
    list_display = (
        'mascota',
        'fecha',
        'motivo',
        'estado',
    )

    list_filter = (
        'estado',
        'fecha',
    )

    search_fields = (
        'mascota__nombre',
        'motivo',
    )