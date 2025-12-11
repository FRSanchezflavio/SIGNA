"""
SIGNA - Sistema de Inteligencia y Gestión de Análisis
Backend API - Módulo de Inteligencia Avanzada (MIA)
Flask Application
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import zipfile
import tempfile
import shutil
import geopandas as gpd
from dotenv import load_dotenv

# Importar servicios
from services.analisis_predictivo import AnalisisPredictivo
from services.analisis_correlaciones import AnalisisCorrelaciones
from services.comparador_periodos import ComparadorPeriodos
from services.busqueda_inteligente import BusquedaInteligente

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configuración
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'signa-dev-key-2025')
app.config['DEBUG'] = os.getenv('DEBUG', 'True') == 'True'

# Servicios
analisis_predictivo = AnalisisPredictivo()
analisis_correlaciones = AnalisisCorrelaciones()
comparador_periodos = ComparadorPeriodos()
busqueda_inteligente = BusquedaInteligente()


@app.route('/health', methods=['GET'])
def health_check():
    """Verificación de estado del servidor"""
    return jsonify({
        'status': 'online',
        'service': 'SIGNA Backend API',
        'version': '1.0.0'
    }), 200


@app.route('/api/mia/tendencias', methods=['POST'])
def obtener_tendencias():
    """
    Analiza tendencias delictivas
    Body: { jurisdiccion_id, tipo_delito_id, dias_horizonte }
    """
    try:
        data = request.get_json()
        resultado = analisis_predictivo.calcular_tendencias(
            jurisdiccion_id=data.get('jurisdiccion_id'),
            tipo_delito_id=data.get('tipo_delito_id'),
            dias_horizonte=data.get('dias_horizonte', 30)
        )
        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/mia/proyecciones', methods=['POST'])
def obtener_proyecciones():
    """
    Calcula proyecciones delictivas
    Body: { jurisdiccion_id, tipo_delito_id, periodos_futuro }
    """
    try:
        data = request.get_json()
        resultado = analisis_predictivo.calcular_proyecciones(
            jurisdiccion_id=data.get('jurisdiccion_id'),
            tipo_delito_id=data.get('tipo_delito_id'),
            periodos_futuro=data.get('periodos_futuro', 12)
        )
        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/mia/hotspots', methods=['POST'])
def identificar_hotspots():
    """
    Identifica hotspots delictivos
    Body: { jurisdiccion_id, tipo_delito_id, fecha_inicio, fecha_fin }
    """
    try:
        data = request.get_json()
        resultado = analisis_predictivo.identificar_hotspots(
            jurisdiccion_id=data.get('jurisdiccion_id'),
            tipo_delito_id=data.get('tipo_delito_id'),
            fecha_inicio=data.get('fecha_inicio'),
            fecha_fin=data.get('fecha_fin')
        )
        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/mia/correlaciones', methods=['POST'])
def calcular_correlaciones():
    """
    Analiza correlaciones entre variables
    Body: { variable_x, variable_y, jurisdiccion_id, fecha_inicio, fecha_fin }
    """
    try:
        data = request.get_json()
        resultado = analisis_correlaciones.calcular_correlacion(
            variable_x=data.get('variable_x'),
            variable_y=data.get('variable_y'),
            jurisdiccion_id=data.get('jurisdiccion_id'),
            fecha_inicio=data.get('fecha_inicio'),
            fecha_fin=data.get('fecha_fin')
        )
        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/mia/correlaciones/matriz', methods=['POST'])
def obtener_matriz_correlaciones():
    """
    Genera matriz de correlaciones múltiples
    Body: { variables[], jurisdiccion_id, fecha_inicio, fecha_fin }
    """
    try:
        data = request.get_json()
        resultado = analisis_correlaciones.generar_matriz(
            variables=data.get('variables', []),
            jurisdiccion_id=data.get('jurisdiccion_id'),
            fecha_inicio=data.get('fecha_inicio'),
            fecha_fin=data.get('fecha_fin')
        )
        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/mia/comparacion/periodos', methods=['POST'])
def comparar_periodos():
    """
    Compara dos períodos temporales
    Body: { periodo_1, periodo_2, jurisdiccion_id, metrica }
    """
    try:
        data = request.get_json()
        resultado = comparador_periodos.comparar(
            periodo_1=data.get('periodo_1'),
            periodo_2=data.get('periodo_2'),
            jurisdiccion_id=data.get('jurisdiccion_id'),
            metrica=data.get('metrica', 'total_delitos')
        )
        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/mia/comparacion/mom', methods=['POST'])
def comparacion_mes_a_mes():
    """
    Comparación Mes vs Mes (MoM)
    Body: { mes_actual, mes_anterior, jurisdiccion_id }
    """
    try:
        data = request.get_json()
        resultado = comparador_periodos.comparacion_mom(
            mes_actual=data.get('mes_actual'),
            mes_anterior=data.get('mes_anterior'),
            jurisdiccion_id=data.get('jurisdiccion_id')
        )
        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/mia/comparacion/yoy', methods=['POST'])
def comparacion_ano_a_ano():
    """
    Comparación Año vs Año (YoY)
    Body: { ano_actual, ano_anterior, jurisdiccion_id }
    """
    try:
        data = request.get_json()
        resultado = comparador_periodos.comparacion_yoy(
            ano_actual=data.get('ano_actual'),
            ano_anterior=data.get('ano_anterior'),
            jurisdiccion_id=data.get('jurisdiccion_id')
        )
        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/mia/busqueda/semantica', methods=['POST'])
def busqueda_semantica():
    """
    Búsqueda semántica en reseñas
    Body: { termino, jurisdiccion_id, limite }
    """
    try:
        data = request.get_json()
        resultado = busqueda_inteligente.buscar_semantica(
            termino=data.get('termino'),
            jurisdiccion_id=data.get('jurisdiccion_id'),
            limite=data.get('limite', 50)
        )
        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/mia/busqueda/patron', methods=['POST'])
def buscar_patron_delictivo():
    """
    Busca patrones delictivos similares
    Body: { id_evento_referencia, similitud_minima }
    """
    try:
        data = request.get_json()
        resultado = busqueda_inteligente.buscar_patron(
            id_evento_referencia=data.get('id_evento_referencia'),
            similitud_minima=data.get('similitud_minima', 0.7)
        )
        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/mia/modus-operandi/perfiles', methods=['POST'])
def generar_perfiles_mo():
    """
    Genera perfiles de Modus Operandi
    Body: { jurisdiccion_id, fecha_inicio, fecha_fin, min_eventos }
    """
    try:
        data = request.get_json()
        resultado = busqueda_inteligente.generar_perfiles_mo(
            jurisdiccion_id=data.get('jurisdiccion_id'),
            fecha_inicio=data.get('fecha_inicio'),
            fecha_fin=data.get('fecha_fin'),
            min_eventos=data.get('min_eventos', 3)
        )
        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/upload-shapefile', methods=['POST'])
def upload_shapefile():
    """
    Carga un archivo ZIP con Shapefiles, lo procesa y devuelve GeoJSON.
    Optimizado para compatibilidad con QGIS 2.14 Essen (manejo de encoding 'latin1' y 'System').
    """
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and file.filename.endswith('.zip'):
        temp_dir = tempfile.mkdtemp()
        try:
            zip_path = os.path.join(temp_dir, file.filename)
            file.save(zip_path)
            
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)
            
            # Buscar archivo .shp
            shp_file = None
            base_path = None
            base_filename = None
            
            for root, dirs, files in os.walk(temp_dir):
                for f in files:
                    if f.lower().endswith('.shp'):
                        shp_file = os.path.join(root, f)
                        base_path = root
                        base_filename = os.path.splitext(f)[0]
                        break
                if shp_file:
                    break
            
            if not shp_file:
                return jsonify({'error': 'El ZIP no contiene ningún archivo .shp válido.'}), 400
            
            # Verificación básica de archivos sidecar (.shx, .dbf)
            # Intentamos encontrar los archivos mandatorios.
            required_extensions = ['.shx', '.dbf']
            missing_files = []
            
            # Listar archivos en el directorio del shapefile para búsqueda case-insensitive
            files_in_dir = os.listdir(base_path)
            files_lower = {f.lower(): f for f in files_in_dir}
            
            for ext in required_extensions:
                expected_file_lower = (base_filename + ext).lower()
                if expected_file_lower not in files_lower:
                    missing_files.append(ext)
            
            if missing_files:
                return jsonify({'error': f'Archivo incompleto. Faltan componentes: {", ".join(missing_files)}'}), 400

            # Detección de Encoding (Específico para QGIS viejos)
            # 1. Buscar archivo .cpg
            encoding = None
            cpg_file_lower = (base_filename + '.cpg').lower()
            if cpg_file_lower in files_lower:
                try:
                    with open(os.path.join(base_path, files_lower[cpg_file_lower]), 'r') as f:
                        encoding = f.read().strip()
                except:
                    pass
            
            # 2. Leer shapefile
            gdf = None
            read_error = None
            
            # Lista de encodings para probar (QGIS 2.14 usa mucho system locale/latin1)
            encodings_to_try = []
            if encoding:
                encodings_to_try.append(encoding)
            encodings_to_try.extend(['utf-8', 'latin1', 'cp1252'])
            
            for enc in encodings_to_try:
                try:
                    gdf = gpd.read_file(shp_file, encoding=enc)
                    break 
                except Exception as e:
                    read_error = e
                    continue
            
            if gdf is None:
                return jsonify({'error': f'No se pudo leer el archivo. Posible problema de codificación. Error: {str(read_error)}'}), 400
            
            # Convertir a WGS84 (EPSG:4326) si es necesario
            if gdf.crs:
                try:
                    if gdf.crs.to_string() != 'EPSG:4326':
                        gdf = gdf.to_crs('EPSG:4326')
                except Exception as e:
                    return jsonify({'error': f'Error al reproyectar coordenadas: {str(e)}'}), 400
            else:
                # Si no tiene CRS, advertimos pero intentamos continuar
                print("Advertencia: El Shapefile no tiene sistema de referencia de coordenadas (.prj) definido.")

            # Convertir a GeoJSON
            geojson_data = gdf.to_json()
            
            count = len(gdf)
            
            return jsonify({
                'status': 'success', 
                'data': geojson_data,
                'message': f'Se cargaron {count} elementos correctamente.'
            }), 200
            
        except Exception as e:
            return jsonify({'error': f'Error interno al procesar el archivo: {str(e)}'}), 500
        finally:
            shutil.rmtree(temp_dir)
    
    return jsonify({'error': 'Invalid file type. Please upload a ZIP file.'}), 400


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='127.0.0.1', port=port, debug=app.config['DEBUG'])
