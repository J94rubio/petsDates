from django.shortcuts import render, get_object_or_404, redirect

from .models import Mascota
from .forms import MascotaForm
from services.mascotas_api import (
    listar_mascotas,
    obtener_mascota,
    crear_mascota as crear_mascota_api
) 

from services.citas_api import listar_citas_mascota


def lista_mascotas(request):
    # mascotas = Mascota.objects.all()
    mascotas = listar_mascotas()

    return render(
        request,
        'mascotas/lista_mascotas.html',
        {'mascotas': mascotas}
    )

def detalle_mascota(request, mascota_id):
    # mascota = get_object_or_404(
    #     Mascota,
    #     id=mascota_id
    # )
    
    try:
        mascota = obtener_mascota(mascota_id)
    except Exception:
        return render(
            request,
            'mascotas/detalle_mascota.html',
            {'mascota': None}
        )

    return render(
        request,
        'mascotas/detalle_mascota.html',
        {'mascota': mascota}
    )


# def citas_mascota(request, mascota_id):

#     mascota = get_object_or_404(
#         Mascota,
#         id=mascota_id
#     )

#     citas = mascota.citas.all().order_by('fecha')

#     return render(
#         request,
#         'mascotas/citas_mascota.html',
#         {
#             'mascota': mascota,
#             'citas': citas
#         }
#     )

def citas_mascota(request, mascota_id):

    try:
        mascota = obtener_mascota(mascota_id)
        citas = listar_citas_mascota(mascota_id)

    except Exception:
        return render(
            request,
            'mascotas/citas_mascota.html',
            {
                'mascota': None,
                'citas': []
            }
        )

    return render(
        request,
        'mascotas/citas_mascota.html',
        {
            'mascota': mascota,
            'citas': citas
        }
    )
    
# def crear_mascota(request):

#     if request.method == 'POST':

#         form = MascotaForm(request.POST)

#         if form.is_valid():
#             form.save()

#             return redirect('lista_mascotas')

#     else:

#         form = MascotaForm()

#     return render(
#         request,
#         'mascotas/crear_mascota.html',
#         {'form': form}
#     )

def crear_mascota(request):

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

            crear_mascota_api(datos)

            return redirect('lista_mascotas')

    else:
        form = MascotaForm()

    return render(
        request,
        'mascotas/crear_mascota.html',
        {'form': form}
    )