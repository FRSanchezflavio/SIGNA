"""
Servicio de Búsqueda Inteligente
Búsqueda semántica y análisis de patrones
"""

import pandas as pd
import numpy as np
from difflib import SequenceMatcher
import re


class BusquedaInteligente:
    
    def buscar_semantica(self, termino, jurisdiccion_id=None, limite=50):
        """
        Búsqueda semántica en reseñas de eventos
        
        Args:
            termino: Texto a buscar
            limite: Máximo de resultados
        
        Returns:
            dict: Eventos con relevancia ordenada
        """
        try:
            # TODO: Implementar búsqueda real en PostgreSQL usando full-text search
            # O en SQLite usando FTS5
            
            # Simulación
            eventos = self._generar_eventos_simulados(termino)
            
            # Calcular relevancia
            eventos_con_relevancia = []
            for evento in eventos:
                relevancia = self._calcular_relevancia(termino, evento['resena_hecho'])
                if relevancia > 0.3:
                    evento['relevancia'] = relevancia
                    eventos_con_relevancia.append(evento)
            
            # Ordenar por relevancia
            eventos_ordenados = sorted(
                eventos_con_relevancia, 
                key=lambda x: x['relevancia'], 
                reverse=True
            )[:limite]
            
            return {
                'total_encontrados': len(eventos_ordenados),
                'termino_busqueda': termino,
                'eventos': eventos_ordenados
            }
            
        except Exception as e:
            raise Exception(f"Error en búsqueda semántica: {str(e)}")
    
    def buscar_patron(self, id_evento_referencia, similitud_minima=0.7):
        """
        Busca eventos con patrón similar a un evento de referencia
        
        Args:
            id_evento_referencia: ID del evento modelo
            similitud_minima: Umbral de similitud (0-1)
        
        Returns:
            dict: Eventos similares
        """
        try:
            # TODO: Obtener evento de referencia de la BD
            evento_ref = self._obtener_evento_referencia(id_evento_referencia)
            
            # TODO: Buscar eventos similares
            eventos_similares = self._buscar_eventos_similares(evento_ref, similitud_minima)
            
            return {
                'evento_referencia': evento_ref,
                'total_similares': len(eventos_similares),
                'umbral_similitud': similitud_minima,
                'eventos_similares': eventos_similares
            }
            
        except Exception as e:
            raise Exception(f"Error al buscar patrón: {str(e)}")
    
    def generar_perfiles_mo(self, jurisdiccion_id=None, fecha_inicio=None, 
                           fecha_fin=None, min_eventos=3):
        """
        Genera perfiles de Modus Operandi
        
        Returns:
            dict: Perfiles identificados
        """
        try:
            # TODO: Agrupar eventos por características similares
            
            perfiles = [
                {
                    'id_perfil': 1,
                    'nombre': 'Robo Agravado Nocturno con Motocicleta',
                    'descripcion': 'Robo con arma de fuego, en franja nocturna (20:00-23:00), usando motocicleta',
                    'caracteristicas': {
                        'tipo_delito': 'ROBO AGRAVADO',
                        'franja_horaria': 'NOCHE',
                        'vehiculo': 'MOTOCICLETA',
                        'arma': 'ARMA DE FUEGO',
                        'lugar_frecuente': 'VÍA PÚBLICA'
                    },
                    'eventos_agrupados': 15,
                    'zona_predominante': 'CENTRO',
                    'nivel_peligrosidad': 'ALTO'
                },
                {
                    'id_perfil': 2,
                    'nombre': 'Hurto de Oportunidad Diurno',
                    'descripcion': 'Hurto sin violencia, en horario de tarde, en comercios',
                    'caracteristicas': {
                        'tipo_delito': 'HURTO',
                        'franja_horaria': 'TARDE',
                        'vehiculo': 'A PIE',
                        'arma': 'SIN ARMA',
                        'lugar_frecuente': 'COMERCIO'
                    },
                    'eventos_agrupados': 22,
                    'zona_predominante': 'MICROCENTRO',
                    'nivel_peligrosidad': 'MEDIO'
                }
            ]
            
            return {
                'total_perfiles': len(perfiles),
                'min_eventos_agrupacion': min_eventos,
                'perfiles': perfiles,
                'recomendacion': 'Asignar recursos preventivos según horarios y zonas identificadas.'
            }
            
        except Exception as e:
            raise Exception(f"Error al generar perfiles MO: {str(e)}")
    
    def _calcular_relevancia(self, termino, texto):
        """Calcula similitud entre términos de búsqueda y texto"""
        termino_lower = termino.lower()
        texto_lower = texto.lower()
        
        # Coincidencia exacta
        if termino_lower in texto_lower:
            return 1.0
        
        # Similitud de secuencia
        return SequenceMatcher(None, termino_lower, texto_lower).ratio()
    
    def _generar_eventos_simulados(self, termino):
        """Genera eventos simulados para testing"""
        return [
            {
                'id_evento': 1,
                'numero_sumario': '001/2025',
                'resena_hecho': f'Robo con {termino} en vía pública durante la noche',
                'fecha_delito': '2025-01-15',
                'jurisdiccion': 'Centro'
            },
            {
                'id_evento': 2,
                'numero_sumario': '002/2025',
                'resena_hecho': f'Hurto mediante {termino} en comercio',
                'fecha_delito': '2025-01-16',
                'jurisdiccion': 'Norte'
            }
        ]
    
    def _obtener_evento_referencia(self, id_evento):
        """Obtiene evento de referencia (simulado)"""
        return {
            'id_evento': id_evento,
            'tipo_delito': 'ROBO AGRAVADO',
            'modus_operandi': 'INTIMIDACIÓN',
            'franja_horaria': 'NOCHE',
            'vehiculo': 'MOTOCICLETA'
        }
    
    def _buscar_eventos_similares(self, evento_ref, umbral):
        """Busca eventos similares (simulado)"""
        return [
            {
                'id_evento': 123,
                'similitud': 0.85,
                'coincidencias': ['tipo_delito', 'franja_horaria', 'vehiculo']
            },
            {
                'id_evento': 456,
                'similitud': 0.75,
                'coincidencias': ['tipo_delito', 'modus_operandi']
            }
        ]
