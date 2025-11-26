from django.urls import path
from . import views

urlpatterns = [
    path('', views.scraper_home, name='scraper_home'),
    path('resultados/<int:busqueda_id>/', views.scraper_resultados, name='scraper_resultados'),
]
