# Implementación: Hechos en Prolog de Enfermedades, Síntomas y Medicamentos

## 📋 Resumen
Se ha implementado una base de conocimientos completa en Prolog con hechos y reglas para enfermedades, síntomas y medicamentos. El sistema ahora puede recomendar tratamientos farmacológicos basados en diagnósticos.

## 🔧 Componentes Implementados

### 1. **Síntomas** (Ya existía)
- ✅ 10+ síntomas definidos como hechos
- ✅ Descripciones detalladas de cada síntoma
- ✅ Clasificación de severidad (alta, media, baja)

### 2. **Enfermedades/Condiciones** (Ya existía)
- ✅ 30+ condiciones médicas definidas
- ✅ Clasificación de urgencia
- ✅ Relaciones síntoma-condición

### 3. **Medicamentos** (NUEVO)
- ✅ 31 medicamentos registrados
- ✅ Categorización por tipo terapéutico
- ✅ Dosis recomendadas para adultos
- ✅ Información de efectos secundarios
- ✅ Contraindicaciones
- ✅ Relaciones medicamento-enfermedad

## 📊 Estructura de Medicamentos en Prolog

### Hechos Básicos
```prolog
medicamento(paracetamol, analgesico_antipiretico).
medicamento(ibuprofeno, antiinflamatorio_analgesico).
medicamento(amoxicilina, antibiotico_penicilina).
... (31 medicamentos total)
```

### Tipos Disponibles de Medicamentos

| Categoría | Ejemplos |
|-----------|----------|
| **Analgésicos/Antitérmicos** | paracetamol |
| **Antiinflamatorios (AINE)** | ibuprofeno, aspirina, diclofenaco, meloxicam |
| **Antibióticos** | amoxicilina, azitromicina |
| **Inhibidores de Bomba de Protones** | omeprazol |
| **Antagonistas H2** | ranitidina |
| **Antidiabéticos** | metformina |
| **Antihipertensivos** | metoprolol, atenolol, losartan, enalapril |
| **Antihistamínicos** | loratadina, fexofenadina |
| **Broncodilatadores** | salbutamol |
| **Corticosteroides** | fluticasona |
| **Antidepresivos** | sertralina, fluoxetina, trazodona |
| **Mucolíticos** | acetilcisteina, carbocisteina |
| **Antidiarreicos** | loperamida, bismuto_subsalicilato |
| **Antiméticos** | metoclopramida, ondansetron, domperidona |

### Relaciones Medicamento-Enfermedad

```prolog
trata(paracetamol, gripe).
trata(paracetamol, resfriado).
trata(paracetamol, 'migraña').
trata(paracetamol, tension).
... (60+ relaciones)
```

**Ejemplos de cobertura:**
- **Gripe**: 2 medicamentos (paracetamol, ibuprofeno)
- **Hipertensión**: 4 medicamentos (metoprolol, atenolol, losartan, enalapril)
- **Alergia**: 2 medicamentos (loratadina, fexofenadina)
- **Asma**: 3 medicamentos (salbutamol, fluticasona, acetilcisteina)
- **Depresión**: 3 medicamentos (sertralina, fluoxetina, trazodona)

### Dosis Recomendadas

Ejemplo:
```prolog
dosis_recomendada(paracetamol, '500-1000 mg cada 6-8 horas (máx 4g/día)').
dosis_recomendada(ibuprofeno, '200-400 mg cada 6-8 horas (máx 1.2g/día)').
dosis_recomendada(amoxicilina, '250-500 mg cada 8 horas (depende condición)').
```

### Efectos Secundarios

```prolog
efecto_secundario(ibuprofeno, 'Molestias gastricas, mareos, erupcion cutanea').
efecto_secundario(amoxicilina, 'Molestias estomacales, diarrea, alergia/erupcion').
efecto_secundario(sertralina, 'Insomnio, nauseas, disfuncion sexual').
```

### Contraindicaciones

```prolog
contraindicacion(aspirina, ulcera_activa).
contraindicacion(ibuprofeno, insuficiencia_renal_severa).
contraindicacion(metformina, insuficiencia_renal_severa).
contraindicacion(metoprolol, asma).
```

## 🐍 Consultas Prolog Disponibles

### Consultas Básicas
```prolog
% Obtener medicamentos para una enfermedad
?- medicamentos_para(gripe, M).
M = [paracetamol, ibuprofeno].

% Obtener todas las enfermedades que trata un medicamento
?- enfermedades_tratadas_por(paracetamol, E).
E = [gripe, resfriado, 'migraña', tension].

% Verificar si un medicamento trata una enfermedad
?- trata_enfermedad(ibuprofeno, gripe).
true.

% Obtener información completa de un medicamento
?- info_medicamento(paracetamol, Tipo, Dosis, Efectos).
Tipo = 'Analgesico/Antipiretico',
Dosis = '500-1000 mg cada 6-8 horas (máx 4g/día)',
Efectos = 'Raramente: erupcion cutanea, reacciones alergicas'.

% Verificar contraindicaciones
?- tiene_contraindicacion(ibuprofeno, asma).
false.

% Obtener todos los medicamentos
?- todos_medicamentos(M).
M = [paracetamol, ibuprofeno, aspirina, ...].

% Medicamentos seguros (sin contraindicaciones)
?- medicamento_seguro(paracetamol).
true.
```

