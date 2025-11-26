from django.db import models
from django.contrib.auth.models import User


class BusquedaScraper(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    palabra_clave = models.CharField(max_length=200)
    fecha_busqueda = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-fecha_busqueda']
    
    def __str__(self):
        return f'{self.palabra_clave} - {self.fecha_busqueda}'


class ResultadoScraper(models.Model):
    busqueda = models.ForeignKey(BusquedaScraper, on_delete=models.CASCADE, related_name='resultados')
    titulo = models.CharField(max_length=500)
    descripcion = models.TextField(blank=True)
    url = models.URLField(max_length=1000)
    
    def __str__(self):
        return self.titulo

