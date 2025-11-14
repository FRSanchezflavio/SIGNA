-- SIGNA - Sistema de Inteligencia y Gestión de Análisis
-- Esquema de Base de Datos - PostgreSQL + PostGIS
-- Versión: 1.0
-- Fecha: Noviembre 2025

-- Activar extensión PostGIS para análisis geoespacial
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- =====================================================
-- TABLA: UNIDADES_REGIONALES
-- =====================================================
CREATE TABLE IF NOT EXISTS unidades_regionales (
    id_unidad_regional SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    codigo VARCHAR(10) NOT NULL UNIQUE,
    descripcion TEXT,
    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- TABLA: JURISDICCIONES
-- =====================================================
CREATE TABLE IF NOT EXISTS jurisdicciones (
    id_jurisdiccion SERIAL PRIMARY KEY,
    id_unidad_regional INTEGER NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    codigo VARCHAR(10) NOT NULL UNIQUE,
    limite_geom GEOMETRY(MULTIPOLYGON, 4326),
    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_unidad_regional) REFERENCES unidades_regionales(id_unidad_regional)
);

-- =====================================================
-- TABLA: DEPENDENCIAS (COMISARÍAS)
-- =====================================================
CREATE TABLE IF NOT EXISTS dependencias (
    id_dependencia SERIAL PRIMARY KEY,
    id_jurisdiccion INTEGER NOT NULL,
    nombre VARCHAR(150) NOT NULL,
    tipo VARCHAR(50),
    direccion VARCHAR(255),
    telefono VARCHAR(20),
    ubicacion GEOMETRY(POINT, 4326),
    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_jurisdiccion) REFERENCES jurisdicciones(id_jurisdiccion)
);

-- =====================================================
-- TABLA: TIPOS_DELITO
-- =====================================================
CREATE TABLE IF NOT EXISTS tipos_delito (
    id_tipo_delito SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    codigo VARCHAR(20),
    categoria VARCHAR(50),
    descripcion TEXT,
    color VARCHAR(7),
    activo BOOLEAN DEFAULT TRUE
);

-- =====================================================
-- TABLA: USUARIOS
-- =====================================================
CREATE TABLE IF NOT EXISTS usuarios (
    id_usuario SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    rol VARCHAR(20) NOT NULL CHECK(rol IN ('ADMINISTRADOR', 'ANALISTA_SENIOR', 'ANALISTA_JUNIOR', 'CONSULTA')),
    id_dependencia INTEGER,
    activo BOOLEAN DEFAULT TRUE,
    ultimo_acceso TIMESTAMP,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_dependencia) REFERENCES dependencias(id_dependencia)
);

-- =====================================================
-- TABLA: EVENTOS_DELICTIVOS (PRINCIPAL)
-- =====================================================
CREATE TABLE IF NOT EXISTS eventos_delictivos (
    id_evento SERIAL PRIMARY KEY,
    
    -- SECCIÓN A: INFORMACIÓN ADMINISTRATIVA
    numero_sumario VARCHAR(50) NOT NULL,
    id_jurisdiccion INTEGER NOT NULL,
    id_dependencia INTEGER NOT NULL,
    
    -- SECCIÓN B: DATOS TEMPORALES
    fecha_delito DATE NOT NULL,
    mes_delito VARCHAR(20) NOT NULL,
    dia_semana VARCHAR(15) NOT NULL,
    hora_delito TIME NOT NULL,
    franja_horaria VARCHAR(20) NOT NULL CHECK(franja_horaria IN ('MADRUGADA', 'MAÑANA', 'TARDE', 'NOCHE')),
    
    -- SECCIÓN C: INFORMACIÓN DEL LUGAR (PostGIS)
    direccion VARCHAR(255) NOT NULL,
    ubicacion GEOMETRY(POINT, 4326) NOT NULL,
    lugar_tipo VARCHAR(50) NOT NULL CHECK(lugar_tipo IN ('VÍA PÚBLICA', 'DOMICILIO PARTICULAR', 'COMERCIO', 'ENTIDAD BANCARIA', 'INSTITUCIÓN PÚBLICA', 'VEHÍCULO', 'OTRO')),
    lugar_detalle VARCHAR(255),
    
    -- SECCIÓN D: CARACTERÍSTICAS DEL DELITO
    id_tipo_delito INTEGER NOT NULL,
    modus_operandi VARCHAR(100),
    vehiculo_utilizado VARCHAR(50),
    vehiculo_descripcion VARCHAR(254),
    
    -- SECCIÓN E: ARMAS Y ELEMENTOS
    arma_utilizada VARCHAR(50),
    arma_detalle VARCHAR(255),
    elementos_sustraidos TEXT,
    elementos_detalle VARCHAR(255),
    
    -- SECCIÓN F: RESEÑA DEL HECHO
    resena_hecho VARCHAR(254) NOT NULL,
    resena_tsvector TSVECTOR,
    
    -- METADATOS
    usuario_registro INTEGER NOT NULL,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usuario_modificacion INTEGER,
    fecha_modificacion TIMESTAMP,
    archivos_adjuntos JSONB,
    
    FOREIGN KEY (id_jurisdiccion) REFERENCES jurisdicciones(id_jurisdiccion),
    FOREIGN KEY (id_dependencia) REFERENCES dependencias(id_dependencia),
    FOREIGN KEY (id_tipo_delito) REFERENCES tipos_delito(id_tipo_delito),
    FOREIGN KEY (usuario_registro) REFERENCES usuarios(id_usuario),
    FOREIGN KEY (usuario_modificacion) REFERENCES usuarios(id_usuario)
);

