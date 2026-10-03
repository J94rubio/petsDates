from .backends import solicitar


def _con_fecha_iso(datos):
    datos = datos.copy()

    if hasattr(datos.get('fecha'), 'isoformat'):
        datos['fecha'] = datos['fecha'].isoformat()

    return datos


def listar_citas(lenguaje=None):
    """
    Obtiene todas las citas.
    """

    return solicitar('citas', 'GET', '/', lenguaje).json()


def obtener_cita(cita_id, lenguaje=None):
    """
    Obtiene una cita por su ID.
    """

    return solicitar('citas', 'GET', f'/{cita_id}', lenguaje).json()


def listar_citas_mascota(mascota_id, lenguaje=None):
    """
    Obtiene todas las citas asociadas
    a una mascota específica.
    """

    return solicitar(
        'citas', 'GET', f'/mascota/{mascota_id}', lenguaje
    ).json()


def crear_cita(datos, lenguaje=None):

    return solicitar(
        'citas', 'POST', '/', lenguaje, json=_con_fecha_iso(datos)
    ).json()


def actualizar_cita(cita_id, datos, lenguaje=None):

    return solicitar(
        'citas', 'PUT', f'/{cita_id}', lenguaje, json=_con_fecha_iso(datos)
    ).json()


def eliminar_cita(cita_id, lenguaje=None):
    """
    Elimina una cita por su ID.
    """

    solicitar('citas', 'DELETE', f'/{cita_id}', lenguaje)

    return True
