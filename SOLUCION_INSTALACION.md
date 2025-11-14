# 🔧 Guía de Solución de Problemas de Instalación

## ⚠️ Problemas Detectados

1. **Falta Visual Studio C++ Build Tools** (crítico)
2. **Archivos bloqueados por OneDrive** (EPERM errors)
3. **Dependencias deprecated** (warnings)

---

## 🚀 SOLUCIÓN PASO A PASO

### PASO 1: Mover el Proyecto Fuera de OneDrive

**IMPORTANTE**: OneDrive bloquea archivos de node_modules causando errores EPERM.

```powershell
# Abrir PowerShell como Administrador

# Crear carpeta de desarrollo
New-Item -Path C:\Dev -ItemType Directory -Force

# Mover el proyecto
Move-Item -Path "C:\Users\Usuario\OneDrive\Desktop\SIGNA" -Destination "C:\Dev\SIGNA" -Force

# Navegar al nuevo directorio
cd C:\Dev\SIGNA
```

**Alternativa si el comando falla:**
1. Pausar OneDrive (click derecho → Pausar sincronización → 2 horas)
2. Copiar manualmente la carpeta SIGNA a `C:\Dev\`
3. Trabajar desde `C:\Dev\SIGNA`

---

### PASO 2: Instalar Visual Studio Build Tools

**Opción A - Instalación Completa (Recomendada):**

1. Descargar Build Tools:
   - URL: https://visualstudio.microsoft.com/downloads/
   - Buscar: "Build Tools for Visual Studio 2022"
   - Descargar e instalar

2. Durante la instalación, seleccionar:
   - ✅ **Desktop development with C++**
   - ✅ MSVC v143 - VS 2022 C++ x64/x86 build tools
   - ✅ Windows 11 SDK (o Windows 10 SDK)
   - ✅ C++ CMake tools for Windows

3. **REINICIAR** la computadora después de la instalación

**Opción B - Instalación Rápida (Windows Build Tools):**

```powershell
# Ejecutar PowerShell como ADMINISTRADOR
npm install --global windows-build-tools
```

⏱️ Esto tomará 10-15 minutos. NO cerrar la ventana.

---

### PASO 3: Limpiar Instalación Previa

```powershell
# En C:\Dev\SIGNA

# Eliminar node_modules y package-lock.json
Remove-Item -Recurse -Force node_modules -ErrorAction SilentlyContinue
Remove-Item package-lock.json -ErrorAction SilentlyContinue

# Limpiar caché de npm
npm cache clean --force
```

---

### PASO 4: Actualizar package.json (Eliminar Warnings)

Reemplazar las dependencias deprecated con versiones actualizadas.

Ver archivo `package.json` actualizado en el proyecto.

---

### PASO 5: Reinstalar Dependencias

```powershell
# Verificar que Build Tools están instalados
npm config get msvs_version

# Instalar dependencias
npm install

# Si better-sqlite3 falla, instalarlo individualmente
npm install better-sqlite3 --build-from-source
```

---

### PASO 6: Instalar Backend Python

```powershell
# Navegar a backend
cd backend

# Crear entorno virtual (recomendado)
python -m venv venv

# Activar entorno virtual
.\venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Volver al directorio raíz
cd ..
```

---

## ✅ Verificación de Instalación

```powershell
# Verificar Node.js
node --version
# Debería mostrar: v22.12.0 o similar

# Verificar npm
npm --version
# Debería mostrar: 10.9.0 o similar

# Verificar Python
python --version
# Debería mostrar: Python 3.13.9 o similar

# Verificar que node_modules se instaló correctamente
Test-Path .\node_modules
# Debería mostrar: True

# Verificar better-sqlite3
npm list better-sqlite3
# No debería mostrar errores
```

---

## 🎯 Iniciar la Aplicación

```powershell
# Desde C:\Dev\SIGNA
npm run dev
```

La aplicación debería abrir automáticamente con:
- **Usuario:** admin
- **Contraseña:** admin123

---

## 🆘 Solución de Problemas Adicionales

### Error: "Cannot find module 'electron'"
```powershell
npm rebuild electron
```

### Error: "Python not found"
```powershell
# Configurar ruta de Python manualmente
npm config set python "C:\Users\Usuario\AppData\Local\Microsoft\WindowsApps\PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0\python.exe"
```

### Error: "Port 5000 already in use"
Editar `.env`:
```
PORT=5001
```

### Warnings de seguridad (npm audit)
```powershell
npm audit fix
# Si hay vulnerabilidades críticas:
npm audit fix --force
```

---

## 📝 Notas Importantes

1. **OneDrive**: NUNCA ejecutar `npm install` en carpetas sincronizadas con OneDrive
2. **Permisos**: Ejecutar PowerShell como Administrador para instalar Build Tools
3. **Antivirus**: Algunos antivirus bloquean node-gyp, desactivar temporalmente si es necesario
4. **Espacio en disco**: Necesitas ~2GB libres para node_modules

---

## 🔗 Enlaces Útiles

- Node-gyp en Windows: https://github.com/nodejs/node-gyp#on-windows
- Visual Studio Build Tools: https://visualstudio.microsoft.com/downloads/
- Better SQLite3: https://github.com/WiseLibs/better-sqlite3

---

## ✉️ Soporte

Si continúan los problemas:
1. Captura pantalla del error completo
2. Ejecuta: `npm run env-info > diagnostico.txt`
3. Envía el archivo de diagnóstico

**Desarrollado por Policía de Tucumán - Departamento de Inteligencia Criminal**
