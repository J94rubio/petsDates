from django.http import JsonResponse
from django.shortcuts import render

from services.ia_api import enviar_mensaje
from services.trazas import lenguajes_usados


def chat_veterinario(request):

    if request.method == 'GET':
        return render(
            request,
            'chat/chat.html'
        )

    if request.method == 'POST':

        mensaje = request.POST.get(
            'mensaje',
            ''
        ).strip()

        if not mensaje:

            return JsonResponse(
                {
                    'error': 'El mensaje no puede estar vacío.'
                },
                status=400
            )

        try:

            previous_interaction_id = request.session.get(
                'chat_interaction_id'
            )

            resultado = enviar_mensaje(
                mensaje,
                previous_interaction_id
            )

            request.session[
                'chat_interaction_id'
            ] = resultado['interaction_id']

            usados = lenguajes_usados()

            return JsonResponse(
                {
                    'respuesta': resultado['respuesta'],
                    'interaction_id': resultado['interaction_id'],
                    'servido_por': usados[0] if usados else None
                }
            )

        except Exception as e:

            return JsonResponse(
                {
                    'error': str(e)
                },
                status=500
            )

    return JsonResponse(
        {
            'error': 'Método no permitido.'
        },
        status=405
    )