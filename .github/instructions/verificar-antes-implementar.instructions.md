---
description: "Use when the user asks to verify whether a feature is already implemented before making changes; enforce a check-first and implement-only-if-missing workflow. Keywords: revisar si esta implementado, verificar implementacion, implementa si falta."
applyTo: "**/*.py"
---
# Regla: verificar antes de implementar

Cuando la solicitud del usuario incluya validar si algo "ya esta implementado" o una variante equivalente:

1. Revisar primero el codigo existente (buscar funciones, endpoints, clases, consultas, reglas o archivos relacionados).
2. Reportar explicitamente si ya existe implementacion completa, parcial o inexistente.
3. Si existe implementacion completa, no duplicar logica; en su lugar, indicar ubicacion exacta y estado.
4. Si existe implementacion parcial, completar solo lo faltante y respetar el estilo del proyecto.
5. Solo crear nueva implementacion cuando no exista una solucion equivalente.
6. Validar el resultado (errores, ejecucion o pruebas disponibles) despues de editar.

## Salida esperada

- Incluir referencias concretas de archivos revisados.
- Explicar brevemente por que se considero existente, parcial o ausente.
- Enumerar cambios aplicados unicamente cuando haya sido necesario implementar.
