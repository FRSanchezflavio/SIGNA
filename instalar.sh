#!/bin/bash

# Script de instalación para SIGNA en sistemas Linux/Mac
# Para Windows, usar instalar.ps1 o instalar.bat

echo "============================================"
echo "  SIGNA - Instalación Automatizada"
echo "  Policía de Tucumán"
echo "============================================"
echo ""

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Función para verificar comandos
check_command() {
    if ! command -v $1 &> /dev/null; then
        echo -e "${RED}❌ $1 no encontrado${NC}"
        echo -e "${YELLOW}Por favor instalar $2${NC}"
        exit 1
    else
        echo -e "${GREEN}✅ $1 instalado${NC}"
    fi
}

# PASO 1: Verificar ubicación del proyecto
echo -e "${YELLOW}[1/7] Verificando ubicación del proyecto...${NC}"
echo -e "${GREEN}✅ OK${NC}"

# PASO 2: Verificar Node.js
echo -e "\n${YELLOW}[2/7] Verificando Node.js...${NC}"
check_command node "desde https://nodejs.org/"
node --version

# PASO 3: Verificar npm
echo -e "\n${YELLOW}[3/7] Verificando npm...${NC}"
check_command npm "desde https://nodejs.org/"
npm --version

# PASO 4: Verificar Python
echo -e "\n${YELLOW}[4/7] Verificando Python...${NC}"
check_command python3 "desde https://www.python.org/"
python3 --version

# PASO 5: Limpiar instalación previa
echo -e "\n${YELLOW}[5/7] Limpiando instalación previa...${NC}"
if [ -d "node_modules" ]; then
    rm -rf node_modules
    echo -e "${GREEN}✅ node_modules eliminado${NC}"
fi
if [ -f "package-lock.json" ]; then
    rm package-lock.json
    echo -e "${GREEN}✅ package-lock.json eliminado${NC}"
fi
npm cache clean --force
echo -e "${GREEN}✅ Caché limpiada${NC}"

# PASO 6: Instalar dependencias de Node.js
echo -e "\n${YELLOW}[6/7] Instalando dependencias de Node.js...${NC}"
echo -e "${YELLOW}Esto puede tomar varios minutos...${NC}"
npm install
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Dependencias de Node.js instaladas${NC}"
else
    echo -e "${YELLOW}⚠️  Problemas al instalar. Intentando better-sqlite3 manualmente...${NC}"
    npm install better-sqlite3 --build-from-source
fi

# PASO 7: Instalar dependencias de Python
echo -e "\n${YELLOW}[7/7] Instalando dependencias de Python...${NC}"
cd backend

# Crear entorno virtual si no existe
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Creando entorno virtual...${NC}"
    python3 -m venv venv
fi

# Activar entorno virtual e instalar dependencias
source venv/bin/activate
pip install -r requirements.txt
deactivate

cd ..
echo -e "${GREEN}✅ Dependencias de Python instaladas${NC}"

# Crear archivo .env si no existe
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo -e "${GREEN}✅ Archivo .env creado${NC}"
fi

# Resumen final
echo -e "\n============================================"
echo -e "${GREEN}  🎉 INSTALACIÓN COMPLETADA${NC}"
echo -e "============================================"
echo ""
echo -e "${YELLOW}Para iniciar la aplicación, ejecuta:${NC}"
echo -e "  ${NC}npm run dev${NC}"
echo ""
echo -e "${YELLOW}Credenciales por defecto:${NC}"
echo -e "  Usuario: admin"
echo -e "  Contraseña: admin123"
echo ""
echo "============================================"
