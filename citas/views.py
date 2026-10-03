from django.shortcuts import render, redirect, get_object_or_404
from .forms import CitaForm
from .models import Cita
from mascotas.models import Mascota

from services.mascotas_api import obtener_mascota
from services.citas_api import crear_cita as crear_cita_api, obtener_cita, actualizar_cita


# def crear_cita(request, mascota_id):

#     mascota = get_object_or_404(
#         Mascota,
#         id=mascota_id
#     )

#     if request.method == 'POST':

#         form = CitaForm(request.POST)

#         if form.is_valid():

#             cita = form.save(commit=False)

#             cita.mascota = mascota

#             cita.save()

#             return redirect(
#                 'citas_mascota',
#                 mascota_id=mascota.id
#             )

#     else:

#         form = CitaForm()

#     return render(
#         request,
#         'citas/crear_cita.html',
#         {
#             'form': form,
#             'mascota': mascota
#         }
#     )

def crear_cita(request, mascota_id):

    try:
        mascota = obtener_mascota(mascota_id)
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

            crear_cita_api(datos)

            return redirect(
                'citas_mascota',
                mascota_id=mascota_id
            )

    else:
        form = CitaForm()

    return render(
        request,
        'citas/crear_cita.html',
        {
            'form': form,
            'mascota': mascota
        }
    )
    
# def editar_cita(request, mascota_id, cita_id):

#     cita = get_object_or_404(
#         Cita,
#         id=cita_id,
#         mascota_id=mascota_id
#     )

#     if request.method == 'POST':

#         form = CitaForm(
#             request.POST,
#             instance=cita
#         )

#         if form.is_valid():

#             form.save()

#             return redirect(
#                 'citas_mascota',
#                 mascota_id=mascota_id
#             )

#     else:

#         form = CitaForm(
#             instance=cita
#         )

#     return render(
#         request,
#         'citas/editar_cita.html',
#         {
#             'form': form,
#             'cita': cita
#         }
#     )

def editar_cita(request, mascota_id, cita_id):

    try:
        mascota = obtener_mascota(mascota_id)
        cita = obtener_cita(cita_id)

    except Exception:
        return redirect(
            'citas_mascota',
            mascota_id=mascota_id
        )

    if request.method == 'POST':

        form = CitaForm(request.POST)

        if form.is_valid():

            datos = {
                'mascota_id': mascota_id,
                'fecha': form.cleaned_data['fecha'],
                'motivo': form.cleaned_data['motivo'],
                'estado': form.cleaned_data['estado'],
            }

            actualizar_cita(
                cita_id,
                datos
            )

            return redirect(
                'citas_mascota',
                mascota_id=mascota_id
            )

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
            'mascota': mascota
        }
    )
