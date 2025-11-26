from django.contrib import admin
from .models import BusquedaScraper, ResultadoScraper


class ResultadoScraperInline(admin.TabularInline):
    model = ResultadoScraper
    extra = 0


@admin.register(BusquedaScraper)
class BusquedaScraperAdmin(admin.ModelAdmin):
    list_display = ['palabra_clave', 'usuario', 'fecha_busqueda', 'cantidad_resultados']
    list_filter = ['fecha_busqueda']
    search_fields = ['palabra_clave', 'usuario__username']
    inlines = [ResultadoScraperInline]
    
    def cantidad_resultados(self, obj):
        return obj.resultados.count()
    cantidad_resultados.short_description = 'Resultados'


@admin.register(ResultadoScraper)
class ResultadoScraperAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'busqueda', 'url']
    search_fields = ['titulo', 'descripcion']

