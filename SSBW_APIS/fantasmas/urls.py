from django.contrib import admin
from . import views
from django.urls import path, include

urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("consulta", views.consulta, name="consulta"),
    path("buscar", views.buscar, name="buscar"),
    path("editar/<registro>", views.editar, name="editar"),
    path("borrar/<registro>", views.eliminar, name="eliminar"),
    path("detalle/<registro>", views.detalle, name="detalle"),
    path("aniadir", views.aniadir, name="aniadir")
]