-- Trigger para actualización automática de búsqueda full-text
CREATE OR REPLACE FUNCTION eventos_resena_trigger() RETURNS trigger AS $$
BEGIN
  NEW.resena_tsvector :=
    to_tsvector('spanish', COALESCE(NEW.resena_hecho, '')) ||
    to_tsvector('spanish', COALESCE(NEW.vehiculo_descripcion, ''));
  RETURN NEW;
END
$$ LANGUAGE plpgsql;

CREATE TRIGGER tsvector_update BEFORE INSERT OR UPDATE
ON eventos_delictivos FOR EACH ROW EXECUTE FUNCTION eventos_resena_trigger();

-- =====================================================
-- TABLA: VICTIMAS
-- =====================================================
CREATE TABLE IF NOT EXISTS victimas (
    id_victima SERIAL PRIMARY KEY,
    id_evento INTEGER NOT NULL,
    apellido_nombre VARCHAR(150) NOT NULL,
    sexo VARCHAR(20) CHECK(sexo IN ('MASCULINO', 'FEMENINO', 'OTRO', 'NO CONSTA')),
    edad INTEGER,
    dni_encrypted BYTEA,
    direccion VARCHAR(255),
    FOREIGN KEY (id_evento) REFERENCES eventos_delictivos(id_evento) ON DELETE CASCADE
);

-- =====================================================
-- TABLA: DENUNCIANTES
-- =====================================================
CREATE TABLE IF NOT EXISTS denunciantes (
    id_denunciante SERIAL PRIMARY KEY,
    id_evento INTEGER NOT NULL,
    apellido_nombre VARCHAR(150),
    sexo VARCHAR(20) CHECK(sexo IN ('MASCULINO', 'FEMENINO', 'OTRO', 'NO CONSTA')),
    edad INTEGER,
    dni_encrypted BYTEA,
    direccion VARCHAR(255),
    vinculo_victima VARCHAR(50) CHECK(vinculo_victima IN ('ES LA MISMA PERSONA', 'FAMILIAR', 'AMIGO/CONOCIDO', 'VECINO', 'TESTIGO', 'OTRO', 'NO CONSTA')),
    FOREIGN KEY (id_evento) REFERENCES eventos_delictivos(id_evento) ON DELETE CASCADE
);

-- =====================================================
-- TABLA: CAUSANTES
-- =====================================================
CREATE TABLE IF NOT EXISTS causantes (
    id_causante SERIAL PRIMARY KEY,
    id_evento INTEGER NOT NULL,
    apellido_nombre_alias VARCHAR(200),
    sexo VARCHAR(20) CHECK(sexo IN ('MASCULINO', 'FEMENINO', 'OTRO', 'NO CONSTA')),
    edad INTEGER,
    dni_encrypted BYTEA,
    direccion VARCHAR(255),
    descripcion TEXT,
    situacion VARCHAR(50) CHECK(situacion IN ('DETENIDO', 'PRÓFUGO', 'IDENTIFICADO', 'NO IDENTIFICADO', 'FALLECIDO', 'NO CONSTA')),
    FOREIGN KEY (id_evento) REFERENCES eventos_delictivos(id_evento) ON DELETE CASCADE
);

-- =====================================================
-- TABLA: AUDITORIA_ACCIONES
-- =====================================================
CREATE TABLE IF NOT EXISTS auditoria_acciones (
    id_auditoria SERIAL PRIMARY KEY,
    id_usuario INTEGER NOT NULL,
    accion VARCHAR(50) NOT NULL CHECK(accion IN ('CREAR', 'EDITAR', 'ELIMINAR', 'EXPORTAR', 'LOGIN', 'LOGOUT')),
    id_evento_afectado INTEGER,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    detalles_cambio JSONB,
    direccion_ip INET,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario),
    FOREIGN KEY (id_evento_afectado) REFERENCES eventos_delictivos(id_evento)
);

