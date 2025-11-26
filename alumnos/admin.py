from django.contrib import admin
from .models import Alumno


@admin.register(Alumno)
class AlumnoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'apellido', 'email', 'carrera', 'promedio', 'usuario', 'fecha_registro']
    list_filter = ['carrera', 'fecha_registro']
    search_fields = ['nombre', 'apellido', 'email']

