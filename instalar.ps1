# Script de PowerShell para Instalación Automatizada de SIGNA
# Ejecutar como Administrador

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  SIGNA - Script de Instalación Automatizada" -ForegroundColor Cyan
Write-Host "  Policía de Tucumán" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Verificar si se ejecuta como Administrador
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    Write-Host "⚠️  ADVERTENCIA: Este script debe ejecutarse como Administrador" -ForegroundColor Yellow
    Write-Host "   Click derecho en PowerShell → Ejecutar como Administrador" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Presiona Enter para salir"
    exit
}

# PASO 1: Verificar que no estamos en OneDrive
Write-Host "[1/8] Verificando ubicación del proyecto..." -ForegroundColor Yellow
$currentPath = Get-Location
if ($currentPath -like "*OneDrive*") {
    Write-Host "⚠️  El proyecto está en OneDrive. Moviendo a C:\Dev\SIGNA..." -ForegroundColor Yellow
    
    # Crear directorio de desarrollo
    New-Item -Path "C:\Dev" -ItemType Directory -Force | Out-Null
    
    # Intentar mover el proyecto
    try {
        Move-Item -Path $currentPath -Destination "C:\Dev\SIGNA" -Force -ErrorAction Stop
        Set-Location "C:\Dev\SIGNA"
        Write-Host "✅ Proyecto movido exitosamente a C:\Dev\SIGNA" -ForegroundColor Green
    } catch {
        Write-Host "❌ No se pudo mover automáticamente. Por favor:" -ForegroundColor Red
        Write-Host "   1. Pausar OneDrive (click derecho → Pausar sincronización)" -ForegroundColor Red
        Write-Host "   2. Copiar manualmente la carpeta SIGNA a C:\Dev\" -ForegroundColor Red
        Write-Host "   3. Ejecutar este script desde C:\Dev\SIGNA" -ForegroundColor Red
        Read-Host "Presiona Enter para salir"
        exit
    }
} else {
    Write-Host "✅ Ubicación del proyecto OK" -ForegroundColor Green
}

# PASO 2: Verificar Node.js
Write-Host "`n[2/8] Verificando Node.js..." -ForegroundColor Yellow
try {
    $nodeVersion = node --version
    Write-Host "✅ Node.js instalado: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Node.js no encontrado. Por favor instalar desde: https://nodejs.org/" -ForegroundColor Red
    Read-Host "Presiona Enter para salir"
    exit
}

# PASO 3: Verificar Python
Write-Host "`n[3/8] Verificando Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version
    Write-Host "✅ Python instalado: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python no encontrado. Por favor instalar desde: https://www.python.org/" -ForegroundColor Red
    Read-Host "Presiona Enter para salir"
    exit
}

# PASO 4: Verificar/Instalar Build Tools
Write-Host "`n[4/8] Verificando Visual Studio Build Tools..." -ForegroundColor Yellow
$buildToolsPath = "C:\Program Files\Microsoft Visual Studio\2022\BuildTools"
if (Test-Path $buildToolsPath) {
    Write-Host "✅ Build Tools detectadas" -ForegroundColor Green
} else {
    Write-Host "⚠️  Build Tools no detectadas" -ForegroundColor Yellow
    Write-Host "   Instalando windows-build-tools (esto tomará 10-15 minutos)..." -ForegroundColor Yellow
    npm install --global windows-build-tools
}

# PASO 5: Limpiar instalación previa
Write-Host "`n[5/8] Limpiando instalación previa..." -ForegroundColor Yellow
if (Test-Path "node_modules") {
    Remove-Item -Recurse -Force "node_modules" -ErrorAction SilentlyContinue
    Write-Host "✅ node_modules eliminado" -ForegroundColor Green
}
if (Test-Path "package-lock.json") {
    Remove-Item "package-lock.json" -ErrorAction SilentlyContinue
    Write-Host "✅ package-lock.json eliminado" -ForegroundColor Green
}

# Limpiar caché de npm
Write-Host "   Limpiando caché de npm..." -ForegroundColor Yellow
npm cache clean --force | Out-Null
Write-Host "✅ Caché limpiada" -ForegroundColor Green

# PASO 6: Instalar dependencias de Node.js
Write-Host "`n[6/8] Instalando dependencias de Node.js..." -ForegroundColor Yellow
Write-Host "   Esto puede tomar varios minutos..." -ForegroundColor Yellow
npm install
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Dependencias de Node.js instaladas" -ForegroundColor Green
} else {
    Write-Host "⚠️  Hubo problemas al instalar algunas dependencias" -ForegroundColor Yellow
    Write-Host "   Intentando instalar better-sqlite3 manualmente..." -ForegroundColor Yellow
    npm install better-sqlite3 --build-from-source
}

# PASO 7: Instalar dependencias de Python
Write-Host "`n[7/8] Instalando dependencias de Python..." -ForegroundColor Yellow
Set-Location "backend"

# Crear entorno virtual si no existe
if (-not (Test-Path "venv")) {
    Write-Host "   Creando entorno virtual..." -ForegroundColor Yellow
    python -m venv venv
}

# Activar entorno virtual e instalar dependencias
Write-Host "   Instalando paquetes de Python..." -ForegroundColor Yellow
& ".\venv\Scripts\Activate.ps1"
pip install -r requirements.txt | Out-Null
deactivate

Set-Location ".."
Write-Host "✅ Dependencias de Python instaladas" -ForegroundColor Green

# PASO 8: Crear archivo .env si no existe
Write-Host "`n[8/8] Configurando archivo .env..." -ForegroundColor Yellow
if (-not (Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
    Write-Host "✅ Archivo .env creado" -ForegroundColor Green
} else {
    Write-Host "✅ Archivo .env ya existe" -ForegroundColor Green
}

# Resumen final
Write-Host "`n============================================" -ForegroundColor Cyan
Write-Host "  🎉 INSTALACIÓN COMPLETADA" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Para iniciar la aplicación, ejecuta:" -ForegroundColor Yellow
Write-Host "  npm run dev" -ForegroundColor White
Write-Host ""
Write-Host "Credenciales por defecto:" -ForegroundColor Yellow
Write-Host "  Usuario: admin" -ForegroundColor White
Write-Host "  Contraseña: admin123" -ForegroundColor White
Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan

Read-Host "`nPresiona Enter para salir"
