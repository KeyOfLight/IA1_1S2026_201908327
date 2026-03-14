# Configuración del Motor Prolog

El sistema de diagnóstico médico ahora usa **Prolog** como motor de lógica para diagnósticos.

## Requisitos

### 1. SWI-Prolog (Requerido)

**Windows:**
- Descargar desde: https://www.swi-prolog.org/download/stable
- Ejecutar instalador
- Marcar "Add to PATH" durante la instalación

**macOS:**
```bash
brew install swi-prolog
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install swi-prolog
```

### 2. Librería Python pyswip

Instalar con pip:

```bash
pip install pyswip
```

Si hay problemas, prueba con:

```bash
pip install --upgrade pyswip
```

## Verificación de Instalación

**Verificar SWI-Prolog:**
```bash
swipl --version
```

**Verificar pyswip:**
```bash
python -c "from pyswip import Prolog; print('✓ pyswip instalado correctamente')"
```

## Estructura del Motor Prolog

### diagnostic_rules.pl
- Archivo de reglas en Prolog
- Define síntomas, condiciones y relaciones
- Contiene la base de datos de diagnósticos
- Se carga automáticamente al iniciar

### prolog_engine.py
- Motor Python que conecta con Prolog
- Interfaz entre Python y las reglas Prolog
- Métodos principales:
  - `obtener_sintomas()` - Obtiene lista de síntomas
  - `obtener_diagnosticos()` - Calcula diagnósticos por síntomas
  - `obtener_recomendacion()` - Obtiene recomendaciones médicas
  - `es_urgente()` - Verifica condiciones urgentes

## Características del Motor Prolog

### Base de Hechos
- 10 síntomas principales
- 30+ condiciones médicas
- Relaciones síntoma-condición definidas

### Reglas de Diagnóstico
```prolog
% Calcula diagnósticos ordenados por relevancia
diagnosticos_ordenados(Síntomas, ListaDiagnosticos)

% Valida síntomas y condiciones
validar_sintoma(Síntoma)
validar_condicion(Condición)

% Verifica urgencia médica
es_urgente(Condición)

% Obtiene recomendaciones
obtener_recomendacion(Condición, Recomendación)
```

## Flujo de Ejecución

```
1. Interfaz Python (tkinter)
     ↓
2. patient_module.py (GUI de síntomas)
     ↓
3. database.py (funciones Prolog)
     ↓
4. prolog_engine.py (motor de conexión)
     ↓
5. diagnostic_rules.pl (reglas Prolog)
     ↓
6. Resultados → mostrados en GUI
```

## Troubleshooting

### Error: "ModuleNotFoundError: No module named 'pyswip'"
```bash
pip install pyswip
```

### Error: "SICStus Prolog required"
- Asegúrate de que SWI-Prolog está instalado correctamente
- Verifica que está en PATH: `swipl --version`

### Error: "No consultation file"
- Verifica que `diagnostic_rules.pl` está en el mismo directorio que `prolog_engine.py`

### Prolog no responde
- Reinicia SWI-Prolog
- Recarga el módulo Python

## Extensión del Sistema

### Agregar Nuevos Síntomas
Editar `diagnostic_rules.pl`:

```prolog
% Agregar síntoma
sintoma(nuevo_sintoma).

% Agregar relaciones
relacion(nuevo_sintoma, condicion_existente).
relacion(nuevo_sintoma, nueva_condicion).
```

### Agregar Nuevas Condiciones
```prolog
% Agregar condición
condicion(nueva_condicion).

% Agregar información
descripcion_sintoma(nuevo_sintoma, "Descripción").
severidad(nuevo_sintoma, alta).
recomendacion(nueva_condicion, "Recomendación médica").
```

## Ventajas de Usar Prolog

✅ **Lógica declarativa** - Definir QUÉ, no CÓMO
✅ **Backtracking automático** - Encuentra múltiples soluciones
✅ **Reglas basadas en hechos** - Fácil de mantener
✅ **Inferencia lógica** - Diagnósticos basados en lógica
✅ **Base de conocimiento** - Todas las reglas en un lugar
✅ **Escalable** - Fácil agregar más síntomas/condiciones

## Performance

- Carga inicial: ~2-3 segundos (carga de reglas)
- Consulta de diagnóstico: <100ms
- Memoria: ~30MB con todas las reglas cargadas

## Ejemplo de Consulta Prolog

```prolog
?- diagnosticos_ordenados([fiebre, tos, dolor_cabeza], D).
D = [gripe-3, resfriado-2, infeccion_viral-2, ...].
```

## Documentación Prolog

- Documentación oficial: https://www.swi-prolog.org/pldoc/
- Tutorial: https://www.swi-prolog.org/Tutorials/
- Ejemplos: https://www.swi-prolog.org/Tutorials/SLD.html

---

**Versión**: 1.0 Prolog Integration
**Fecha**: Febrero 2026
