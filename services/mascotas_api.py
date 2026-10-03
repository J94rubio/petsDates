from .backends import solicitar


def listar_mascotas(lenguaje=None):
    """
    Obtiene todas las mascotas.
    """

    return solicitar('mascotas', 'GET', '/', lenguaje).json()


def obtener_mascota(mascota_id, lenguaje=None):
    """
    Obtiene una mascota por su ID.
    """

    return solicitar('mascotas', 'GET', f'/{mascota_id}', lenguaje).json()


def crear_mascota(datos, lenguaje=None):
    """
    Crea una nueva mascota.

    datos debe ser un diccionario.
    """

    return solicitar('mascotas', 'POST', '/', lenguaje, json=datos).json()


def actualizar_mascota(mascota_id, datos, lenguaje=None):
    """
    Actualiza una mascota existente.

    datos debe ser un diccionario con los campos
    que se desean modificar.
    """

    return solicitar(
        'mascotas', 'PUT', f'/{mascota_id}', lenguaje, json=datos
    ).json()


def eliminar_mascota(mascota_id, lenguaje=None):
    """
    Elimina una mascota por su ID.
    """

    solicitar('mascotas', 'DELETE', f'/{mascota_id}', lenguaje)

    return True
