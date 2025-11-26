

Write-Host "🚀 Iniciando proyecto Django..." -ForegroundColor Green


Write-Host "`n📦 Activando entorno virtual..." -ForegroundColor Cyan
& "C:/Users/Usuario/OneDrive/Escritorio/parcial2programacion/.venv/Scripts/Activate.ps1"


Set-Location "C:\Users\Usuario\OneDrive\Escritorio\parcial2programacion"

Write-Host "`n✅ Entorno activado!" -ForegroundColor Green
Write-Host "`n🌐 Para iniciar el servidor, ejecuta:" -ForegroundColor Yellow
Write-Host "   python manage.py runserver" -ForegroundColor White

Write-Host "`n📝 Otras comandos útiles:" -ForegroundColor Yellow
Write-Host "   python manage.py createsuperuser  - Crear usuario admin" -ForegroundColor White
Write-Host "   python manage.py makemigrations   - Crear migraciones" -ForegroundColor White
Write-Host "   python manage.py migrate          - Aplicar migraciones" -ForegroundColor White

Write-Host "`n📂 URLs importantes:" -ForegroundColor Yellow
Write-Host "   http://127.0.0.1:8000/            - Página principal" -ForegroundColor White
Write-Host "   http://127.0.0.1:8000/admin/      - Panel admin" -ForegroundColor White
Write-Host "   http://127.0.0.1:8000/accounts/register/ - Registro" -ForegroundColor White
Write-Host "   http://127.0.0.1:8000/accounts/login/    - Login" -ForegroundColor White

Write-Host "`n🎯 El proyecto está listo!" -ForegroundColor Green
