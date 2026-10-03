import os

import requests


BASE_URL = os.environ.get(
    "IA_API_URL",
    "http://127.0.0.1:8003/api/chat"
).rstrip("/")


def enviar_mensaje(
    mensaje,
    previous_interaction_id=None
):

    response = requests.post(
        f"{BASE_URL}/",
        json={
            "mensaje": mensaje,
            "previous_interaction_id": (
                previous_interaction_id
            )
        },
        timeout=240
    )

    if not response.ok:
        try:
            detalle = response.json().get("detail")
        except ValueError:
            detalle = None

        raise RuntimeError(
            detalle or f"El servicio de IA respondió {response.status_code}"
        )

    return response.json()