# Sugerencia Segura de Medicamentos

## Estado: ✅ IMPLEMENTADO

Implementación completa de filtrado inteligente de medicamentos que:
- ✅ Retorna **medicamentos seguros** (sin conflictos)
- ✅ Retorna **medicamentos bloqueados** con motivo (alergia o enfermedad)
- ✅ Normaliza términos automáticamente
- ✅ Proporciona información completa (tipo, dosis, efectos, contraindicaciones)

## Funciones Principales

### 1. `obtener_medicamentos_seguros()`
Devuelve medicamentos que tratan el diagnóstico SIN conflictos con alergias/enfermedades.

**Uso:**
```python
from database import obtener_medicamentos_seguros

medicamentos = obtener_medicamentos_seguros(
    diagnostico='gripe',
    alergias=['Aspirina'],
    enfermedades_cronicas=['Asma']
)

# Retorna:
# [
#     {"nombre": "paracetamol", "tipo": "Analgesico", "dosis": "...", ...},
#     {"nombre": "ibuprofeno", "tipo": "Antiinflamatorio", "dosis": "...", ...}
# ]
```

### 2. `obtener_medicamentos_bloqueados()`
Retorna medicamentos que TIENEN conflictos, especificando el motivo.

**Uso:**
```python
from database import obtener_medicamentos_bloqueados

bloqueados = obtener_medicamentos_bloqueados(
    diagnostico='faringitis',
    alergias=['Penicilina'],
    enfermedades_cronicas=[]
)

# Retorna:
# [
#     {
#         "medicamento": "amoxicilina",
#         "tipo": "Antibiótico",
#         "motivo": "alergia",
#         "razon": "Penicilina",
#         "contraindicaciones": ["alergia_penicilina"]
#     }
# ]
```

### 3. `sugerir_tratamiento_seguro()`
Sugerencia COMPLETA en una sola llamada: medicamentos seguros + bloqueados + resumen.

**Uso:**
```python
from database import sugerir_tratamiento_seguro

resultado = sugerir_tratamiento_seguro(
    diagnostico='gripe',
    alergias=['Aspirina'],
    enfermedades_cronicas=['Asma']
)

# Estructura completa:
resultado = {
    "diagnostico": "gripe",
    "perfil_paciente": {
        "alergias": ["Aspirina"],
        "enfermedades_cronicas": ["Asma"]
    },
    "medicamentos_seguros": [...],  # Con información completa
    "medicamentos_bloqueados": [...],  # Con motivo
    "resumen": {
        "total_opciones": 2,
        "medicamentos_disponibles": 1,
        "medicamentos_contraindicados": 1
    }
}
```

## Características

### Normalización Automática
- Convierte "Penicilina" → "alergia_penicilina"
- Convierte "Hipertensión" → "hipertension"
- Maneja espacios y mayúsculas automáticamente

### Base de Datos de Contraindicaciones
Definidas en `diagnostic_rules.pl`:

| Medicamento | Contraindicado por | Razón |
|---|---|---|
| amoxicilina | alergia_penicilina | Alergia |
| ibuprofeno | ulcera_activa | Úlcera activa |
| metoprolol | asma | Asma |
| aspirina | insuficiencia_renal_severa | Insuficiencia renal |
| metformina | enfermedad_hepatica | Enfermedad hepática |

### Medicamentos Disponibles
31 medicamentos completamente documentados con:
- Categoría terapéutica
- Dosis recomendada para adultos
- Efectos secundarios comunes
- Contraindicaciones específicas
- Enfermedades que tratan

## Validación

Tests incluidos en `test_medicamentos_seguros.py`:

```bash
cd h:\Usac\IA1\P1\backend
python test_medicamentos_seguros.py
```

**Resultados esperados:**
- ✓ TEST 1: Medicamentos SEGUROS (gripe)
- ✓ TEST 2: Medicamentos BLOQUEADOS (faringitis + alergia penicilina)
- ✓ TEST 3: SUGERENCIA COMPLETA SEGURA (múltiples condiciones)

## Integración en UI

Para integrar en `patient_module.py`:

```python
from prolog_engine import get_prolog_engine

engine = get_prolog_engine()

# O desde database.py también está disponible
from database import sugerir_tratamiento_seguro

tratamiento = sugerir_tratamiento_seguro(
    diagnostico=diagnostico_resultado,
    alergias=self.allergies_list,
    enfermedades_cronicas=self.chronic_diseases_list
)
```

## Consideraciones Clínicas

⚠️ **IMPORTANTE**: Esta sugerencia es **EDUCATIVA SOLAMENTE**
- No reemplaza consulta médica profesional
- Basada en contraindicaciones conocidas
- Recomendación clínica debe validarla un profesional de salud

## Próximas Mejoras (Opcionales)

- [ ] Agregar interacciones medicamento-medicamento
- [ ] Agregar categorización por severidad de contraindicación
- [ ] Panel visual de "Seguro/Bloqueado" en interfaz
- [ ] Historial de medicamentos rechazados/aceptados
- [ ] Base de datos expandible de más medicamentos
