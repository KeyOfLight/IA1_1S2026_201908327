"""
Motor de Prolog para diagnósticos médicos
Conecta Python con el sistema de reglas en Prolog
"""

import os
from pathlib import Path

try:
    from pyswip import Prolog
except ImportError:
    print("ERROR: pyswip no está instalado.")
    print("Instálalo con: pip install pyswip")
    raise


class PrologDiagnosticEngine:
    """Motor de diagnóstico basado en Prolog"""
    
    def __init__(self):
        """Inicializa el motor de Prolog"""
        self.prolog = Prolog()
        
        # Cargar el archivo de reglas
        rules_file = os.path.join(os.path.dirname(__file__), "diagnostic_rules.pl")
        
        if not os.path.exists(rules_file):
            raise FileNotFoundError(f"Archivo de reglas no encontrado: {rules_file}")
        
        # Cargar las reglas en Prolog
        try:
            self.prolog.consult(rules_file)
            print(f"✓ Reglas de Prolog cargadas desde: {rules_file}")
        except Exception as e:
            raise Exception(f"Error al cargar reglas Prolog: {e}")
    
    def obtener_sintomas(self):
        """Obtiene la lista de síntomas disponibles"""
        try:
            sintomas = []
            for result in self.prolog.query("todos_sintomas(S)"):
                sintomas_temp = result["S"]
                # Convertir lista de Prolog a lista de Python
                sintomas = self._prolog_list_to_python(sintomas_temp)
                break
            
            # Formatear para GUI (reemplazar guiones bajos por espacios)
            sintomas_formateados = [s.replace('_', ' ').title() for s in sintomas]
            return sorted(sintomas_formateados)
        except Exception as e:
            print(f"Error obteniendo síntomas: {e}")
            return []
    
    def obtener_diagnosticos(self, sintomas_seleccionados):
        """
        Obtiene diagnósticos basados en síntomas seleccionados
        
        Args:
            sintomas_seleccionados: Lista de síntomas (strings con espacios)
        
        Returns:
            Lista de tuplas (condición, relevancia)
        """
        try:
            # Convertir síntomas a formato Prolog (minúsculas y guiones bajos)
            sintomas_prolog = [s.lower().replace(' ', '_') for s in sintomas_seleccionados]
            
            # Crear lista Prolog
            sintomas_formato_prolog = self._python_list_to_prolog(sintomas_prolog)
            
            # Consultar diagnósticos ordenados
            diagnosticos = []
            query = f"diagnosticos_ordenados({sintomas_formato_prolog}, D)"
            
            for result in self.prolog.query(query):
                diagnosticos_lista = result["D"]
                diagnosticos_temp = self._prolog_list_to_python(diagnosticos_lista)
                
                # Convertir formato de Prolog a tuplas (condición, relevancia)
                diagnosticos_con_relevancia = []
                for item in diagnosticos_temp:
                    # item es de formato: "condición-relevancia"
                    if isinstance(item, str) and '-' in item:
                        partes = item.split('-')
                        if len(partes) == 2:
                            condicion, relevancia = partes
                            diagnosticos_con_relevancia.append(
                                (condicion.replace('_', ' ').title(), int(relevancia))
                            )
                
                diagnosticos = diagnosticos_con_relevancia
                break
            
            return diagnosticos
        except Exception as e:
            print(f"Error obteniendo diagnósticos: {e}")
            return []
    
    def obtener_recomendacion(self, condicion):
        """
        Obtiene la recomendación médica para una condición
        
        Args:
            condicion: Nombre de la condición (string con espacios)
        
        Returns:
            String con la recomendación
        """
        try:
            # Convertir a formato Prolog
            condicion_prolog = condicion.lower().replace(' ', '_')
            
            for result in self.prolog.query(f"obtener_recomendacion({condicion_prolog}, R)"):
                recomendacion = result["R"]
                if isinstance(recomendacion, str):
                    return recomendacion
            
            return "Consulte con un profesional médico para más información."
        except Exception as e:
            print(f"Error obteniendo recomendación: {e}")
            return "Consulte con un profesional médico para más información."
    
    def es_urgente(self, condicion):
        """
        Verifica si una condición requiere atención inmediata
        
        Args:
            condicion: Nombre de la condición (string con espacios)
        
        Returns:
            Boolean
        """
        try:
            condicion_prolog = condicion.lower().replace(' ', '_')
            
            for _ in self.prolog.query(f"es_urgente({condicion_prolog})"):
                return True
            
            return False
        except Exception as e:
            print(f"Error verificando urgencia: {e}")
            return False
    
    def obtener_descripcion_sintoma(self, sintoma):
        """
        Obtiene la descripción de un síntoma
        
        Args:
            sintoma: Nombre del síntoma (string con espacios)
        
        Returns:
            String con la descripción
        """
        try:
            sintoma_prolog = sintoma.lower().replace(' ', '_')
            
            for result in self.prolog.query(f"descripcion_sintoma({sintoma_prolog}, D)"):
                descripcion = result["D"]
                if isinstance(descripcion, str):
                    return descripcion
            
            return "Sin descripción disponible."
        except Exception as e:
            print(f"Error obteniendo descripción: {e}")
            return "Sin descripción disponible."
    
    def obtener_severidad_sintoma(self, sintoma):
        """
        Obtiene el nivel de severidad de un síntoma
        
        Args:
            sintoma: Nombre del síntoma (string con espacios)
        
        Returns:
            String: 'alta', 'media' o 'baja'
        """
        try:
            sintoma_prolog = sintoma.lower().replace(' ', '_')
            
            for result in self.prolog.query(f"severidad({sintoma_prolog}, S)"):
                severidad = result["S"]
                if isinstance(severidad, str):
                    return severidad
            
            return "media"
        except Exception as e:
            print(f"Error obteniendo severidad: {e}")
            return "media"
    
    # ==================== MÉTODOS AUXILIARES ====================
    
    def _python_list_to_prolog(self, py_list):
        """Convierte una lista de Python a formato de lista Prolog"""
        if not py_list:
            return "[]"
        
        items = ", ".join([f"'{item}'" for item in py_list])
        return f"[{items}]"
    
    def _prolog_list_to_python(self, prolog_list):
        """Convierte una lista de Prolog a lista de Python"""
        result = []
        
        if isinstance(prolog_list, str):
            # Si es un string, parsearlo
            return [prolog_list]
        
        # Iterar a través de la lista de Prolog
        try:
            if hasattr(prolog_list, '__iter__'):
                for item in prolog_list:
                    result.append(str(item))
        except:
            result.append(str(prolog_list))
        
        return result


# Instancia global del motor
_engine = None


def get_prolog_engine():
    """Obtiene instancia global del motor de Prolog"""
    global _engine
    if _engine is None:
        _engine = PrologDiagnosticEngine()
    return _engine
