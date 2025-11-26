from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import EmailMessage
from django.conf import settings
from .models import Alumno
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer


@login_required
def dashboard(request):
    alumnos = Alumno.objects.filter(usuario=request.user)
    return render(request, 'alumnos/dashboard.html', {'alumnos': alumnos})


@login_required
def crear_alumno(request):
    if request.method == 'POST':
        alumno = Alumno.objects.create(
            usuario=request.user,
            nombre=request.POST.get('nombre'),
            apellido=request.POST.get('apellido'),
            email=request.POST.get('email'),
            edad=request.POST.get('edad'),
            carrera=request.POST.get('carrera'),
            promedio=request.POST.get('promedio') or None
        )
        messages.success(request, f'Alumno {alumno.nombre} creado exitosamente.')
        return redirect('dashboard')
    
    return render(request, 'alumnos/crear_alumno.html')


@login_required
def editar_alumno(request, pk):
    alumno = get_object_or_404(Alumno, pk=pk, usuario=request.user)
    
    if request.method == 'POST':
        alumno.nombre = request.POST.get('nombre')
        alumno.apellido = request.POST.get('apellido')
        alumno.email = request.POST.get('email')
        alumno.edad = request.POST.get('edad')
        alumno.carrera = request.POST.get('carrera')
        alumno.promedio = request.POST.get('promedio') or None
        alumno.save()
        messages.success(request, 'Alumno actualizado exitosamente.')
        return redirect('dashboard')
    
    return render(request, 'alumnos/editar_alumno.html', {'alumno': alumno})


@login_required
def eliminar_alumno(request, pk):
    alumno = get_object_or_404(Alumno, pk=pk, usuario=request.user)
    nombre = str(alumno)
    alumno.delete()
    messages.success(request, f'Alumno {nombre} eliminado exitosamente.')
    return redirect('dashboard')


@login_required
def enviar_pdf_alumno(request, pk):
    alumno = get_object_or_404(Alumno, pk=pk, usuario=request.user)
    
    # Crear PDF
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()
    
    # Título
    title = Paragraph(f"<b>Información del Alumno</b>", styles['Title'])
    elements.append(title)
    elements.append(Spacer(1, 20))
    
    # Datos del alumno en tabla
    data = [
        ['Campo', 'Valor'],
        ['Nombre completo', f'{alumno.nombre} {alumno.apellido}'],
        ['Email', alumno.email],
        ['Edad', str(alumno.edad)],
        ['Carrera', alumno.carrera],
        ['Promedio', str(alumno.promedio) if alumno.promedio else 'N/A'],
        ['Fecha de registro', alumno.fecha_registro.strftime('%d/%m/%Y %H:%M')],
    ]
    
    table = Table(data, colWidths=[200, 300])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    
    elements.append(table)
    doc.build(elements)
    
    # Enviar email con PDF
    buffer.seek(0)
    email = EmailMessage(
        f'Información del alumno {alumno.nombre} {alumno.apellido}',
        f'Adjunto encontrarás el PDF con la información del alumno {alumno.nombre} {alumno.apellido}.',
        settings.DEFAULT_FROM_EMAIL,
        [request.user.email],
    )
    email.attach(f'alumno_{alumno.nombre}_{alumno.apellido}.pdf', buffer.getvalue(), 'application/pdf')
    
    try:
        email.send()
        messages.success(request, f'PDF enviado exitosamente a {request.user.email}')
    except Exception as e:
        messages.error(request, f'Error al enviar el correo: {str(e)}')
    
    return redirect('dashboard')

