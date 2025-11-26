from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import BusquedaScraper, ResultadoScraper
import requests
from bs4 import BeautifulSoup


@login_required
def scraper_home(request):
    if request.method == 'POST':
        palabra_clave = request.POST.get('palabra_clave')
        
        # Crear búsqueda
        busqueda = BusquedaScraper.objects.create(
            usuario=request.user,
            palabra_clave=palabra_clave
        )
        
        # Realizar scraping - Wikipedia para contenido educativo
        try:
            url = f'https://es.wikipedia.org/wiki/Especial:Buscar?search={palabra_clave}'
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Buscar resultados
            resultados_encontrados = []
            
            # Si hay una página directa
            if 'Especial:Buscar' not in response.url:
                titulo = soup.find('h1', {'id': 'firstHeading'})
                if titulo:
                    primer_parrafo = soup.find('p')
                    ResultadoScraper.objects.create(
                        busqueda=busqueda,
                        titulo=titulo.text.strip(),
                        descripcion=primer_parrafo.text.strip() if primer_parrafo else '',
                        url=response.url
                    )
                    resultados_encontrados.append({
                        'titulo': titulo.text.strip(),
                        'descripcion': primer_parrafo.text.strip() if primer_parrafo else '',
                        'url': response.url
                    })
            else:
                # Página de resultados
                resultados = soup.find_all('div', {'class': 'mw-search-result-heading'})[:5]
                
                for resultado in resultados:
                    link = resultado.find('a')
                    if link:
                        titulo_texto = link.get('title', link.text.strip())
                        href = 'https://es.wikipedia.org' + link.get('href', '')
                        
                        # Obtener descripción
                        parent = resultado.parent
                        descripcion_elem = parent.find('div', {'class': 'searchresult'})
                        descripcion = descripcion_elem.text.strip() if descripcion_elem else ''
                        
                        ResultadoScraper.objects.create(
                            busqueda=busqueda,
                            titulo=titulo_texto,
                            descripcion=descripcion,
                            url=href
                        )
                        resultados_encontrados.append({
                            'titulo': titulo_texto,
                            'descripcion': descripcion,
                            'url': href
                        })
            
            # Si no hay resultados, buscar en el contenido general
            if not resultados_encontrados:
                links = soup.find_all('a', href=True)[:5]
                for link in links:
                    if '/wiki/' in link['href'] and ':' not in link['href']:
                        titulo_texto = link.text.strip()
                        if titulo_texto and len(titulo_texto) > 3:
                            href = 'https://es.wikipedia.org' + link['href']
                            ResultadoScraper.objects.create(
                                busqueda=busqueda,
                                titulo=titulo_texto,
                                descripcion='Artículo relacionado encontrado',
                                url=href
                            )
                            resultados_encontrados.append({
                                'titulo': titulo_texto,
                                'descripcion': 'Artículo relacionado encontrado',
                                'url': href
                            })
            
            # Enviar resultados por correo
            if resultados_encontrados:
                mensaje = f'Resultados de búsqueda para: {palabra_clave}\n\n'
                for i, res in enumerate(resultados_encontrados, 1):
                    mensaje += f"{i}. {res['titulo']}\n"
                    mensaje += f"   {res['descripcion'][:200]}...\n"
                    mensaje += f"   URL: {res['url']}\n\n"
                
                try:
                    send_mail(
                        f'Resultados de scraping: {palabra_clave}',
                        mensaje,
                        settings.DEFAULT_FROM_EMAIL,
                        [request.user.email],
                        fail_silently=False,
                    )
                    messages.success(request, f'Se encontraron {len(resultados_encontrados)} resultados y se enviaron a tu correo.')
                except Exception as e:
                    messages.warning(request, f'Resultados encontrados pero no se pudo enviar el correo: {str(e)}')
            else:
                messages.info(request, 'No se encontraron resultados para la búsqueda.')
            
            return redirect('scraper_resultados', busqueda_id=busqueda.id)
            
        except Exception as e:
            messages.error(request, f'Error al realizar el scraping: {str(e)}')
            return redirect('scraper_home')
    
    busquedas_recientes = BusquedaScraper.objects.filter(usuario=request.user)[:5]
    return render(request, 'scraper/home.html', {'busquedas_recientes': busquedas_recientes})


@login_required
def scraper_resultados(request, busqueda_id):
    busqueda = BusquedaScraper.objects.get(id=busqueda_id, usuario=request.user)
    resultados = busqueda.resultados.all()
    return render(request, 'scraper/resultados.html', {
        'busqueda': busqueda,
        'resultados': resultados
    })

