"""
Módulo de base de datos integrado con motor de Prolog
Maneja autenticación, diagnósticos y persistencia de datos
"""

import json
import os
from datetime import datetime
from prolog_engine import get_prolog_engine
from rpa_automation import execute_diagnosis_rpa_flow, get_rpa_status as get_rpa_status_internal


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


def save_diagnosis(
    symptoms,
    conditions,
    run_rpa=False,
    return_details=False,
    chronic_diseases=None,
    allergies=None,
    urgency_profile=None,
):
    """
    Guarda un registro de diagnóstico en JSON (datos de Prolog guardados)
    
    Args:
        symptoms: Lista de síntomas seleccionados
        conditions: Lista de condiciones diagnosticadas (tuplas)
        run_rpa: Ejecuta automatización con PyAutoGUI al guardar
        return_details: Retorna metadatos en lugar de bool para flujos UI avanzados
        chronic_diseases: Lista de enfermedades crónicas reportadas
        allergies: Lista de alergias reportadas
    
    Returns:
        Boolean indicando éxito o diccionario de detalles
    """
    initialize_data()
    
    try:
        with open(DIAGNOSES_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        chronic_diseases = _normalize_text_list(chronic_diseases)
        allergies = _normalize_text_list(allergies)

        # Procesar síntomas - manejar tanto formato antiguo (lista simple) como nuevo (con severidad)
        processed_symptoms = []
        if symptoms:
            for symptom in symptoms:
                if isinstance(symptom, dict):
                    # Nuevo formato con severidad
                    processed_symptoms.append({
                        "name": symptom.get("name", ""),
                        "severity": symptom.get("severity", "Moderado")
                    })
                else:
                    # Formato antiguo: solo string
                    processed_symptoms.append({
                        "name": symptom,
                        "severity": "Moderado"  # Severidad por defecto para compatibilidad
                    })

        # Crear registro de diagnóstico
        diagnosis_record = {
            "id": len(data["diagnoses"]) + 1,
            "symptoms": processed_symptoms,
            "enfermedades_cronicas": chronic_diseases,
            "alergias": allergies,
            "perfil_clinico": urgency_profile or {},
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

        rpa_result = None
        if run_rpa:
            try:
                rpa_result = execute_diagnosis_rpa_flow(diagnosis_record)
            except Exception as rpa_error:
                rpa_result = {
                    "executed": False,
                    "available": False,
                    "report_path": None,
                    "screenshot_path": None,
                    "message": f"Fallo inesperado en RPA: {rpa_error}",
                }
        
        print(f"✓ Diagnóstico guardado (desde Prolog): ID {diagnosis_record['id']}")
        if return_details:
            return {
                "success": True,
                "diagnosis_id": diagnosis_record["id"],
                "rpa": rpa_result,
            }
        return True
    except Exception as e:
        print(f"Error guardando diagnóstico: {e}")
        if return_details:
            return {
                "success": False,
                "diagnosis_id": None,
                "rpa": None,
                "error": str(e),
            }
        return False


def _normalize_text_list(values):
    """Normaliza listas de texto evitando nulos, vacíos y duplicados."""
    if not values:
        return []

    normalized = []
    seen = set()

    for value in values:
        text = str(value).strip()
        if not text:
            continue

        key = text.lower()
        if key in seen:
            continue

        seen.add(key)
        normalized.append(text)

    return normalized


def get_rpa_status():
    """Obtiene estado del módulo RPA (PyAutoGUI)."""
    return get_rpa_status_internal()


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


def obtener_diagnostico_prolog(sintomas, symptoms_with_severity=None):
    """
    Obtiene diagnósticos usando el motor de Prolog
    
    Args:
        sintomas: Lista de síntomas seleccionados (strings)
        symptoms_with_severity: Lista de diccionarios con síntoma y severidad (opcional)
    
    Returns:
        Lista de tuplas (diagnóstico, relevancia)
    """
    try:
        engine = get_prolog_engine()
        # Si tenemos severidad, pasarla al motor Prolog
        if symptoms_with_severity:
            diagnosticos = engine.obtener_diagnosticos(sintomas, symptoms_with_severity)
        else:
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


def obtener_perfil_urgencia(symptoms_with_severity, conditions=None, chronic_diseases=None, allergies=None):
    """Calcula nivel de urgencia clinica para el perfil actual."""
    try:
        engine = get_prolog_engine()
        return engine.evaluar_perfil_urgencia(
            symptoms_with_severity=symptoms_with_severity,
            condiciones=conditions,
            chronic_diseases=chronic_diseases,
            allergies=allergies,
        )
    except Exception as e:
        print(f"Error calculando perfil de urgencia: {e}")
        return {
            "score": 0,
            "nivel_urgencia": "leve",
            "accion_recomendada": "Consulte con un profesional medico para una evaluacion completa.",
        }


def obtener_clasificacion_condicion(condicion):
    """
    Obtiene clasificación de una condición por sistema y tipo clínico

    Args:
        condicion: Nombre de la condición

    Returns:
        Diccionario: {"condicion", "sistema", "tipo"}
    """
    try:
        engine = get_prolog_engine()
        return engine.obtener_clasificacion_condicion(condicion)
    except Exception as e:
        print(f"Error obteniendo clasificación para {condicion}: {e}")
        return {
            "condicion": str(condicion),
            "sistema": "No definido",
            "tipo": "No definido",
        }


def obtener_clasificacion_diagnosticos(diagnosticos):
    """
    Obtiene clasificación para una lista de diagnósticos

    Args:
        diagnosticos: Lista de tuplas (condicion, relevancia) o strings

    Returns:
        Diccionario con nombre de condición como llave y clasificación como valor
    """
    clasificaciones = {}

    for diagnostico in diagnosticos or []:
        if isinstance(diagnostico, tuple):
            condicion = diagnostico[0]
        else:
            condicion = str(diagnostico)

        clasificaciones[condicion] = obtener_clasificacion_condicion(condicion)

    return clasificaciones


def obtener_condiciones_por_sistema(sistema):
    """
    Lista condiciones según sistema corporal

    Args:
        sistema: Nombre del sistema

    Returns:
        Lista de condiciones
    """
    try:
        engine = get_prolog_engine()
        return engine.obtener_condiciones_por_sistema(sistema)
    except Exception as e:
        print(f"Error obteniendo condiciones por sistema {sistema}: {e}")
        return []


def obtener_condiciones_por_tipo(tipo):
    """
    Lista condiciones según tipo clínico

    Args:
        tipo: Nombre del tipo

    Returns:
        Lista de condiciones
    """
    try:
        engine = get_prolog_engine()
        return engine.obtener_condiciones_por_tipo(tipo)
    except Exception as e:
        print(f"Error obteniendo condiciones por tipo {tipo}: {e}")
        return []


def obtener_sistemas_clasificacion():
    """Obtiene sistemas disponibles para clasificación de condiciones."""
    try:
        engine = get_prolog_engine()
        return engine.obtener_sistemas_clasificacion()
    except Exception as e:
        print(f"Error obteniendo sistemas de clasificación: {e}")
        return []


def obtener_tipos_clasificacion():
    """Obtiene tipos disponibles para clasificación de condiciones."""
    try:
        engine = get_prolog_engine()
        return engine.obtener_tipos_clasificacion()
    except Exception as e:
        print(f"Error obteniendo tipos de clasificación: {e}")
        return []


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
            symptoms_str = ", ".join(diagnosis.get("symptoms", []))
            if not symptoms_str:
                symptoms_str = "No registrados"

            # Formatear enfermedades crónicas y alergias
            chronic_diseases_str = ", ".join(diagnosis.get("enfermedades_cronicas", []))
            if not chronic_diseases_str:
                chronic_diseases_str = "No reportadas"

            allergies_str = ", ".join(diagnosis.get("alergias", []))
            if not allergies_str:
                allergies_str = "No reportadas"
            
            # Formatear condiciones
            condition_names = []
            for condition in diagnosis.get("conditions", []):
                if isinstance(condition, dict):
                    condition_names.append(condition.get("name", ""))
                else:
                    condition_names.append(str(condition))

            conditions_str = ", ".join([name for name in condition_names if name])
            if not conditions_str:
                conditions_str = "Sin diagnóstico"
            
            # Agregar a la lista
            diagnoses_list.append((
                diagnosis["id"],
                symptoms_str,
                chronic_diseases_str,
                allergies_str,
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


# ==================== MEDICAMENTOS ====================

def obtener_medicamentos_para(condicion):
    """
    Obtiene medicamentos recomendados para una condición
    
    Args:
        condicion: Nombre de la condición
    
    Returns:
        Lista de medicamentos recomendados
    """
    try:
        engine = get_prolog_engine()
        # Usar la consulta medicamentos_para/2
        medicamentos = []
        query = f"medicamentos_para({condicion}, M)"
        for result in engine.prolog.query(query):
            meds = result["M"]
            # Convertir resultado Prolog a Python
            if isinstance(meds, str):
                medicamentos = [m.strip() for m in meds.replace('[', '').replace(']', '').split(',')]
            elif hasattr(meds, '__iter__'):
                medicamentos = list(meds)
        return medicamentos
    except Exception as e:
        print(f"Error obteniendo medicamentos para {condicion}: {e}")
        return []


def obtener_info_medicamento(medicamento):
    """
    Obtiene información detallada de un medicamento
    
    Args:
        medicamento: Nombre del medicamento
    
    Returns:
        Diccionario con tipo, dosis, efectos secundarios
    """
    try:
        engine = get_prolog_engine()
        info = {
            "nombre": medicamento,
            "tipo": None,
            "dosis": None,
            "efectos_secundarios": None,
            "contraindicaciones": []
        }
        
        # Obtener tipo
        for result in engine.prolog.query(f"tipo_medicamento({medicamento}, T)"):
            info["tipo"] = result["T"]
            break
        
        # Obtener dosis
        for result in engine.prolog.query(f"dosis_recomendada({medicamento}, D)"):
            info["dosis"] = result["D"]
            break
        
        # Obtener efectos secundarios
        for result in engine.prolog.query(f"efecto_secundario({medicamento}, E)"):
            info["efectos_secundarios"] = result["E"]
            break
        
        # Obtener contraindicaciones
        contraind = []
        for result in engine.prolog.query(f"contraindicacion({medicamento}, C)"):
            contraind.append(result["C"])
        info["contraindicaciones"] = contraind
        
        return info
    except Exception as e:
        print(f"Error obteniendo información de medicamento {medicamento}: {e}")
        return None


def obtener_todos_medicamentos():
    """
    Obtiene lista de todos los medicamentos disponibles
    
    Returns:
        Lista de nombres de medicamentos
    """
    try:
        engine = get_prolog_engine()
        medicamentos = []
        for result in engine.prolog.query("todos_medicamentos(M)"):
            meds = result["M"]
            if isinstance(meds, str):
                medicamentos = [m.strip().replace("'", "") for m in meds.replace('[', '').replace(']', '').split(',')]
            elif hasattr(meds, '__iter__'):
                medicamentos = list(meds)
            break
        return medicamentos
    except Exception as e:
        print(f"Error obteniendo medicamentos: {e}")
        return []


def obtener_enfermedades_tratadas_por(medicamento):
    """
    Obtiene list de enfermedades que trata un medicamento
    
    Args:
        medicamento: Nombre del medicamento
    
    Returns:
        Lista de enfermedades
    """
    try:
        engine = get_prolog_engine()
        enfermedades = []
        for result in engine.prolog.query(f"enfermedades_tratadas_por({medicamento}, E)"):
            enfs = result["E"]
            if isinstance(enfs, str):
                enfermedades = [e.strip().replace("'", "") for e in enfs.replace('[', '').replace(']', '').split(',')]
            elif hasattr(enfs, '__iter__'):
                enfermedades = list(enfs)
            break
        return enfermedades
    except Exception as e:
        print(f"Error obteniendo enfermedades tratadas por {medicamento}: {e}")
        return []


def sugerir_tratamiento(diagnostico):
    """
    Sugiere medicamentos y tratamiento para un diagnóstico
    
    Args:
        diagnostico: Nombre de la enfermedad/condición
    
    Returns:
        Diccionario con medicamentos y detalles de tratamiento
    """
    medicamentos = obtener_medicamentos_para(diagnostico)
    
    tratamiento = {
        "diagnostico": diagnostico,
        "medicamentos_sugeridos": [],
        "nota_importante": "⚠️ Esta es UNA SUGERENCIA EDUCATIVA solamente. No reemplaza la consulta médica profesional."
    }
    
    for med in medicamentos:
        info = obtener_info_medicamento(med)
        if info:
            tratamiento["medicamentos_sugeridos"].append(info)
    
    return tratamiento


def _normalizar_lista_prolog(items_prolog):
    """
    Convierte resultado de Prolog a lista de Python
    
    Args:
        items_prolog: Resultado de Prolog (puede ser string o iterable)
    
    Returns:
        Lista de strings
    """
    resultado = []
    if isinstance(items_prolog, str):
        items_clean = items_prolog.replace('[', '').replace(']', '').replace("'", '')
        resultado = [item.strip() for item in items_clean.split(',') if item.strip()]
    elif hasattr(items_prolog, '__iter__'):
        resultado = [str(item).strip("'") for item in items_prolog]
    return resultado


def obtener_medicamentos_seguros(diagnostico, alergias=None, enfermedades_cronicas=None):
    """
    Obtiene medicamentos seguros para un diagnóstico, evitando conflictos con
    alergias y enfermedades crónicas del paciente
    
    Args:
        diagnostico: Nombre de la condición/enfermedad
        alergias: Lista de alergias del paciente (ej. ['Penicilina', 'Aspirina'])
        enfermedades_cronicas: Lista de enfermedades crónicas (ej. ['Asma', 'Hipertensión'])
    
    Returns:
        Lista de medicamentos seguros con información completa
    """
    try:
        engine = get_prolog_engine()
        alergias = alergias or []
        enfermedades_cronicas = enfermedades_cronicas or []
        
        # Normalizar nombre de diagnóstico para Prolog
        diagnostico_prolog = engine._to_prolog_atom(diagnostico)
        
        # Convertir listas a formato Prolog
        alergias_prolog = [engine._to_prolog_atom(a) for a in alergias]
        enfermedades_prolog = [engine._to_prolog_atom(e) for e in enfermedades_cronicas]
        
        query = f"medicamentos_seguros_para_paciente({diagnostico_prolog}, [{', '.join(alergias_prolog)}], [{', '.join(enfermedades_prolog)}], M)"
        
        medicamentos_seguros = []
        for result in engine.prolog.query(query):
            meds = result.get("M", [])
            medicamentos_seguros = _normalizar_lista_prolog(meds)
            break
        
        # Agregar información completa de cada medicamento
        medicamentos_info = []
        for med in medicamentos_seguros:
            info = obtener_info_medicamento(med)
            if info:
                medicamentos_info.append(info)
        
        return medicamentos_info
    except Exception as e:
        print(f"Error obteniendo medicamentos seguros para {diagnostico}: {e}")
        return []


def obtener_medicamentos_bloqueados(diagnostico, alergias=None, enfermedades_cronicas=None):
    """
    Obtiene medicamentos bloqueados para un diagnóstico, indicando el motivo
    (alergia o enfermedad crónica que causa conflicto)
    
    Args:
        diagnostico: Nombre de la condición/enfermedad
        alergias: Lista de alergias del paciente (ej. ['Penicilina'])
        enfermedades_cronicas: Lista de enfermedades crónicas (ej. ['Asma'])
    
    Returns:
        Lista de dicts con estructura:
        [
            {
                "medicamento": "amoxicilina",
                "tipo": "Antibiótico",
                "motivo": "alergia",
                "razon": "Penicilina",
                "contraindicacion": "alergia_penicilina"
            },
            ...
        ]
    """
    try:
        engine = get_prolog_engine()
        alergias = alergias or []
        enfermedades_cronicas = enfermedades_cronicas or []
        
        # Normalizar nombre de diagnóstico para Prolog
        diagnostico_prolog = engine._to_prolog_atom(diagnostico)
        
        # Convertir listas a formato Prolog
        alergias_prolog = [engine._to_prolog_atom(a) for a in alergias]
        enfermedades_prolog = [engine._to_prolog_atom(e) for e in enfermedades_cronicas]
        
        query = f"medicamentos_bloqueados_para_paciente({diagnostico_prolog}, [{', '.join(alergias_prolog)}], [{', '.join(enfermedades_prolog)}], M)"
        
        medicamentos_bloqueados_raw = []
        for result in engine.prolog.query(query):
            meds = result.get("M", [])
            medicamentos_bloqueados_raw = _normalizar_lista_prolog(meds)
            break
        
        # Procesar resultados y extraer información
        medicamentos_bloqueados = []
        for med_raw in medicamentos_bloqueados_raw:
            # Parsear estructura med_bloqueado(nombre, motivo(...))
            if 'med_bloqueado(' in str(med_raw):
                try:
                    # Extraer nombre de medicamento y motivo
                    parts = str(med_raw).split('med_bloqueado(')[1].rstrip(')').split(',', 1)
                    med_nombre = parts[0].strip("'")
                    motivo_raw = parts[1].strip() if len(parts) > 1 else ""
                    
                    # Parsear motivo(tipo, razon)
                    if 'motivo(' in motivo_raw:
                        motivo_parts = motivo_raw.split('motivo(')[1].rstrip(')').split(',')
                        motivo_tipo = motivo_parts[0].strip("'")
                        razon = motivo_parts[1].strip().strip("'") if len(motivo_parts) > 1 else ""
                        
                        info_med = obtener_info_medicamento(med_nombre)
                        if info_med:
                            medicamentos_bloqueados.append({
                                "medicamento": med_nombre,
                                "tipo": info_med.get("tipo", "Desconocido"),
                                "motivo": motivo_tipo,
                                "razon": razon,
                                "contraindicaciones": info_med.get("contraindicaciones", [])
                            })
                except Exception as parse_e:
                    print(f"Error parseando medicamento bloqueado {med_raw}: {parse_e}")
                    continue
        
        return medicamentos_bloqueados
    except Exception as e:
        print(f"Error obteniendo medicamentos bloqueados para {diagnostico}: {e}")
        return []


def sugerir_tratamiento_seguro(diagnostico, alergias=None, enfermedades_cronicas=None):
    """
    Sugiere medicamentos de forma segura para un diagnóstico, considerando
    el perfil clínico del paciente (alergias y enfermedades crónicas)
    
    Args:
        diagnostico: Nombre de la enfermedad/condición
        alergias: Lista de alergias del paciente
        enfermedades_cronicas: Lista de enfermedades crónicas
    
    Returns:
        Diccionario con medicamentos seguros y bloqueados con motivos
    """
    alergias = alergias or []
    enfermedades_cronicas = enfermedades_cronicas or []
    
    medicamentos_seguros = obtener_medicamentos_seguros(diagnostico, alergias, enfermedades_cronicas)
    medicamentos_bloqueados = obtener_medicamentos_bloqueados(diagnostico, alergias, enfermedades_cronicas)
    
    resultado = {
        "diagnostico": diagnostico,
        "perfil_paciente": {
            "alergias": alergias,
            "enfermedades_cronicas": enfermedades_cronicas
        },
        "medicamentos_seguros": medicamentos_seguros,
        "medicamentos_bloqueados": medicamentos_bloqueados,
        "resumen": {
            "total_opciones": len(medicamentos_seguros) + len(medicamentos_bloqueados),
            "medicamentos_disponibles": len(medicamentos_seguros),
            "medicamentos_contraindicados": len(medicamentos_bloqueados)
        },
        "nota_importante": "⚠️ Esta es UNA SUGERENCIA EDUCATIVA solamente. No reemplaza la consulta médica profesional."
    }
    
    return resultado


# Inicializar datos al importar el módulo
initialize_data()
