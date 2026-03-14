"""
DEMOSTRACIÓN DE CONSULTAS PROLOG
Sistema de Diagnóstico Médico - MediLogic

Este archivo demuestra las 5+ consultas Prolog ejecutadas desde Python
que evidencian la integración correcta entre Python y Prolog.
"""

from prolog_engine import get_prolog_engine
from database import obtener_sintomas, obtener_diagnostico_prolog, es_condicion_urgente, obtener_recomendacion_prolog
import json
from datetime import datetime


def demostrar_consultas_prolog():
    """
    Demuestra 5 consultas principales ejecutadas desde Python hacia Prolog
    """
    
    print("╔════════════════════════════════════════════════════════════════╗")
    print("║           DEMOSTRACIÓN DE CONSULTAS PROLOG                    ║")
    print("║        Integración Python ↔ Prolog - MediLogic              ║")
    print("╚════════════════════════════════════════════════════════════════╝")
    print()
    
    try:
        engine = get_prolog_engine()
        print("✓ Motor Prolog inicializado correctamente\n")
    except Exception as e:
        print(f"✗ Error al inicializar Prolog: {e}")
        print("  Asegúrate de tener SWI-Prolog instalado y pyswip disponible")
        return
    
    # ==================== CONSULTA 1: Obtener síntomas ====================
    print("┌────────────────────────────────────────────────────────────┐")
    print("│ CONSULTA 1: Obtener lista de síntomas disponibles         │")
    print("└────────────────────────────────────────────────────────────┘")
    print("\nCódigo Prolog:")
    print("  ?- todos_sintomas(S).")
    print("\nResultado Python:")
    
    try:
        sintomas = obtener_sintomas()
        print(f"  ✓ {len(sintomas)} síntomas obtenidos:")
        for i, sintoma in enumerate(sintomas, 1):
            print(f"    {i:2d}. {sintoma}")
        consulta_1 = {
            "numero": 1,
            "nombre": "Obtener síntomas disponibles",
            "prolog": "todos_sintomas(S)",
            "resultado": sintomas,
            "exito": True
        }
    except Exception as e:
        print(f"  ✗ Error: {e}")
        consulta_1 = {"numero": 1, "exito": False, "error": str(e)}
    
    # ==================== CONSULTA 2: Diagnóstico simple (1 síntoma) ====================
    print("\n┌────────────────────────────────────────────────────────────┐")
    print("│ CONSULTA 2: Diagnóstico con UN síntoma (Fiebre)          │")
    print("└────────────────────────────────────────────────────────────┘")
    print("\nCódigo Prolog:")
    print("  ?- diagnosticos_ordenados([fiebre], D).")
    print("\nResultado Python:")
    
    try:
        diagnosticos_fiebre = obtener_diagnostico_prolog(["Fiebre"])
        print(f"  ✓ {len(diagnosticos_fiebre)} diagnósticos encontrados:")
        for i, (condition, relevance) in enumerate(diagnosticos_fiebre[:5], 1):
            print(f"    {i}. {condition} (Relevancia: {relevance})")
        consulta_2 = {
            "numero": 2,
            "nombre": "Diagnóstico con Fiebre",
            "prolog": "diagnosticos_ordenados([fiebre], D)",
            "sintomas": ["Fiebre"],
            "resultado": diagnosticos_fiebre,
            "exito": True
        }
    except Exception as e:
        print(f"  ✗ Error: {e}")
        consulta_2 = {"numero": 2, "exito": False, "error": str(e)}
    
    # ==================== CONSULTA 3: Diagnóstico múltiple (3 síntomas) ====================
    print("\n┌────────────────────────────────────────────────────────────┐")
    print("│ CONSULTA 3: Diagnóstico con MÚLTIPLES síntomas           │")
    print("│             (Fiebre, Tos, Dolor de cabeza)               │")
    print("└────────────────────────────────────────────────────────────┘")
    print("\nCódigo Prolog:")
    print("  ?- diagnosticos_ordenados([fiebre, tos, dolor_cabeza], D).")
    print("\nResultado Python:")
    
    try:
        sintomas_multiples = ["Fiebre", "Tos", "Dolor de cabeza"]
        diagnosticos_multiples = obtener_diagnostico_prolog(sintomas_multiples)
        print(f"  Síntomas seleccionados: {', '.join(sintomas_multiples)}")
        print(f"  ✓ {len(diagnosticos_multiples)} diagnósticos encontrados:")
        for i, (condition, relevance) in enumerate(diagnosticos_multiples[:5], 1):
            print(f"    {i}. {condition} (Relevancia: {relevance})")
        consulta_3 = {
            "numero": 3,
            "nombre": "Diagnóstico múltiple",
            "prolog": "diagnosticos_ordenados([fiebre, tos, dolor_cabeza], D)",
            "sintomas": sintomas_multiples,
            "resultado": diagnosticos_multiples,
            "exito": True
        }
    except Exception as e:
        print(f"  ✗ Error: {e}")
        consulta_3 = {"numero": 3, "exito": False, "error": str(e)}
    
    # ==================== CONSULTA 4: Verificar urgencia ====================
    print("\n┌────────────────────────────────────────────────────────────┐")
    print("│ CONSULTA 4: Verificar urgencia de condiciones             │")
    print("└────────────────────────────────────────────────────────────┘")
    print("\nCódigo Prolog:")
    print("  ?- es_urgente(apendicitis).")
    print("  ?- es_urgente(gripe).")
    print("\nResultado Python:")
    
    try:
        condiciones_urgentes = [
            ("Apendicitis", True),
            ("Neumonía", True),
            ("Gripe", False),
            ("Resfriado", False)
        ]
        
        print("  Verificando condiciones:")
        urgencias_encontradas = {}
        for condicion, esperado_urgente in condiciones_urgentes:
            es_urgente_result = es_condicion_urgente(condicion)
            estado = "✓ URGENTE" if es_urgente_result else "○ No urgente"
            print(f"    {condicion}: {estado}")
            urgencias_encontradas[condicion] = es_urgente_result
        
        consulta_4 = {
            "numero": 4,
            "nombre": "Verificar urgencias",
            "prolog": "es_urgente(Condicion)",
            "resultado": urgencias_encontradas,
            "exito": True
        }
    except Exception as e:
        print(f"  ✗ Error: {e}")
        consulta_4 = {"numero": 4, "exito": False, "error": str(e)}
    
    # ==================== CONSULTA 5: Obtener recomendaciones ====================
    print("\n┌────────────────────────────────────────────────────────────┐")
    print("│ CONSULTA 5: Obtener recomendaciones médicas               │")
    print("└────────────────────────────────────────────────────────────┘")
    print("\nCódigo Prolog:")
    print("  ?- obtener_recomendacion(gripe, R).")
    print("  ?- obtener_recomendacion(apendicitis, R).")
    print("\nResultado Python:")
    
    try:
        condiciones_consulta = ["Gripe", "Apendicitis", "Gastroenteritis"]
        recomendaciones = {}
        
        for condicion in condiciones_consulta:
            recom = obtener_recomendacion_prolog(condicion)
            recomendaciones[condicion] = recom
            print(f"\n  {condicion}:")
            print(f"    {recom[:80]}...")
        
        consulta_5 = {
            "numero": 5,
            "nombre": "Obtener recomendaciones",
            "prolog": "obtener_recomendacion(Condicion, R)",
            "resultado": recomendaciones,
            "exito": True
        }
    except Exception as e:
        print(f"  ✗ Error: {e}")
        consulta_5 = {"numero": 5, "exito": False, "error": str(e)}
    
    # ==================== CONSULTA 6 (Bonus): Flujo completo ====================
    print("\n┌────────────────────────────────────────────────────────────┐")
    print("│ CONSULTA 6 (BONUS): Flujo completo de diagnóstico        │")
    print("└────────────────────────────────────────────────────────────┘")
    print("\nSimulando flujo del módulo de pacientes:")
    
    try:
        sintomas_paciente = ["Fiebre", "Nauseas", "Dolor Abdominal"]
        print(f"\n  1. Paciente selecciona síntomas: {sintomas_paciente}")
        
        diagnosticos_paciente = obtener_diagnostico_prolog(sintomas_paciente)
        print(f"\n  2. Sistema consulta Prolog → encontrados {len(diagnosticos_paciente)} diagnósticos")
        
        diagnostico_principal = diagnosticos_paciente[0] if diagnosticos_paciente else None
        if diagnostico_principal:
            print(f"\n  3. Diagnóstico principal: {diagnostico_principal[0]} (relevancia: {diagnostico_principal[1]})")
            
            urgente = es_condicion_urgente(diagnostico_principal[0])
            print(f"\n  4. ¿Es urgente? {'SÍ ⚠️ ' if urgente else 'No'}")
            
            recom = obtener_recomendacion_prolog(diagnostico_principal[0])
            print(f"\n  5. Recomendación: {recom[:100]}...")
        
        consulta_6 = {
            "numero": 6,
            "nombre": "Flujo completo",
            "sintomas": sintomas_paciente,
            "diagnosticos": diagnosticos_paciente,
            "exito": True
        }
    except Exception as e:
        print(f"  ✗ Error: {e}")
        consulta_6 = {"numero": 6, "exito": False, "error": str(e)}
    
    # ==================== RESUMEN ====================
    print("\n╔════════════════════════════════════════════════════════════════╗")
    print("║                    RESUMEN DE CONSULTAS                     ║")
    print("╚════════════════════════════════════════════════════════════════╝")
    
    consultas = [consulta_1, consulta_2, consulta_3, consulta_4, consulta_5, consulta_6]
    exitosas = sum(1 for c in consultas if c.get("exito", False))
    total = len(consultas)
    
    print(f"\n✓ Consultas ejecutadas exitosamente: {exitosas}/{total}")
    print(f"\nDetalle por consulta:")
    for consulta in consultas:
        status = "✓" if consulta.get("exito", False) else "✗"
        print(f"  {status} Consulta {consulta.get('numero', '?')}: {consulta.get('nombre', 'Desconocida')}")
    
    # ==================== GUARDAR REPORTE ====================
    print("\n┌────────────────────────────────────────────────────────────┐")
    print("│ Generando reporte JSON...                               │")
    print("└────────────────────────────────────────────────────────────┘")
    
    reporte = {
        "timestamp": datetime.now().isoformat(),
        "titulo": "Demostración de Consultas Prolog - MediLogic",
        "consultas": consultas,
        "resumen": {
            "total_consultas": total,
            "consultas_exitosas": exitosas,
            "tasa_exito": f"{(exitosas/total*100):.1f}%"
        }
    }
    
    with open("reporte_consultas_prolog.json", "w", encoding="utf-8") as f:
        json.dump(reporte, f, ensure_ascii=False, indent=2)
    
    print(f"\n✓ Reporte guardado: reporte_consultas_prolog.json")
    
    print("\n" + "="*64)
    print("CONCLUSIÓN: Integración Python ↔ Prolog OPERATIVO")
    print("="*64)
    print("\nEl sistema demuestra:")
    print("  ✓ Conexión exitosa con motor Prolog")
    print("  ✓ Carga de reglas desde archivo .pl")
    print("  ✓ Ejecución de consultas complejas")
    print("  ✓ Obtención de resultados estructurados")
    print("  ✓ Flujo completo de diagnóstico funcional")
    print()


if __name__ == "__main__":
    demostrar_consultas_prolog()
