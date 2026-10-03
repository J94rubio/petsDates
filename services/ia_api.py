import os

import requests

from .backends import solicitar


TIEMPO_LECTURA_IA = float(os.environ.get('IA_READ_TIMEOUT', '120'))


def enviar_mensaje(
    mensaje,
    previous_interaction_id=None
):

    try:
        respuesta = solicitar(
            'ia',
            'POST',
            '/',
            None,
            tiempo_lectura=TIEMPO_LECTURA_IA,
            json={
                "mensaje": mensaje,
                "previous_interaction_id": (
                    previous_interaction_id
                )
            }
        )

    except requests.HTTPError as error:
        try:
            detalle = error.response.json().get("detail")
        except ValueError:
            detalle = None

        raise RuntimeError(
            detalle
            or f"El servicio de IA respondió {error.response.status_code}"
        )

    return respuesta.json()
