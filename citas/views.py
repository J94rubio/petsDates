from django.shortcuts import redirect, render
from django.urls import reverse

from services.backends import ServicioNoDisponible, con_lenguaje, lenguaje_de
from services.citas_api import (
    actualizar_cita,
    crear_cita as crear_cita_api,
    obtener_cita,
)
from services.mascotas_api import obtener_mascota

from .forms import CitaForm


def _volver_a_citas(mascota_id, lenguaje):
    return redirect(
        con_lenguaje(
            reverse('citas_mascota', args=[mascota_id]),
            lenguaje
        )
    )


def crear_cita(request, mascota_id):

    lenguaje = lenguaje_de(request)
    error = None

    try:
        mascota = obtener_mascota(mascota_id, lenguaje)

    except ServicioNoDisponible as e:
        return render(
            request,
            'citas/crear_cita.html',
            {
                'form': CitaForm(),
                'mascota': {'id': mascota_id},
                'error': str(e)
            }
        )

    except Exception:
        return redirect('lista_mascotas')

    if request.method == 'POST':

        form = CitaForm(request.POST)

        if form.is_valid():

            datos = {
                'mascota_id': mascota_id,
                'fecha': form.cleaned_data['fecha'],
                'motivo': form.cleaned_data['motivo'],
                'estado': form.cleaned_data['estado'],
            }

            try:
                crear_cita_api(datos, lenguaje)

                return _volver_a_citas(mascota_id, lenguaje)

            except ServicioNoDisponible as e:
                error = str(e)

    else:
        form = CitaForm()

    return render(
        request,
        'citas/crear_cita.html',
        {
            'form': form,
            'mascota': mascota,
            'error': error
        }
    )


def editar_cita(request, mascota_id, cita_id):

    lenguaje = lenguaje_de(request)
    error = None

    try:
        mascota = obtener_mascota(mascota_id, lenguaje)
        cita = obtener_cita(cita_id, lenguaje)

    except ServicioNoDisponible as e:
        return render(
            request,
            'citas/editar_cita.html',
            {
                'form': None,
                'cita': None,
                'mascota': {'id': mascota_id},
                'error': str(e)
            }
        )

    except Exception:
        return _volver_a_citas(mascota_id, lenguaje)

    if request.method == 'POST':

        form = CitaForm(request.POST)

        if form.is_valid():

            datos = {
                'mascota_id': mascota_id,
                'fecha': form.cleaned_data['fecha'],
                'motivo': form.cleaned_data['motivo'],
                'estado': form.cleaned_data['estado'],
            }

            try:
                actualizar_cita(cita_id, datos, lenguaje)

                return _volver_a_citas(mascota_id, lenguaje)

            except ServicioNoDisponible as e:
                error = str(e)

    else:

        form = CitaForm(
            initial={
                'fecha': cita['fecha'],
                'motivo': cita['motivo'],
                'estado': cita['estado'],
            }
        )

    return render(
        request,
        'citas/editar_cita.html',
        {
            'form': form,
            'cita': cita,
            'mascota': mascota,
            'error': error
        }
    )
