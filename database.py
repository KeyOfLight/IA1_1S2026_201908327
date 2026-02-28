"""
Módulo de base de datos integrado con motor de Prolog
Maneja autenticación, diagnósticos y persistencia de datos
"""

import json
import os
from datetime import datetime
from prolog_engine import get_prolog_engine


# Rutas de archivos de datos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CREDENTIALS_FILE = os.path.join(BASE_DIR, "credentials.json")
DIAGNOSES_FILE = os.path.join(BASE_DIR, "diagnoses.json")


def initialize_data():
    """Inicializa los archivos de datos si no existen"""
    # Crear archivo de credenciales si no existe
    if not os.path.exists(CREDENTIALS_FILE):
        default_credentials = {
            "users": [
                {
                    "username": "medico",
                    "password": "medico123",
                    "level": "medico",
                    "name": "Dr. Médico"
                },
                {
                    "username": "admin",
                    "password": "admin123",
                    "level": "admin",
                    "name": "Administrador"
                }
            ]
        }
        with open(CREDENTIALS_FILE, 'w', encoding='utf-8') as f:
            json.dump(default_credentials, f, ensure_ascii=False, indent=2)
    
    # Crear archivo de diagnósticos si no existe
    if not os.path.exists(DIAGNOSES_FILE):
        with open(DIAGNOSES_FILE, 'w', encoding='utf-8') as f:
            json.dump({"diagnoses": []}, f, ensure_ascii=False, indent=2)


