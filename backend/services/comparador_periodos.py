"""
Servicio de Comparación de Períodos
Análisis MoM (Month-over-Month) y YoY (Year-over-Year)
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


class ComparadorPeriodos:
    
    def comparar(self, periodo_1, periodo_2, jurisdiccion_id=None, metrica='total_delitos'):
        """
        Compara dos períodos personalizados
        
        Args:
            periodo_1: {'fecha_inicio': str, 'fecha_fin': str}
            periodo_2: {'fecha_inicio': str, 'fecha_fin': str}
            metrica: 'total_delitos', 'tipo_delito', 'franja_horaria', etc.
        
        Returns:
            dict: Comparación detallada con variaciones
        """
        try:
            # TODO: Obtener datos reales de la BD
            datos_p1 = self._obtener_datos_periodo(periodo_1)
            datos_p2 = self._obtener_datos_periodo(periodo_2)
            
            # Calcular métricas
            total_p1 = datos_p1['total']
            total_p2 = datos_p2['total']
            
            variacion_absoluta = total_p1 - total_p2
            variacion_porcentual = ((total_p1 - total_p2) / total_p2 * 100) if total_p2 > 0 else 0
            
            return {
                'periodo_1': {
                    'rango': periodo_1,
                    'total_delitos': total_p1,
                    'desglose': datos_p1['desglose']
                },
                'periodo_2': {
                    'rango': periodo_2,
                    'total_delitos': total_p2,
                    'desglose': datos_p2['desglose']
                },
                'variacion': {
                    'absoluta': variacion_absoluta,
                    'porcentual': round(variacion_porcentual, 2),
                    'tendencia': 'AUMENTO' if variacion_absoluta > 0 else 'DISMINUCIÓN' if variacion_absoluta < 0 else 'ESTABLE'
                },
                'interpretacion': self._generar_interpretacion(variacion_porcentual)
            }
            
        except Exception as e:
            raise Exception(f"Error al comparar períodos: {str(e)}")
    
    def comparacion_mom(self, mes_actual, mes_anterior, jurisdiccion_id=None):
        """
        Comparación Mes vs Mes (Month-over-Month)
        
        Args:
            mes_actual: str formato 'YYYY-MM'
            mes_anterior: str formato 'YYYY-MM' o None (automático)
        
        Returns:
            dict: Comparación mensual
        """
        try:
            # Parsear fecha
            fecha_actual = datetime.strptime(mes_actual, '%Y-%m')
            
            if not mes_anterior:
                fecha_anterior = fecha_actual - relativedelta(months=1)
            else:
                fecha_anterior = datetime.strptime(mes_anterior, '%Y-%m')
            
            # Crear períodos
            periodo_1 = {
                'fecha_inicio': fecha_actual.strftime('%Y-%m-01'),
                'fecha_fin': (fecha_actual + relativedelta(months=1) - timedelta(days=1)).strftime('%Y-%m-%d')
            }
            
            periodo_2 = {
                'fecha_inicio': fecha_anterior.strftime('%Y-%m-01'),
                'fecha_fin': (fecha_anterior + relativedelta(months=1) - timedelta(days=1)).strftime('%Y-%m-%d')
            }
            
            resultado = self.comparar(periodo_1, periodo_2, jurisdiccion_id)
            resultado['tipo_comparacion'] = 'MoM (Mes vs Mes)'
            
            return resultado
            
        except Exception as e:
            raise Exception(f"Error en comparación MoM: {str(e)}")
    
    def comparacion_yoy(self, ano_actual, ano_anterior, jurisdiccion_id=None):
        """
        Comparación Año vs Año (Year-over-Year)
        
        Args:
            ano_actual: int
            ano_anterior: int o None (automático)
        
        Returns:
            dict: Comparación anual
        """
        try:
            if not ano_anterior:
                ano_anterior = ano_actual - 1
            
            periodo_1 = {
                'fecha_inicio': f'{ano_actual}-01-01',
                'fecha_fin': f'{ano_actual}-12-31'
            }
            
            periodo_2 = {
                'fecha_inicio': f'{ano_anterior}-01-01',
                'fecha_fin': f'{ano_anterior}-12-31'
            }
            
            resultado = self.comparar(periodo_1, periodo_2, jurisdiccion_id)
            resultado['tipo_comparacion'] = 'YoY (Año vs Año)'
            
            return resultado
            
        except Exception as e:
            raise Exception(f"Error en comparación YoY: {str(e)}")
    
    def _obtener_datos_periodo(self, periodo):
        """Simula obtención de datos del período"""
        # TODO: Implementar consulta real a la BD
        np.random.seed(hash(periodo['fecha_inicio']) % 1000)
        
        total = np.random.randint(50, 200)
        
        desglose = {
            'ROBO': np.random.randint(10, 50),
            'HURTO': np.random.randint(10, 50),
            'ROBO AGRAVADO': np.random.randint(5, 30),
            'OTROS': np.random.randint(5, 20)
        }
        
        return {
            'total': total,
            'desglose': desglose
        }
    
    def _generar_interpretacion(self, variacion_porcentual):
        """Genera interpretación textual de la variación"""
        abs_var = abs(variacion_porcentual)
        
        if abs_var < 5:
            nivel = "insignificante"
        elif abs_var < 15:
            nivel = "moderado"
        elif abs_var < 30:
            nivel = "significativo"
        else:
            nivel = "crítico"
        
        direccion = "incremento" if variacion_porcentual > 0 else "decremento"
        
        return f"Se observa un {nivel} {direccion} del {abs(variacion_porcentual):.1f}% respecto al período anterior."
