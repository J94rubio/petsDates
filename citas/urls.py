from django.urls import path

from . import views


urlpatterns = [

    path(
        'crear/',
        views.crear_cita,
        name='crear_cita'
    ),

    path(
        'editar/<int:cita_id>/',
        views.editar_cita,
        name='editar_cita'
    ),

]