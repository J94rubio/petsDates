import os

import requests


BASE_URL = os.environ.get(
    "MASCOTAS_API_URL",
    "http://127.0.0.1:8001/api/mascotas"
).rstrip("/")


def listar_mascotas():
    """
    Obtiene todas las mascotas.
    """

    response = requests.get(
        f"{BASE_URL}/"
    )

    response.raise_for_status()

    return response.json()


def obtener_mascota(mascota_id):
    """
    Obtiene una mascota por su ID.
    """

    response = requests.get(
        f"{BASE_URL}/{mascota_id}"
    )

    response.raise_for_status()

    return response.json()


def crear_mascota(datos):
    """
    Crea una nueva mascota.

    datos debe ser un diccionario.
    """

    response = requests.post(
        f"{BASE_URL}/",
        json=datos
    )

    response.raise_for_status()

    return response.json()


def actualizar_mascota(mascota_id, datos):
    """
    Actualiza una mascota existente.

    datos debe ser un diccionario con los campos
    que se desean modificar.
    """

    response = requests.put(
        f"{BASE_URL}/{mascota_id}",
        json=datos
    )

    response.raise_for_status()

    return response.json()


def eliminar_mascota(mascota_id):
    """
    Elimina una mascota por su ID.
    """

    response = requests.delete(
        f"{BASE_URL}/{mascota_id}"
    )

    response.raise_for_status()

    return True