"""Registro, por petición, de qué lenguaje respondió cada llamada a los microservicios."""

import threading

NOMBRES = {
    'python': 'Python',
    'java': 'Java',
    'js': 'JavaScript',
    'go': 'Go',
}

_estado = threading.local()


def reiniciar_uso():
    _estado.usados = []


def registrar_uso(lenguaje, respaldo=False):
    usados = getattr(_estado, 'usados', None)

    if usados is None:
        usados = _estado.usados = []

    if all(u['clave'] != lenguaje for u in usados):
        usados.append({
            'clave': lenguaje,
            'nombre': NOMBRES[lenguaje],
            'respaldo': respaldo,
        })


def lenguajes_usados():
    return list(getattr(_estado, 'usados', []))


class ReiniciarUsoMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        reiniciar_uso()
        return self.get_response(request)


def contexto(request):
    return {'servido_por': lenguajes_usados()}
