@echo off
echo ============================================
echo   SIGNA - Instalacion Automatizada
echo   Policia de Tucuman
echo ============================================
echo.

REM Verificar privilegios de administrador
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo ERROR: Este script debe ejecutarse como Administrador
    echo Click derecho en el archivo -^> Ejecutar como Administrador
    pause
    exit /b 1
)

echo [1/8] Verificando ubicacion del proyecto...
cd /d "%~dp0"
echo %cd% | findstr /C:"OneDrive" >nul
if %errorLevel% equ 0 (
    echo ADVERTENCIA: El proyecto esta en OneDrive
    echo Moviendo a C:\Dev\SIGNA...
    if not exist "C:\Dev" mkdir "C:\Dev"
    xcopy /E /I /Y "%~dp0" "C:\Dev\SIGNA"
    cd /d "C:\Dev\SIGNA"
    echo OK: Proyecto movido a C:\Dev\SIGNA
) else (
    echo OK: Ubicacion del proyecto correcta
)

echo.
echo [2/8] Verificando Node.js...
node --version >nul 2>&1
if %errorLevel% neq 0 (
    echo ERROR: Node.js no encontrado
    echo Por favor instalar desde: https://nodejs.org/
    pause
    exit /b 1
)
node --version
echo OK: Node.js instalado

echo.
echo [3/8] Verificando Python...
python --version >nul 2>&1
if %errorLevel% neq 0 (
    echo ERROR: Python no encontrado
    echo Por favor instalar desde: https://www.python.org/
    pause
    exit /b 1
)
python --version
echo OK: Python instalado

echo.
echo [4/8] Verificando Build Tools...
if exist "C:\Program Files\Microsoft Visual Studio\2022\BuildTools" (
    echo OK: Build Tools detectadas
) else (
    echo ADVERTENCIA: Build Tools no detectadas
    echo Instalando windows-build-tools...
    call npm install --global windows-build-tools
)

echo.
echo [5/8] Limpiando instalacion previa...
if exist "node_modules" (
    rd /s /q "node_modules"
    echo OK: node_modules eliminado
)
if exist "package-lock.json" (
    del /q "package-lock.json"
    echo OK: package-lock.json eliminado
)
call npm cache clean --force
echo OK: Cache limpiada

echo.
echo [6/8] Instalando dependencias de Node.js...
echo Esto puede tomar varios minutos...
call npm install
if %errorLevel% neq 0 (
    echo ADVERTENCIA: Problemas al instalar dependencias
    echo Intentando instalar better-sqlite3 manualmente...
    call npm install better-sqlite3 --build-from-source
)
echo OK: Dependencias de Node.js instaladas

echo.
echo [7/8] Instalando dependencias de Python...
cd backend
if not exist "venv" (
    echo Creando entorno virtual...
    python -m venv venv
)
call venv\Scripts\activate.bat
pip install -r requirements.txt
call deactivate
cd ..
echo OK: Dependencias de Python instaladas

echo.
echo [8/8] Configurando archivo .env...
if not exist ".env" (
    copy ".env.example" ".env"
    echo OK: Archivo .env creado
) else (
    echo OK: Archivo .env ya existe
)

echo.
echo ============================================
echo   INSTALACION COMPLETADA
echo ============================================
echo.
echo Para iniciar la aplicacion, ejecuta:
echo   npm run dev
echo.
echo Credenciales por defecto:
echo   Usuario: admin
echo   Contraseña: admin123
echo.
echo ============================================

pause
