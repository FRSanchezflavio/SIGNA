"""
Servicio de Análisis de Correlaciones
Identifica relaciones entre variables delictivas
"""

import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency, pearsonr
import json


class AnalisisCorrelaciones:
    
    def calcular_correlacion(self, variable_x, variable_y, jurisdiccion_id=None, 
                            fecha_inicio=None, fecha_fin=None):
        """
        Calcula correlación entre dos variables
        
        Args:
            variable_x: 'tipo_delito', 'franja_horaria', 'dia_semana', etc.
            variable_y: Variable a correlacionar
        
        Returns:
            dict: Matriz de correlación y estadísticas
        """
        try:
            # TODO: Obtener datos reales
            datos = self._generar_datos_correlacion_simulados()
            
            # Crear tabla de contingencia
            tabla_contingencia = pd.crosstab(datos[variable_x], datos[variable_y])
            
            # Test Chi-cuadrado
            chi2, p_valor, dof, expected = chi2_contingency(tabla_contingencia)
            
            # Determinar significancia
            es_significativa = p_valor < 0.05
            
            return {
                'variable_x': variable_x,
                'variable_y': variable_y,
                'tabla_contingencia': tabla_contingencia.to_dict(),
                'chi_cuadrado': float(chi2),
                'p_valor': float(p_valor),
                'grados_libertad': int(dof),
                'es_significativa': es_significativa,
                'interpretacion': self._interpretar_correlacion(chi2, p_valor, es_significativa),
                'fuerza_asociacion': self._calcular_fuerza_asociacion(chi2, tabla_contingencia)
            }
            
        except Exception as e:
            raise Exception(f"Error al calcular correlación: {str(e)}")
    
    def generar_matriz(self, variables, jurisdiccion_id=None, 
                      fecha_inicio=None, fecha_fin=None):
        """
        Genera matriz de correlaciones múltiples
        
        Returns:
            dict: Matriz con todas las correlaciones
        """
        try:
            resultados = {}
            
            for i, var1 in enumerate(variables):
                for var2 in variables[i+1:]:
                    key = f"{var1}_vs_{var2}"
                    resultados[key] = self.calcular_correlacion(
                        var1, var2, jurisdiccion_id, fecha_inicio, fecha_fin
                    )
            
            return {
                'matriz_correlaciones': resultados,
                'variables_analizadas': variables,
                'total_combinaciones': len(resultados)
            }
            
        except Exception as e:
            raise Exception(f"Error al generar matriz: {str(e)}")
    
    def _generar_datos_correlacion_simulados(self):
        """Genera datos simulados para testing"""
        np.random.seed(42)
        n = 200
        
        datos = pd.DataFrame({
            'tipo_delito': np.random.choice(['ROBO', 'HURTO', 'ROBO AGRAVADO'], n),
            'franja_horaria': np.random.choice(['MADRUGADA', 'MAÑANA', 'TARDE', 'NOCHE'], n),
            'dia_semana': np.random.choice(['LUNES', 'MARTES', 'MIÉRCOLES', 'JUEVES', 'VIERNES', 'SÁBADO', 'DOMINGO'], n),
            'lugar_tipo': np.random.choice(['VÍA PÚBLICA', 'COMERCIO', 'DOMICILIO PARTICULAR'], n),
            'arma_utilizada': np.random.choice(['ARMA DE FUEGO', 'ARMA BLANCA', 'SIN ARMA'], n)
        })
        
        return datos
    
    def _interpretar_correlacion(self, chi2, p_valor, es_significativa):
        """Genera interpretación textual"""
        if es_significativa:
            if chi2 > 20:
                return "Existe una FUERTE asociación estadística entre las variables (p < 0.05)."
            elif chi2 > 10:
                return "Existe una MODERADA asociación estadística entre las variables (p < 0.05)."
            else:
                return "Existe una DÉBIL asociación estadística entre las variables (p < 0.05)."
        else:
            return "NO existe asociación estadísticamente significativa entre las variables (p >= 0.05)."
    
    def _calcular_fuerza_asociacion(self, chi2, tabla):
        """Calcula el coeficiente V de Cramer"""
        n = tabla.sum().sum()
        min_dim = min(len(tabla.index), len(tabla.columns)) - 1
        v_cramer = np.sqrt(chi2 / (n * min_dim))
        
        if v_cramer < 0.1:
            return {'valor': float(v_cramer), 'clasificacion': 'DÉBIL'}
        elif v_cramer < 0.3:
            return {'valor': float(v_cramer), 'clasificacion': 'MODERADA'}
        else:
            return {'valor': float(v_cramer), 'clasificacion': 'FUERTE'}
