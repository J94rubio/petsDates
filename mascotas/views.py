from django.shortcuts import redirect, render
from django.urls import reverse

from services.backends import ServicioNoDisponible, con_lenguaje, lenguaje_de
from services.citas_api import listar_citas_mascota
from services.mascotas_api import (
    crear_mascota as crear_mascota_api,
    listar_mascotas,
    obtener_mascota,
)

from .forms import MascotaForm


def lista_mascotas(request):

    lenguaje = lenguaje_de(request)

    try:
        mascotas = listar_mascotas(lenguaje)
        error = None

    except ServicioNoDisponible as e:
        mascotas = []
        error = str(e)

    return render(
        request,
        'mascotas/lista_mascotas.html',
        {
            'mascotas': mascotas,
            'error': error
        }
    )


def detalle_mascota(request, mascota_id):

    lenguaje = lenguaje_de(request)
    error = None

    try:
        mascota = obtener_mascota(mascota_id, lenguaje)

    except ServicioNoDisponible as e:
        mascota = None
        error = str(e)

    except Exception:
        mascota = None

    return render(
        request,
        'mascotas/detalle_mascota.html',
        {
            'mascota': mascota,
            'error': error
        }
    )


def citas_mascota(request, mascota_id):

    lenguaje = lenguaje_de(request)
    error = None

    try:
        mascota = obtener_mascota(mascota_id, lenguaje)
        citas = listar_citas_mascota(mascota_id, lenguaje)

    except ServicioNoDisponible as e:
        mascota = None
        citas = []
        error = str(e)

    except Exception:
        mascota = None
        citas = []

    return render(
        request,
        'mascotas/citas_mascota.html',
        {
            'mascota': mascota,
            'citas': citas,
            'error': error
        }
    )


def crear_mascota(request):

    lenguaje = lenguaje_de(request)
    error = None

    if request.method == 'POST':

        form = MascotaForm(request.POST)

        if form.is_valid():

            datos = {
                'nombre': form.cleaned_data['nombre'],
                'especie': form.cleaned_data['especie'],
                'raza': form.cleaned_data['raza'],
                'edad': form.cleaned_data['edad'],
                'propietario': form.cleaned_data['propietario'],
            }

            try:
                crear_mascota_api(datos, lenguaje)

                return redirect(
                    con_lenguaje(reverse('lista_mascotas'), lenguaje)
                )

            except ServicioNoDisponible as e:
                error = str(e)

    else:
        form = MascotaForm()

    return render(
        request,
        'mascotas/crear_mascota.html',
        {
            'form': form,
            'error': error
        }
    )
