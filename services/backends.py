"""Cliente común de los microservicios, con respaldo entre lenguajes.

Sin lenguaje (o con 'python') se usa el backend principal y, si no responde,
el siguiente: Python -> Java -> JavaScript -> Go. Con 'java', 'js' o 'go' se
llama solo a ese lenguaje y, si falla, se informa el error.
"""

import os

import requests

from .trazas import NOMBRES, registrar_uso

LENGUAJES = ('python', 'java', 'js', 'go')
ESTRICTOS = ('java', 'js', 'go')

SERVICIOS = {
    'mascotas': {
        'variable': 'MASCOTAS_API_URL',
        'ruta': '/api/mascotas',
        'puertos': {'python': 8001, 'java': 8101, 'js': 8201, 'go': 8301},
    },
    'citas': {
        'variable': 'CITAS_API_URL',
        'ruta': '/api/citas',
        'puertos': {'python': 8002, 'java': 8102, 'js': 8202, 'go': 8302},
    },
    'ia': {
        'variable': 'IA_API_URL',
        'ruta': '/api/chat',
        'puertos': {'python': 8003, 'java': 8103, 'js': 8203, 'go': 8303},
    },
}

# Una lectura puede repetirse en otro lenguaje; una escritura solo si la
# petición no llegó a procesarse (sin conexión o 502/503 del proxy).
ESTADOS_LECTURA = {500, 502, 503, 504}
ESTADOS_ESCRITURA = {502, 503}

TIEMPO_CONEXION = float(os.environ.get('BACKEND_CONNECT_TIMEOUT', '5'))
TIEMPO_LECTURA = float(os.environ.get('BACKEND_READ_TIMEOUT', '15'))


class ServicioNoDisponible(Exception):
    """Ningún lenguaje pudo atender la petición."""


def normalizar_lenguaje(valor):
    valor = (valor or '').strip().lower()
    return valor if valor in LENGUAJES else 'python'


def lenguaje_de(request):
    """Lenguaje elegido con el botón pulsado (?lang= o campo lang del formulario)."""
    return normalizar_lenguaje(request.POST.get('lang') or request.GET.get('lang'))


def con_lenguaje(url, lenguaje):
    """Añade ?lang= solo cuando se eligió un lenguaje concreto."""
    return f'{url}?lang={lenguaje}' if lenguaje in ESTRICTOS else url


def url_base(servicio, lenguaje):
    datos = SERVICIOS[servicio]
    nombre = datos['variable']

    if lenguaje != 'python':
        nombre = f'{nombre}_{lenguaje.upper()}'

    por_defecto = f"http://127.0.0.1:{datos['puertos'][lenguaje]}{datos['ruta']}"

    return (os.environ.get(nombre) or por_defecto).rstrip('/')


def solicitar(servicio, metodo, ruta, lenguaje=None, tiempo_lectura=None, **kwargs):
    lenguaje = normalizar_lenguaje(lenguaje)
    estricto = lenguaje in ESTRICTOS
    orden = [lenguaje] if estricto else list(LENGUAJES)

    es_lectura = metodo.upper() == 'GET'
    estados_fallo = ESTADOS_LECTURA if es_lectura else ESTADOS_ESCRITURA
    tiempo_lectura = tiempo_lectura or TIEMPO_LECTURA

    errores = []

    for actual in orden:
        nombre = NOMBRES[actual]
        url = f'{url_base(servicio, actual)}{ruta}'

        try:
            respuesta = requests.request(
                metodo,
                url,
                timeout=(TIEMPO_CONEXION, tiempo_lectura),
                **kwargs
            )

        except requests.ConnectionError:
            errores.append(f'{nombre}: sin conexión')
            continue

        except requests.Timeout:
            errores.append(f'{nombre}: tiempo de espera agotado')

            if not es_lectura:
                break

            continue

        if respuesta.status_code in estados_fallo:
            errores.append(f'{nombre}: respondió {respuesta.status_code}')
            continue

        respuesta.raise_for_status()

        registrar_uso(actual, respaldo=not estricto and actual != 'python')

        return respuesta

    raise ServicioNoDisponible(
        f'El servicio de {servicio} no respondió ({"; ".join(errores)}).'
    )