def validate_credentials(username, password):
    """
    Valida las credenciales del usuario
    
    Args:
        username: Nombre de usuario
        password: Contraseña
    
    Returns:
        Diccionario con 'authenticated' (bool) y 'level' (str)
    """
    initialize_data()
    
    try:
        with open(CREDENTIALS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        for user in data.get("users", []):
            if user["username"] == username and user["password"] == password:
                return {
                    "authenticated": True,
                    "level": user["level"]
                }
        
        return {
            "authenticated": False,
            "level": None
        }
    except Exception as e:
        print(f"Error validando credenciales: {e}")
        return {
            "authenticated": False,
            "level": None
        }


def save_diagnosis(symptoms, conditions):
    """
    Guarda un registro de diagnóstico en JSON (datos de Prolog guardados)
    
    Args:
        symptoms: Lista de síntomas seleccionados
        conditions: Lista de condiciones diagnosticadas (tuplas)
    
    Returns:
        Boolean indicando éxito
    """
    initialize_data()
    
    try:
        with open(DIAGNOSES_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Crear registro de diagnóstico
        diagnosis_record = {
            "id": len(data["diagnoses"]) + 1,
            "symptoms": symptoms,
            "conditions": [
                {
                    "name": c[0] if isinstance(c, tuple) else c, 
                    "relevance": c[1] if isinstance(c, tuple) else 1
                } 
                for c in conditions
            ],
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "source": "prolog"  # Identificar que vino de Prolog
        }
        
        data["diagnoses"].append(diagnosis_record)
        
        with open(DIAGNOSES_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"✓ Diagnóstico guardado (desde Prolog): ID {diagnosis_record['id']}")
        return True
    except Exception as e:
        print(f"Error guardando diagnóstico: {e}")
        return False


def obtener_sintomas():
    """
    Obtiene lista de síntomas del motor de Prolog
    
    Returns:
        Lista de síntomas disponibles
    """
    try:
        engine = get_prolog_engine()
        sintomas = engine.obtener_sintomas()
        return sintomas
    except Exception as e:
        print(f"Error obteniendo síntomas: {e}")
        return []


def obtener_diagnostico_prolog(sintomas):
    """
    Obtiene diagnósticos usando el motor de Prolog
    
    Args:
        sintomas: Lista de síntomas seleccionados
    
    Returns:
        Lista de tuplas (diagnóstico, relevancia)
    """
    try:
        engine = get_prolog_engine()
        diagnosticos = engine.obtener_diagnosticos(sintomas)
        return diagnosticos
    except Exception as e:
        print(f"Error obteniendo diagnósticos de Prolog: {e}")
        return []


def obtener_recomendacion_prolog(condicion):
    """
    Obtiene recomendación médica del motor de Prolog
    
    Args:
        condicion: Nombre de la condición
    
    Returns:
        String con recomendación
    """
    try:
        engine = get_prolog_engine()
        recomendacion = engine.obtener_recomendacion(condicion)
        return recomendacion
    except Exception as e:
        print(f"Error obteniendo recomendación: {e}")
        return "Consulte con un profesional médico."


def es_condicion_urgente(condicion):
    """
    Verifica si una condición requiere atención inmediata
    
    Args:
        condicion: Nombre de la condición
    
    Returns:
        Boolean
    """
    try:
        engine = get_prolog_engine()
        return engine.es_urgente(condicion)
    except Exception as e:
        print(f"Error verificando urgencia: {e}")
        return False


def get_diagnoses():
    """
    Obtiene todos los diagnósticos registrados
    
    Returns:
        Lista de diagnósticos formateados para la tabla
    """
    initialize_data()
    
    try:
        with open(DIAGNOSES_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        diagnoses_list = []
        for diagnosis in data.get("diagnoses", []):
            # Formatear síntomas
            symptoms_str = ", ".join(diagnosis["symptoms"])
            
            # Formatear condiciones
            conditions_str = ", ".join(
                [c["name"] for c in diagnosis.get("conditions", [])]
            )
            
            # Agregar a la lista
            diagnoses_list.append((
                diagnosis["id"],
                symptoms_str,
                conditions_str,
                diagnosis["date"]
            ))
        
        return diagnoses_list
    except Exception as e:
        print(f"Error obteniendo diagnósticos: {e}")
        return []


def delete_diagnosis(diagnosis_id):
    """
    Elimina un diagnóstico de los registros
    
    Args:
        diagnosis_id: ID del diagnóstico a eliminar
    """
    initialize_data()
    
    try:
        with open(DIAGNOSES_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Eliminar el diagnóstico con el ID especificado
        data["diagnoses"] = [
            d for d in data["diagnoses"] if d["id"] != diagnosis_id
        ]
        
        # Renumerar los IDs
        for i, diagnosis in enumerate(data["diagnoses"], 1):
            diagnosis["id"] = i
        
        with open(DIAGNOSES_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        return True
    except Exception as e:
        print(f"Error eliminando diagnóstico: {e}")
        return False


def add_user(username, password, level, name):
    """
    Agrega un nuevo usuario (solo para administradores)
    
    Args:
        username: Nombre de usuario
        password: Contraseña
        level: Nivel de acceso (medico o admin)
        name: Nombre completo
    
    Returns:
        Boolean indicando éxito
    """
    initialize_data()
    
    try:
        with open(CREDENTIALS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Verificar que el usuario no exista
        for user in data.get("users", []):
            if user["username"] == username:
                return False
        
        # Agregar nuevo usuario
        new_user = {
            "username": username,
            "password": password,
            "level": level,
            "name": name
        }
        data["users"].append(new_user)
        
        with open(CREDENTIALS_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        return True
    except Exception as e:
        print(f"Error agregando usuario: {e}")
        return False


def get_statistics():
    """
    Obtiene estadísticas de los diagnósticos del motor Prolog
    
    Returns:
        Diccionario con estadísticas
    """
    initialize_data()
    
    try:
        with open(DIAGNOSES_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        diagnoses = data.get("diagnoses", [])
        
        # Contar síntomas más frecuentes
        symptom_count = {}
        for diagnosis in diagnoses:
            for symptom in diagnosis.get("symptoms", []):
                symptom_count[symptom] = symptom_count.get(symptom, 0) + 1
        
        # Contar condiciones más frecuentes
        condition_count = {}
        for diagnosis in diagnoses:
            for condition in diagnosis.get("conditions", []):
                cond_name = condition["name"]
                condition_count[cond_name] = condition_count.get(cond_name, 0) + 1
        
        return {
            "total_diagnoses": len(diagnoses),
            "total_symptoms": len(symptom_count),
            "total_conditions": len(condition_count),
            "top_symptoms": sorted(symptom_count.items(), key=lambda x: x[1], reverse=True)[:5],
            "top_conditions": sorted(condition_count.items(), key=lambda x: x[1], reverse=True)[:5],
            "engine": "Prolog"  # Indicar que usa Prolog
        }
    except Exception as e:
        print(f"Error obteniendo estadísticas: {e}")
        return {
            "total_diagnoses": 0,
            "total_symptoms": 0,
            "total_conditions": 0,
            "top_symptoms": [],
            "top_conditions": [],
            "engine": "Prolog"
        }


# Inicializar datos al importar el módulo
initialize_data()
