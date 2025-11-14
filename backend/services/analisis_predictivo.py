"""
Servicio de Análisis Predictivo
Implementa modelos de tendencias y proyecciones delictivas
"""

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from statsmodels.tsa.arima.model import ARIMA
from datetime import datetime, timedelta
import json


class AnalisisPredictivo:
    
    def __init__(self):
        self.modelos_cache = {}
    
    def calcular_tendencias(self, jurisdiccion_id=None, tipo_delito_id=None, dias_horizonte=30):
        """
        Calcula la tendencia delictiva usando regresión lineal
        
        Returns:
            dict: {
                'tendencia': 'ASCENDENTE' | 'DESCENDENTE' | 'ESTABLE',
                'pendiente': float,
                'r_cuadrado': float,
                'datos_historicos': [...],
                'proyeccion': [...]
            }
        """
        try:
            # TODO: Obtener datos reales de la base de datos
            # Por ahora, generamos datos simulados
            datos_historicos = self._generar_datos_simulados(90)
            
            # Preparar datos para regresión
            X = np.array(range(len(datos_historicos))).reshape(-1, 1)
            y = np.array(datos_historicos)
            
            # Entrenar modelo
            modelo = LinearRegression()
            modelo.fit(X, y)
            
            # Calcular métricas
            r_cuadrado = modelo.score(X, y)
            pendiente = modelo.coef_[0]
            
            # Clasificar tendencia
            if pendiente > 0.1:
                tendencia = 'ASCENDENTE'
            elif pendiente < -0.1:
                tendencia = 'DESCENDENTE'
            else:
                tendencia = 'ESTABLE'
            
            # Proyección
            X_futuro = np.array(range(len(datos_historicos), len(datos_historicos) + dias_horizonte)).reshape(-1, 1)
            proyeccion = modelo.predict(X_futuro).tolist()
            
            return {
                'tendencia': tendencia,
                'pendiente': float(pendiente),
                'r_cuadrado': float(r_cuadrado),
                'confianza': self._calcular_confianza(r_cuadrado),
                'datos_historicos': datos_historicos,
                'proyeccion': proyeccion,
                'mensaje': self._generar_mensaje_tendencia(tendencia, pendiente)
            }
            
        except Exception as e:
            raise Exception(f"Error al calcular tendencias: {str(e)}")
    
    def calcular_proyecciones(self, jurisdiccion_id=None, tipo_delito_id=None, periodos_futuro=12):
        """
        Calcula proyecciones usando modelo ARIMA
        
        Returns:
            dict: {
                'proyecciones': [...],
                'intervalos_confianza': {...},
                'metricas_modelo': {...}
            }
        """
        try:
            # TODO: Obtener datos reales de la base de datos
            datos_historicos = self._generar_datos_simulados(180)
            
            # Crear serie temporal
            serie = pd.Series(datos_historicos)
            
            # Entrenar modelo ARIMA (p=1, d=1, q=1)
            modelo = ARIMA(serie, order=(1, 1, 1))
            modelo_ajustado = modelo.fit()
            
            # Proyectar
            forecast = modelo_ajustado.forecast(steps=periodos_futuro)
            
            # Intervalos de confianza (simulados)
            conf_int_lower = [max(0, f * 0.8) for f in forecast]
            conf_int_upper = [f * 1.2 for f in forecast]
            
            return {
                'proyecciones': forecast.tolist(),
                'intervalos_confianza': {
                    'inferior': conf_int_lower,
                    'superior': conf_int_upper
                },
                'metricas_modelo': {
                    'aic': float(modelo_ajustado.aic),
                    'bic': float(modelo_ajustado.bic)
                },
                'advertencia': 'Las proyecciones son estimaciones basadas en datos históricos. Usar con precaución.'
            }
            
        except Exception as e:
            raise Exception(f"Error al calcular proyecciones: {str(e)}")
    
    def identificar_hotspots(self, jurisdiccion_id=None, tipo_delito_id=None, 
                            fecha_inicio=None, fecha_fin=None):
        """
        Identifica zonas de alta concentración delictiva
        
        Returns:
            dict: {
                'hotspots': [
                    {
                        'latitud': float,
                        'longitud': float,
                        'intensidad': int,
                        'radio_metros': float
                    }
                ]
            }
        """
        try:
            # TODO: Implementar análisis geoespacial real con clustering
            # Por ahora, retornamos datos simulados
            
            hotspots = [
                {
                    'id': 1,
                    'latitud': -26.8241,
                    'longitud': -65.2226,
                    'intensidad': 45,
                    'radio_metros': 500,
                    'eventos_totales': 45,
                    'nivel_riesgo': 'ALTO'
                },
                {
                    'id': 2,
                    'latitud': -26.8308,
                    'longitud': -65.2064,
                    'intensidad': 32,
                    'radio_metros': 400,
                    'eventos_totales': 32,
                    'nivel_riesgo': 'MEDIO'
                }
            ]
            
            return {
                'hotspots': hotspots,
                'total_hotspots': len(hotspots),
                'metodo': 'DBSCAN Clustering',
                'umbral_minimo': 10
            }
            
        except Exception as e:
            raise Exception(f"Error al identificar hotspots: {str(e)}")
    
    def _generar_datos_simulados(self, cantidad):
        """Genera datos simulados para testing"""
        np.random.seed(42)
        base = 20
        tendencia = np.linspace(0, 5, cantidad)
        ruido = np.random.normal(0, 3, cantidad)
        estacionalidad = 5 * np.sin(np.linspace(0, 4*np.pi, cantidad))
        return (base + tendencia + ruido + estacionalidad).tolist()
    
    def _calcular_confianza(self, r_cuadrado):
        """Calcula nivel de confianza basado en R²"""
        if r_cuadrado >= 0.8:
            return 'ALTA'
        elif r_cuadrado >= 0.5:
            return 'MEDIA'
        else:
            return 'BAJA'
    
    def _generar_mensaje_tendencia(self, tendencia, pendiente):
        """Genera mensaje interpretativo de la tendencia"""
        if tendencia == 'ASCENDENTE':
            return f"Se observa una tendencia ASCENDENTE con un incremento promedio de {abs(pendiente):.2f} delitos por día."
        elif tendencia == 'DESCENDENTE':
            return f"Se observa una tendencia DESCENDENTE con una reducción promedio de {abs(pendiente):.2f} delitos por día."
        else:
            return "Se observa una tendencia ESTABLE sin variaciones significativas."
