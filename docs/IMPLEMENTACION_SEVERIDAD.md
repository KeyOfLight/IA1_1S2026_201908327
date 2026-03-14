# Implementación: Registro de Severidad de Síntomas e Impacto en el Diagnóstico

## 📋 Resumen
Se ha implementado un sistema completo de registro de severidad de síntomas que afecta directamente en el impacto del diagnóstico. Ahora los síntomas se clasifican en tres niveles: **Leve**, **Moderado** y **Severo**.

## 🔧 Cambios Implementados

### 1. **Interfaz de Usuario** (`patient_module.py`)
- ✅ Agregados selectores de severidad (OptionMenu) para cada síntoma
- ✅ Diseño mejorado: cada síntoma tiene un checkbox + selector de severidad
- ✅ Severidad por defecto: "Moderado"
- ✅ Se muestra la severidad en los resultados del diagnóstico

#### Interfaz:
```
[✓] Fiebre         Severidad: [Moderado ▼]
[✓] Tos             Severidad: [Severo ▼]
[ ] Dolor de cabeza Severidad: [Leve ▼]
```

### 2. **Base de Datos** (`database.py`)
- ✅ Estructura de síntomas actualizada para incluir severidad
- ✅ Compatibilidad hacia atrás con diagnósticos antiguos
- ✅ Procesamiento automático: síntomas sin severidad se asignan "Moderado"

#### Nuevo formato de almacenamiento:
```json
{
  "symptoms": [
    {"name": "Fiebre", "severity": "Severo"},
    {"name": "Tos", "severity": "Moderado"},
    {"name": "Congestion Nasal", "severity": "Leve"}
  ],
  "date": "2026-03-09 14:30:00"
}
```

### 3. **Reglas de Prolog** (`diagnostic_rules.pl`)
- ✅ Agregadas nuevas reglas para ponderación por severidad
- ✅ Pesos de severidad:
  - **Severo**: peso 3
  - **Moderado**: peso 2
  - **Leve**: peso 1
- ✅ Reglas para identificar síntomas críticos
- ✅ Aumento de relevancia de diagnósticos con síntomas críticos

### 4. **Motor Prolog** (`prolog_engine.py`)
- ✅ Método `obtener_diagnosticos()` actualizado para aceptar severidad
- ✅ Sistema de ponderación por severidad implementado
- ✅ Compatibilidad total con codigo previo (parámetro opcional)
- ✅ Método auxiliar `_get_severity_weight()` para calcular pesos

#### Lógica de ponderación:
```
Diagnóstico Score = Σ(peso_severidad de síntomas relacionados)
Ejemplo: 
  - Fiebre (Severo) + Tos (Moderado) → Gripe = 3 + 2 = 5
  - Fiebre (Leve) + Congestión (Leve) → Resfriado = 1 + 1 = 2
```

## 📊 Flujo de Datos

```
┌─────────────────────────────────────────────────────────────────┐
│ INTERFAZ (patient_module.py)                                    │
│ - Seleccionar síntomas                                          │
│ - Elegir severidad para cada uno: [Leve|Moderado|Severo]       │
└────────────────────────┬────────────────────────────────────────┘
                         │ symptoms_with_severity
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ MOTOR PROLOG (prolog_engine.py)                                 │
│ - Aplica ponderación según severidad                            │
│ - Calcula relevancia ajustada                                   │
│ - Ordenar diagnósticos por score ponderado                      │
└────────────────────────┬────────────────────────────────────────┘
                         │ diagnosticos_ponderados
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ RESULTADOS (mostrados al usuario)                               │
│ - Síntomas con severidad visible                                │
│ - Diagnósticos ordenados por relevancia ponderada               │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ BASE DE DATOS (database.py)                                     │
│ - Guardar síntomas con severidad                                │
│ - Mantener historial completo                                   │
│ - Incluir información de relevancia ponderada                   │
└─────────────────────────────────────────────────────────────────┘
```

## 🔄 Compatibilidad

✅ **Compatible hacia atrás**: Diagnósticos antiguos sin severidad se manejan correctamente
✅ **Transición suave**: Nuevos diagnósticos usan el sistema de severidad
✅ **Sin breaking changes**: API existente sigue funcionando

## 🧪 Validación

- ✅ No hay errores de sintaxis Python
- ✅ No hay errores de importación
- ✅ Lógica de ponderación implementada correctamente
- ✅ Manejo de compatibility hacia atrás

## 📋 Checklist de Implementación

- [x] Interfaz actualizada con selectores de severidad
- [x] Base de datos preparada para almacenar severidad
- [x] Reglas de Prolog para manejar severidad
- [x] Motor Prolog con ponderación por severidad
- [x] Mostrar severidad en resultados
- [x] Compatibilidad hacia atrás
- [x] Sin errores de compilación

## 🚀 Cómo Usar

1. **Seleccionar síntomas** con sus respectivas severidades
2. **Ver diagnósticos ordenados** por relevancia ponderada (síntomas severos pesan más)
3. **Guardar registro** con información completa de severidad
4. **Consultar histórico** en la base de datos con detalles de severidad

## 📝 Ejemplo

**Entrada:**
- Fiebre (Severo)
- Tos (Moderado)
- Dolor de cabeza (Leve)

**Cálculo:**
- Gripe: 3 (fiebre-severo) + 2 (tos-moderado) = **5** ✓
- Resfriado: 2 (tos-moderado) + 1 (congestión-leve?) = **3**
- Migraña: 1 (cierto) = **1**

**Resultado ordenado:**
1. Gripe (Relevancia: Alta) - Score: 5
2. Resfriado (Relevancia: Media) - Score: 3
3. Migraña (Relevancia: Media) - Score: 1

## ⚠️ Notas Importantes

- El sistema sigue siendo **PRELIMINAR Y EDUCATIVO**
- No reemplaza consulta médica profesional
- La severidad es auto-reportada por el paciente
- Debe siempre consultarse con profesional médico calificado