## 🐍 API Python - database.py

### Funciones Disponibles

**1. Obtener medicamentos para una enfermedad**
```python
medicamentos = obtener_medicamentos_para("gripe")
# Retorna: ['paracetamol', 'ibuprofeno']
```

**2. Obtener información detallada de medicamento**
```python
info = obtener_info_medicamento("ibuprofeno")
# Retorna:
# {
#   'nombre': 'ibuprofeno',
#   'tipo': 'Antiinflamatorio (AINE)',
#   'dosis': '200-400 mg cada 6-8 horas...',
#   'efectos_secundarios': 'Molestias gastricas...',
#   'contraindicaciones': ['ulcera_activa', 'insuficiencia_renal_severa', ...]
# }
```

**3. Obtener todos los medicamentos**
```python
todos = obtener_todos_medicamentos()
# Retorna lista de 31 medicamentos
```

**4. Obtener enfermedades tratadas por medicamento**
```python
enfermedades = obtener_enfermedades_tratadas_por("paracetamol")
# Retorna: ['gripe', 'resfriado', 'migraña', 'tension']
```

**5. Sugerir tratamiento completo**
```python
tratamiento = sugerir_tratamiento("gripe")
# Retorna:
# {
#   'diagnostico': 'gripe',
#   'medicamentos_sugeridos': [
#     {
#       'nombre': 'paracetamol',
#       'tipo': '...',
#       'dosis': '...',
#       'efectos_secundarios': '...',
#       'contraindicaciones': [...]
#     },
#     ...
#   ],
#   'nota_importante': '⚠️ Esta es UNA SUGERENCIA EDUCATIVA...'
# }
```

## 🐍 API Python - prolog_engine.py

### Métodos del Motor Prolog

```python
engine = PrologDiagnosticEngine()

# Obtener medicamentos
medicamentos = engine.obtener_medicamentos_para("hipertension")

# Obtener información
tipo = engine.obtener_tipo_medicamento("metoprolol")
dosis = engine.obtener_dosis_medicamento("amoxicilina")
efectos = engine.obtener_efectos_secundarios("sertralina")

# Contraindicaciones
contraindicaciones = engine.obtener_contraindicaciones("ibuprofeno")

# Todos los medicamentos
todos = engine.obtener_todos_medicamentos()
```

## 📊 Estadísticas

| Concepto | Cantidad |
|----------|----------|
| **Síntomas** | 10+ |
| **Enfermedades/Condiciones** | 30+ |
| **Medicamentos** | 31 |
| **Relaciones medicamento-enfermedad** | 60+ |
| **Medicamentos con información completa** | 31 |
| **Medicamentos con contraindicaciones** | 14 |

## 🚀 Ejemplos de Uso

### Ejemplo 1: Sugerir medicamentos para gripe
```python
tratamiento = sugerir_tratamiento("gripe")

# Muestra:
# - Paracetamol: 500-1000 mg cada 6-8 horas
# - Ibuprofeno: 200-400 mg cada 6-8 horas
#   ⚠️ Contraindicaciones: ulcera_activa, insuficiencia_renal_severa
```

### Ejemplo 2: Consultar información detallada
```python
info = obtener_info_medicamento("omeprazol")

# Muestra:
# Tipo: Inhibidor de Bomba de Protones
# Dosis: 20-40 mg una vez diaria
# Para tratar: gastritis, ulcera, reflujo_gastrico
```

### Ejemplo 3: Verificar medicamentos seguros
```python
# En Prolog:
medicamento_seguro(X)  # Encuentra medicamentos sin contraindicaciones conocidas
```

## ✅ Validación

- ✅ 31 medicamentos definidos correctamente
- ✅ Todos los medicamentos tienen tipo definido
- ✅ Dosis recomendadas para la mayoría de medicamentos
- ✅ Información de efectos secundarios
- ✅ Contraindicaciones identificadas
- ✅ Relaciones medicamento-enfermedad establecidas
- ✅ Sin errores de sintaxis Prolog
- ✅ API Python completamente funcional
- ✅ Pruebas ejecutadas exitosamente

## ⚠️ Notas Importantes

1. **Esta es una base de datos EDUCATIVA**
2. **No sustituye consulta médica profesional**
3. **Las dosis son para adultos en condiciones normales**
4. **Consultar siempre con farmacéutico o médico**
5. **Las contraindicaciones son básicas, existen muchas más**
6. **Los efectos secundarios son los más comunes reportados**

## 📝 Próximos Pasos Sugeridos

- [ ] Agregar más medicamentos específicos
- [ ] Incluir interacciones entre medicamentos
- [ ] Agregar información de categoría de embarazo (A, B, C, D, X)
- [ ] Incluir datos de farmacocinética
- [ ] Agregar equivalencias genéricas
- [ ] Sistema de alertas por alergias
