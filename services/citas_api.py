import os

import requests


BASE_URL = os.environ.get(
    "CITAS_API_URL",
    "http://127.0.0.1:8002/api/citas"
).rstrip("/")


def listar_citas():
    """
    Obtiene todas las citas.
    """

    response = requests.get(
        f"{BASE_URL}/"
    )

    response.raise_for_status()

    return response.json()


def obtener_cita(cita_id):
    """
    Obtiene una cita por su ID.
    """

    response = requests.get(
        f"{BASE_URL}/{cita_id}"
    )

    response.raise_for_status()

    return response.json()


def listar_citas_mascota(mascota_id):
    """
    Obtiene todas las citas asociadas
    a una mascota específica.
    """

    response = requests.get(
        f"{BASE_URL}/mascota/{mascota_id}"
    )

    response.raise_for_status()

    return response.json()


def crear_cita(datos):
    datos = datos.copy()

    if hasattr(datos.get('fecha'), 'isoformat'):
        datos['fecha'] = datos['fecha'].isoformat()

    response = requests.post(
        f"{BASE_URL}/",
        json=datos
    )

    response.raise_for_status()

    return response.json()


def actualizar_cita(cita_id, datos):

    datos = datos.copy()

    if hasattr(datos.get('fecha'), 'isoformat'):
        datos['fecha'] = datos['fecha'].isoformat()

    response = requests.put(
        f"{BASE_URL}/{cita_id}",
        json=datos
    )

    response.raise_for_status()

    return response.json()

def eliminar_cita(cita_id):
    """
    Elimina una cita por su ID.
    """

    response = requests.delete(
        f"{BASE_URL}/{cita_id}"
    )

    response.raise_for_status()

    return True