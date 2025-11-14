"""
SIGNA - Sistema de Inteligencia y Gestión de Análisis
Backend API - Módulo de Inteligencia Avanzada (MIA)
Flask Application
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
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


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='127.0.0.1', port=port, debug=app.config['DEBUG'])
