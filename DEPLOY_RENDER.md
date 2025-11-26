# ☁️ GUÍA COMPLETA DE DEPLOYMENT EN RENDER

## 📋 PRE-REQUISITOS

- [ ] Cuenta en GitHub
- [ ] Cuenta en Render (https://render.com)
- [ ] Código probado localmente
- [ ] Cuenta de Gmail para emails (con contraseña de aplicación)

---

## 📦 PASO 1: PREPARAR REPOSITORIO DE GITHUB

### 1.1 Inicializar Git (si no lo has hecho)

```powershell
cd C:\Users\Usuario\OneDrive\Escritorio\parcial2programacion
git init
git add .
git commit -m "Proyecto Django completo - Gestión de Alumnos"
```

### 1.2 Crear repositorio en GitHub

1. Ve a https://github.com/new
2. Nombre del repositorio: `proyecto-alumnos-django` (o el que prefieras)
3. Descripción: "Sistema de gestión de alumnos con Django"
4. **NO** inicialices con README, .gitignore o licencia
5. Haz clic en "Create repository"

### 1.3 Subir código a GitHub

```powershell
git remote add origin https://github.com/TU-USUARIO/proyecto-alumnos-django.git
git branch -M main
git push -u origin main
```

---

## 🗄️ PASO 2: CREAR BASE DE DATOS POSTGRESQL EN RENDER

### 2.1 Crear PostgreSQL Database

1. Ve a https://dashboard.render.com
2. Haz clic en **"New +"** → **"PostgreSQL"**

### 2.2 Configurar base de datos

```
Name: parcial2-db
Database: parcial2_db
User: parcial2_user
Region: Oregon (US West) - o el más cercano
PostgreSQL Version: 15 o superior
Plan: Free
```

3. Haz clic en **"Create Database"**
4. **IMPORTANTE**: Guarda las credenciales (aparecen en "Connections")

### 2.3 Credenciales importantes

Render te dará:
```
Internal Database URL
External Database URL
PSQL Command
Host
Port
Database
Username
Password
```

**NO necesitas copiarlas manualmente**, Render las configurará automáticamente.

---

## 🌐 PASO 3: CREAR WEB SERVICE EN RENDER

### 3.1 Crear nuevo Web Service

1. En Render Dashboard, clic en **"New +"** → **"Web Service"**
2. Conecta tu cuenta de GitHub si no lo has hecho
3. Busca y selecciona tu repositorio `proyecto-alumnos-django`

### 3.2 Configuración básica

```
Name: parcial2-alumnos
Region: Oregon (US West) - mismo que la BD
Branch: main
Root Directory: (dejar vacío)
Runtime: Python 3
```

### 3.3 Build & Start Commands

```
Build Command: ./build.sh
Start Command: gunicorn parcial2.wsgi:application
```

### 3.4 Plan

```
Instance Type: Free
```

---

## 🔐 PASO 4: CONFIGURAR VARIABLES DE ENTORNO

### 4.1 En la sección "Environment" del Web Service, agregar:

#### Variables básicas:

```
DEBUG
False
```

```
ALLOWED_HOSTS
tu-app.onrender.com
```

⚠️ **IMPORTANTE**: Reemplaza `tu-app.onrender.com` con el nombre real de tu app.
Ejemplo: Si tu app se llama `parcial2-alumnos`, será `parcial2-alumnos.onrender.com`

#### Variables de Django:

```
SECRET_KEY
[generar-una-clave-segura]
```

**Para generar SECRET_KEY**, abre Python y ejecuta:
```python
import secrets
print(secrets.token_urlsafe(50))
```
Copia el resultado.

#### Variables de Email (Gmail):

```
EMAIL_HOST
smtp.gmail.com
```

```
EMAIL_PORT
587
```

```
EMAIL_HOST_USER
tu-email@gmail.com
```

```
EMAIL_HOST_PASSWORD
xxxx xxxx xxxx xxxx
```

⚠️ **IMPORTANTE**: Usa la contraseña de aplicación de Gmail, NO tu contraseña normal.

**Obtener contraseña de aplicación**:
1. Ve a https://myaccount.google.com/apppasswords
2. Crea una contraseña para "Correo" → "Otro (Django)"
3. Copia la contraseña de 16 caracteres

```
DEFAULT_FROM_EMAIL
tu-email@gmail.com
```

### 4.2 Conectar PostgreSQL

Render automáticamente agregará estas variables (NO las agregues manualmente):
- `DATABASE_URL`
- `PGDATABASE`
- `PGHOST`
- `PGPASSWORD`
- `PGPORT`
- `PGUSER`

Para conectarlas:
1. En el Web Service, ve a la pestaña **"Environment"**
2. Busca la sección **"Add Environment Variable"**
3. Haz clic en **"Add from Database"**
4. Selecciona tu base de datos `parcial2-db`
5. Render automáticamente agregará todas las variables

---

## 🚀 PASO 5: DEPLOY

### 5.1 Iniciar deployment

1. Después de configurar todo, haz clic en **"Create Web Service"**
2. Render comenzará a:
   - Clonar tu repositorio
   - Instalar dependencias (`pip install -r requirements.txt`)
   - Ejecutar `./build.sh`:
     - Recolectar archivos estáticos
     - Ejecutar migraciones
   - Iniciar Gunicorn

### 5.2 Monitorear el deploy

- Verás los logs en tiempo real
- El proceso toma 2-5 minutos
- Busca el mensaje: `Your service is live 🎉`

### 5.3 URL de tu aplicación

Render te dará una URL como:
```
https://parcial2-alumnos.onrender.com
```

---

## 👤 PASO 6: CREAR SUPERUSUARIO EN PRODUCCIÓN

### 6.1 Abrir Shell de Render

1. En tu Web Service, ve a la pestaña **"Shell"**
2. Haz clic en **"Launch Shell"**

### 6.2 Crear superusuario

```bash
python manage.py createsuperuser
```

Sigue las instrucciones:
- Username: `admin`
- Email: `tu-email@gmail.com`
- Password: `tu-password-seguro`

---

## ✅ PASO 7: VERIFICAR FUNCIONAMIENTO

### 7.1 Probar la aplicación

1. **Página principal**: `https://tu-app.onrender.com`
2. **Registro**: `https://tu-app.onrender.com/accounts/register/`
3. **Login**: `https://tu-app.onrender.com/accounts/login/`
4. **Admin**: `https://tu-app.onrender.com/admin/`

### 7.2 Probar funcionalidades

- [ ] Registrar un usuario → Verificar email de bienvenida
- [ ] Crear alumnos
- [ ] Generar y enviar PDF → Verificar email
- [ ] Probar scraper → Verificar email con resultados
- [ ] Acceder al admin

---

## 🔄 PASO 8: ACTUALIZAR LA APLICACIÓN

### 8.1 Hacer cambios localmente

```powershell
# Editar archivos
git add .
git commit -m "Descripción de cambios"
git push
```

### 8.2 Deploy automático

Render detecta los cambios en GitHub y automáticamente:
1. Descarga los nuevos cambios
2. Ejecuta `./build.sh`
3. Reinicia el servicio

---

## 📊 MONITOREO Y MANTENIMIENTO

### Ver logs

1. En Render Dashboard → Tu Web Service
2. Pestaña **"Logs"**
3. Verás todos los logs en tiempo real

### Ver emails enviados

Los emails se enviarán realmente a las direcciones configuradas.
Verifica tu bandeja de entrada.

### Ver estado de la base de datos

1. En Render Dashboard → Tu PostgreSQL Database
2. Pestaña **"Info"**
3. Verás métricas y estado

---

## ⚠️ SOLUCIÓN DE PROBLEMAS EN PRODUCCIÓN

### ❌ Error 500 - Internal Server Error

**Solución**:
1. Revisa los logs en Render
2. Verifica que `DEBUG=False`
3. Verifica que `ALLOWED_HOSTS` esté configurado correctamente
4. Revisa que todas las variables de entorno estén configuradas

### ❌ Archivos estáticos no se cargan (CSS, JS)

**Solución**:
1. Verifica que `./build.sh` se ejecutó correctamente
2. En Shell de Render, ejecuta:
```bash
python manage.py collectstatic --no-input
```

### ❌ Error de base de datos

**Solución**:
1. Verifica que la base de datos PostgreSQL esté corriendo
2. Verifica que las variables de la BD estén conectadas
3. En Shell de Render:
```bash
python manage.py migrate
```

### ❌ Emails no se envían

**Solución**:
1. Verifica las variables de email en Environment
2. Verifica que usas contraseña de aplicación de Gmail
3. Verifica los logs para ver errores de SMTP

### ❌ Build falla

**Solución**:
1. Verifica que `build.sh` tenga permisos de ejecución
2. Si el error persiste, en Build Command usa:
```bash
pip install -r requirements.txt && python manage.py collectstatic --no-input && python manage.py migrate
```

---

## 💰 COSTOS

### Plan Free de Render:

```
✅ Web Service: Gratis
   - 750 horas/mes
   - Duerme después de 15 min de inactividad
   - Despierta automáticamente al recibir tráfico

✅ PostgreSQL: Gratis
   - 90 días gratis
   - 1 GB de almacenamiento
   - Después: $7/mes o migrar a otro servicio
```

### Alternativas después de 90 días:

1. **Pagar PostgreSQL en Render** ($7/mes)
2. **Usar Neon** (PostgreSQL gratis) - https://neon.tech
3. **Usar Supabase** (PostgreSQL gratis) - https://supabase.com
4. **Migrar a Railway** (plan free similar) - https://railway.app

---

## 🎯 CHECKLIST DE DEPLOYMENT

- [ ] Código subido a GitHub
- [ ] PostgreSQL creado en Render
- [ ] Web Service creado
- [ ] Build command: `./build.sh`
- [ ] Start command: `gunicorn parcial2.wsgi:application`
- [ ] Variable `DEBUG=False` configurada
- [ ] Variable `ALLOWED_HOSTS` configurada
- [ ] Variable `SECRET_KEY` generada y configurada
- [ ] Variables de email configuradas
- [ ] Base de datos conectada
- [ ] Deploy exitoso
- [ ] Superusuario creado
- [ ] Funcionalidades probadas

---

## 📱 COMPARTIR TU PROYECTO

Una vez deployado, puedes compartir tu URL:

```
🌐 Mi proyecto: https://parcial2-alumnos.onrender.com
👤 Usuario demo: estudiante1
🔑 Password demo: mipassword123
```

---

## 🎓 TIPS PARA LA PRESENTACIÓN

1. **Ten varios alumnos creados** antes de presentar
2. **Ten búsquedas del scraper** en el historial
3. **Acceso rápido al admin** para mostrar el backend
4. **Email configurado** para demostrar envíos en tiempo real
5. **Logs abiertos en Render** para mostrar actividad

---

## 🚀 ¡LISTO PARA PRODUCCIÓN!

Siguiendo estos pasos, tu proyecto estará:

✅ Accesible desde cualquier parte del mundo
✅ Con base de datos PostgreSQL profesional
✅ Enviando emails reales
✅ Con archivos estáticos servidos correctamente
✅ Listo para presentar

**¡Éxito con tu parcial!** 🎉
