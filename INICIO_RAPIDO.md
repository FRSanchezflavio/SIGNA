# SIGNA - Guía de Inicio Rápido

## 🚀 Instalación

### 1. Instalar Dependencias

```bash
# Instalar dependencias de Node.js
npm install

# Instalar dependencias de Python
cd backend
pip install -r requirements.txt
cd ..
```

### 2. Configurar Variables de Entorno

```bash
# Copiar archivo de ejemplo
cp .env.example .env

# Editar .env con tu configuración
# (Por defecto, usa SQLite - no requiere configuración adicional)
```

### 3. Iniciar la Aplicación

```bash
# Modo desarrollo (recomendado para primera vez)
npm run dev
```

La aplicación se abrirá automáticamente con:

- **Usuario:** admin
- **Contraseña:** admin123

## 📁 Estructura del Proyecto

```
SIGNA/
├── src/
│   ├── main/              # Electron (proceso principal)
│   └── renderer/          # React (interfaz de usuario)
├── backend/               # API Python Flask
├── database/              # Esquemas SQL
├── public/                # Recursos estáticos
└── config/                # Configuraciones
```

## 🛠️ Comandos Disponibles

```bash
npm run dev              # Iniciar todo (Frontend + Backend + Electron)
npm run dev:renderer     # Solo frontend
npm run dev:backend      # Solo backend API
npm run build            # Compilar para producción
npm run package:win      # Crear instalador Windows
```

## 📝 Próximos Pasos

1. **Cambiar contraseña del admin** (recomendado)
2. **Crear usuarios** con roles apropiados
3. **Configurar BD PostgreSQL** (opcional, para uso departamental)
4. **Importar datos históricos** (si existen)
5. **Personalizar capas del mapa**

## ❓ Problemas Comunes

### Error: "No se encuentra Python"

- Asegúrese de tener Python 3.8+ instalado
- Agregue Python al PATH del sistema

### Error: "Puerto 5000 en uso"

- Cambie el puerto en `.env`: `PORT=5001`

### El mapa no se carga

- Verifique conexión a Internet
- Compruebe que Leaflet CSS se cargó correctamente

## 📞 Soporte

Para soporte técnico, contacte:

- Email: soporte.signa@policia.tucuman.gob.ar
- Interno: 1234

---

**Desarrollado por Policía de Tucumán - Departamento de Inteligencia Criminal**