-- =====================================================
-- TABLA: CAPAS_PERSONALIZADAS
-- =====================================================
CREATE TABLE IF NOT EXISTS capas_personalizadas (
    id_capa SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    tipo VARCHAR(50) NOT NULL,
    ruta_archivo VARCHAR(500),
    geometria GEOMETRY,
    estilo_json JSONB,
    visible BOOLEAN DEFAULT TRUE,
    orden_visualizacion INTEGER DEFAULT 0,
    fecha_importacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usuario_importacion INTEGER,
    FOREIGN KEY (usuario_importacion) REFERENCES usuarios(id_usuario)
);

-- =====================================================
-- ÍNDICES PARA OPTIMIZACIÓN
-- =====================================================
CREATE INDEX idx_eventos_fecha ON eventos_delictivos(fecha_delito);
CREATE INDEX idx_eventos_jurisdiccion ON eventos_delictivos(id_jurisdiccion);
CREATE INDEX idx_eventos_tipo_delito ON eventos_delictivos(id_tipo_delito);
CREATE INDEX idx_eventos_ubicacion ON eventos_delictivos USING GIST(ubicacion);
CREATE INDEX idx_eventos_resena_fts ON eventos_delictivos USING GIN(resena_tsvector);
CREATE INDEX idx_eventos_usuario ON eventos_delictivos(usuario_registro);
CREATE INDEX idx_victimas_evento ON victimas(id_evento);
CREATE INDEX idx_denunciantes_evento ON denunciantes(id_evento);
CREATE INDEX idx_causantes_evento ON causantes(id_evento);
CREATE INDEX idx_auditoria_usuario ON auditoria_acciones(id_usuario);
CREATE INDEX idx_auditoria_fecha ON auditoria_acciones(timestamp);
CREATE INDEX idx_jurisdicciones_geom ON jurisdicciones USING GIST(limite_geom);
CREATE INDEX idx_dependencias_ubicacion ON dependencias USING GIST(ubicacion);

-- =====================================================
-- INSERCIÓN DE DATOS INICIALES
-- =====================================================

-- Tipos de Delito
INSERT INTO tipos_delito (nombre, codigo, categoria, color) VALUES
('ROBO', 'ROB-001', 'CONTRA LA PROPIEDAD', '#FA8C16'),
('ROBO AGRAVADO', 'ROB-002', 'CONTRA LA PROPIEDAD', '#F5222D'),
('HURTO', 'HUR-001', 'CONTRA LA PROPIEDAD', '#FAAD14'),
('HOMICIDIO', 'HOM-001', 'CONTRA LA VIDA', '#820014'),
('ESTAFA', 'EST-001', 'CONTRA LA PROPIEDAD', '#722ED1'),
('189 BIS', '189BIS', 'CONTRA LA INTEGRIDAD SEXUAL', '#C41D7F'),
('ABIGEATO', 'ABI-001', 'CONTRA LA PROPIEDAD', '#52C41A'),
('OTRO', 'OTR-001', 'OTROS', '#8C8C8C');

-- Usuario Administrador por defecto (password: admin123)
-- Nota: El hash debe ser generado con bcrypt
INSERT INTO usuarios (username, password_hash, nombre, apellido, email, rol, activo) VALUES
('admin', '$2b$10$rqYvFzN1h5W5l5YzN1h5W5l5YzN1h5W5l5YzN1h5W5l5YzN1h5W5l', 'Administrador', 'Sistema', 'admin@policia.tucuman.gob.ar', 'ADMINISTRADOR', TRUE);

-- =====================================================
-- FUNCIONES ÚTILES POSTGIS
-- =====================================================

-- Función para buscar eventos dentro de un radio (km)
CREATE OR REPLACE FUNCTION eventos_en_radio(
    lat_centro DOUBLE PRECISION,
    lon_centro DOUBLE PRECISION,
    radio_km DOUBLE PRECISION
)
RETURNS TABLE(id_evento INTEGER, distancia_metros DOUBLE PRECISION) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        e.id_evento,
        ST_Distance(
            e.ubicacion::geography,
            ST_SetSRID(ST_MakePoint(lon_centro, lat_centro), 4326)::geography
        ) AS distancia_metros
    FROM eventos_delictivos e
    WHERE ST_DWithin(
        e.ubicacion::geography,
        ST_SetSRID(ST_MakePoint(lon_centro, lat_centro), 4326)::geography,
        radio_km * 1000
    )
    ORDER BY distancia_metros;
END;
$$ LANGUAGE plpgsql;

-- Función para búsqueda full-text en reseñas
CREATE OR REPLACE FUNCTION buscar_eventos_por_texto(termino_busqueda TEXT)
RETURNS TABLE(id_evento INTEGER, relevancia REAL) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        e.id_evento,
        ts_rank(e.resena_tsvector, plainto_tsquery('spanish', termino_busqueda)) AS relevancia
    FROM eventos_delictivos e
    WHERE e.resena_tsvector @@ plainto_tsquery('spanish', termino_busqueda)
    ORDER BY relevancia DESC;
END;
$$ LANGUAGE plpgsql;
