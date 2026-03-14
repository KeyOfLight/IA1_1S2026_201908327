#!/usr/bin/env python3
"""
Test para validar las nuevas funciones:
- obtener_medicamentos_seguros
- obtener_medicamentos_bloqueados
- sugerir_tratamiento_seguro
"""

from database import obtener_medicamentos_seguros, obtener_medicamentos_bloqueados, sugerir_tratamiento_seguro

def test_medicamentos_seguros():
    """Test 1: Medicamentos seguros sin conflictos"""
    print('=' * 70)
    print('TEST 1: Medicamentos SEGUROS (Gripe sin alergias ni condiciones)')
    print('=' * 70)
    
    seguros = obtener_medicamentos_seguros('gripe', [], [])
    print(f'Total medicamentos seguros para gripe: {len(seguros)}')
    if seguros:
        print('\nPrimeros 3 medicamentos:')
        for med in seguros[:3]:
            print(f'  [OK] {med.get("nombre")}: {med.get("tipo")}')
            print(f'       Dosis: {med.get("dosis")}')
    print()

def test_medicamentos_bloqueados():
    """Test 2: Medicamentos bloqueados por conflictos"""
    print('=' * 70)
    print('TEST 2: Medicamentos BLOQUEADOS (Faringitis con alergia Penicilina)')
    print('=' * 70)
    
    bloqueados = obtener_medicamentos_bloqueados('faringitis', ['Penicilina'], [])
    print(f'Total medicamentos bloqueados: {len(bloqueados)}')
    if bloqueados:
        print('\nMedicamentos contraindicados:')
        for med in bloqueados:
            print(f'  [NO] {med.get("medicamento")} ({med.get("tipo")})')
            print(f'       Motivo: {med.get("motivo")}')
            print(f'       Razon: {med.get("razon")}')
    print()

def test_sugerencia_completa():
    """Test 3: Sugerencia segura completa"""
    print('=' * 70)
    print('TEST 3: SUGERENCIA COMPLETA SEGURA')
    print('Diagnostico: Gripe')
    print('Alergia: Aspirina')
    print('Enfermedad cronica: Asma')
    print('=' * 70)
    
    resultado = sugerir_tratamiento_seguro('gripe', ['Aspirina'], ['Asma'])
    
    print(f'\nDiagnostico: {resultado["diagnostico"]}')
    print(f'Perfil del paciente:')
    print(f'  - Alergias: {resultado["perfil_paciente"]["alergias"]}')
    print(f'  - Enfermedades cronicas: {resultado["perfil_paciente"]["enfermedades_cronicas"]}')
    
    print(f'\nResumen:')
    print(f'  - Total opciones: {resultado["resumen"]["total_opciones"]}')
    print(f'  - Medicamentos disponibles: {resultado["resumen"]["medicamentos_disponibles"]}')
    print(f'  - Medicamentos contraindicados: {resultado["resumen"]["medicamentos_contraindicados"]}')
    
    print(f'\nMedicamentos SEGUROS ({len(resultado["medicamentos_seguros"])}):')
    for med in resultado["medicamentos_seguros"][:3]:
        print(f'  [OK] {med.get("nombre")}: {med.get("tipo")}')
    
    print(f'\nMedicamentos BLOQUEADOS ({len(resultado["medicamentos_bloqueados"])}):')
    for med in resultado["medicamentos_bloqueados"]:
        print(f'  [NO] {med.get("medicamento")}: Razon = {med.get("razon")}')
    
    print()

if __name__ == "__main__":
    try:
        test_medicamentos_seguros()
        test_medicamentos_bloqueados()
        test_sugerencia_completa()
        print('=' * 70)
        print('[EXITOSO] Todos los tests completados correctamente')
        print('=' * 70)
    except Exception as e:
        print(f'\n[ERROR] Error durante los tests: {e}')
        import traceback
        traceback.print_exc()

