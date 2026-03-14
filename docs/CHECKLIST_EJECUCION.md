# CHECKLIST EJECUCIÓN - MediLogic

## ✅ FASE 1: GITHUB + GIT (1 Hora)

### Setup Inicial
- [ ] Crear cuenta GitHub (5 min)
  - [ ] Email confirmado
  - [ ] Usuario listo

- [ ] Instalar Git (5 min)
  - [ ] git --version funciona
  - [ ] Configurar user.name
  - [ ] Configurar user.email

- [ ] Crear repositorio en GitHub (5 min)
  - [ ] Nombre: MediLogic
  - [ ] Public ✓
  - [ ] Copiar URL HTTPS

### Subir Código (30 min)
- [ ] Navegar a: h:\Usac\IA1\P1\backend
- [ ] `git init`
- [ ] `git add .`
- [ ] `git commit -m "Initial commit: MediLogic project structure"`
- [ ] `git remote add origin [TU_URL_HTTPS]`
- [ ] `git branch -M main`
- [ ] `git push -u origin main`
- [ ] Verificar en GitHub que se vea todo

### 5 Commits Adicionales (15 min)
- [ ] Commit 2: diagnostic_rules.pl ("feat: Add Prolog knowledge base...")
- [ ] Commit 3: prolog_engine.py ("feat: Implement Python-Prolog integration...")
- [ ] Commit 4: database.py ("feat: Integrate Prolog queries...")
- [ ] Commit 5: patient_module.py ("feat: Update patient module...")
- [ ] Commit 6: *.md files ("docs: Add complete technical documentation...")
- [ ] `git push origin main` para subir todos

### Colaborador (5 min)
- [ ] Ir a Settings → Collaborators
- [ ] Agregar email del auxiliar
- [ ] Enviar invitación

### Verificación GitHub
- [ ] Ver repositorio públicamente: https://github.com/[TU_USUARIO]/MediLogic
- [ ] Ver historial: 6+ commits visibles
- [ ] Ver archivos: .py, .pl, .md presentes

---

## ✅ FASE 2: SCREENSHOTS (30-45 Minutos)

### Capturas Requeridas (7 Total)

#### 1. Pantalla Principal
- [ ] Ejecutar: `python Main.py`
- [ ] Capturar: Ventana con título "MediLogic", botones "Paciente" y "Médico/Admin"
- [ ] Guardar: 001_main_screen.png

#### 2. Módulo Pacientes - Selección de Síntomas
- [ ] Click botón "Paciente"
- [ ] Capturar: Listbox con síntomas (fiebre, tos, etc.), scroll visible
- [ ] Guardar: 002_paciente_sintomas.png

#### 3. Módulo Pacientes - Resultados
- [ ] Seleccionar síntomas (ej: fiebre, tos)
- [ ] Click "Generar Diagnóstico"
- [ ] Capturar: Tabla con diagnósticos, relevancia, recomendaciones
- [ ] Guardar: 003_paciente_resultados.png

#### 4. Módulo Admin - Login
- [ ] Volver a main → Click "Médico/Admin"
- [ ] Capturar: Pantalla de login (campos usuario/contraseña)
- [ ] Guardar: 004_admin_login.png

#### 5. Módulo Admin - Historial (después de login)
- [ ] User: "medico", Password: "123" (o credenciales de datos.json)
- [ ] Capturar: Tabla de diagnósticos históricos
- [ ] Guardar: 005_admin_historial.png

#### 6. Terminal: Demo Prolog
- [ ] Ejecutar: `python demo_consultas_prolog.py`
- [ ] Capturar: Output mostrando 6 queries ejecutadas
- [ ] Incluir: Síntomas, diagnósticos simples, múltiples, urgencia
- [ ] Guardar: 006_terminal_prolog_demo.png

#### 7. GitHub Repository
- [ ] Abrir navegador: https://github.com/[TU_USUARIO]/MediLogic
- [ ] Capturar: Página principal mostando commits, archivos, colaboradores
- [ ] Guardar: 007_github_repository.png

### Guardado de Archivos
- [ ] Crear carpeta: h:\Usac\IA1\P1\backend\screenshots
- [ ] Guardar 7 imágenes con nombre numerado (001_, 002_, etc.)
- [ ] Verificar que cada captura sea legible
- [ ] Tamaño recomendado: 1920x1080 o similar

---

## ✅ FASE 3: DOCUMENTO PDF (1.5-2 Horas)

### Herramienta Recomendada
- [ ] Google Docs (Google Drive)
  - [ ] Gratis
  - [ ] Colaboración
  - [ ] Export a PDF simple
  
  O:
- [ ] Microsoft Word
- [ ] LibreOffice Writer

### Estructura del PDF (15-20 páginas)

#### Portada (Página 1)
- [ ] Título: "MediLogic: Sistema de Diagnóstico Médico Basado en Prolog"
- [ ] Autores: [Tus nombres]
- [ ] Universidad: USAC
- [ ] Curso: IA1
- [ ] Fecha: Actual
- [ ] Institución: Facultad de Ingeniería

#### Introducción (Página 2)
- [ ] Problema: Diagnóstico médico manual es lento
- [ ] Solución: Sistema automatizado con Prolog
- [ ] Objetivo: Integrar Python + Prolog para diagnóstico

#### Tabla de Contenidos (Página 3)
- [ ] Secciones principales listadas

#### Sección 1: Arquitectura Sistema (Páginas 4-5)
- [ ] Diagrama 1: Python (GUI) ↔ Prolog (Motor)
- [ ] Explicación: 3 capas (Frontend, Backend, Logic)
- [ ] Componentes:
  - [ ] Main.py (entry point)
  - [ ] patient_module.py (UI diagnóstico)
  - [ ] admin_module.py (gestión)
  - [ ] database.py (API)
  - [ ] prolog_engine.py (puente Python-Prolog)
  - [ ] diagnostic_rules.pl (base conocimiento)

#### Sección 2: Base de Conocimiento Prolog (Páginas 6-7)
- [ ] Tabla: Síntomas (10 total con definiciones)
- [ ] Tabla: Condiciones/Enfermedades (30+ listadas)
- [ ] Código Prolog snippet (5-10 líneas principales)
- [ ] Explicación: Cómo se relacionan sintomas ↔ condiciones

#### Sección 3: Integración Python-Prolog (Páginas 8-9)
- [ ] Diagrama: Flujo de datos
- [ ] Código: Función `prolog_engine.py` principal
- [ ] Conversión: Tipos Python ↔ Prolog
- [ ] Ejemplo: Query y resultado

#### Sección 4: Módulo Pacientes (Página 10)
- [ ] Screenshot: Pantalla selección síntomas
- [ ] Screenshot: Resultados diagnóstico
- [ ] Explicación: Flujo usuario
- [ ] Código: 5-10 líneas clave patient_module.py

#### Sección 5: Módulo Admin (Página 11)
- [ ] Screenshot: Login
- [ ] Screenshot: Historial
- [ ] Explicación: Credenciales, roles
- [ ] Código: Autenticación

#### Sección 6: Pruebas y Demo Prolog (Páginas 12-13)
- [ ] Query 1: Obtener síntomas
- [ ] Query 2: Diagnóstico simple
- [ ] Query 3: Diagnóstico múltiple
- [ ] Query 4: Urgencia
- [ ] Query 5: Recomendaciones
- [ ] Query 6: Flujo completo
- [ ] Screenshot: Terminal output demo_consultas_prolog.py

#### Sección 7: GitHub y Control de Versiones (Página 14)
- [ ] Screenshot: Repositorio GitHub
- [ ] Historial commits (6+)
- [ ] Lista de contribuciones
- [ ] Descripción de colaboradores

#### Sección 8: Análisis Técnico (Páginas 15-16)
- [ ] Ventajas de usar Prolog
- [ ] Limitaciones actuales
- [ ] Mejoras futuras
- [ ] Complejidad computacional

#### Conclusiones (Página 17)
- [ ] Resumen logros
- [ ] Objetivos cumplidos
- [ ] Reflexiones personales

#### Apéndice (Páginas 18-20, opcional)
- [ ] Código completo diagnostic_rules.pl
- [ ] Instrucciones instalación
- [ ] Credenciales de prueba

### Verificación PDF
- [ ] Todas las imágenes insertas y legibles
- [ ] Código con formato monoespaciado
- [ ] Tabla de contenidos con links funcionales
- [ ] Numeración de páginas correcta
- [ ] Márgenes estándar (2.54 cm)
- [ ] Fuente legible (Arial/Times 11-12 pt)
- [ ] Sin errores ortográficos (revisar con F7 o herramienta)

### Exportar a PDF
- [ ] Descargar como PDF
- [ ] Nombre: MediLogic_Avance_Proyecto_[NOMBRES].pdf
- [ ] Guardar: h:\Usac\IA1\P1\backend\
- [ ] Verificar tamaño < 50 MB

---

## ✅ FASE FINAL: ENTREGA

### Archivos Preparados
- [ ] MediLogic_Avance_Proyecto_[NOMBRES].pdf (en carpeta backend)
- [ ] Carpeta screenshots/ con 7 imágenes
- [ ] Repositorio GitHub visible públicamente
- [ ] 6+ commits en GitHub con mensajes descriptivos

### Para Profesor
- [ ] Enviar email con:
  - [ ] PDF adjunto
  - [ ] Link a GitHub
  - [ ] Credenciales prueba (si solicita):
    - [ ] Usuario medico / Contraseña 123
    - [ ] Usuario admin / Contraseña 456

### Verificación Final
- [ ] Sistema ejecuta sin errores
- [ ] GUI es responsiva
- [ ] Prolog responde en < 3 segundos
- [ ] Diagnósticos tienen sentido médico
- [ ] Datos se guardan en historia
- [ ] GitHub tiene commits

---

## 📊 TIMELINE RECOMENDADO

| Fase | Duración | Inicio | Fin |
|------|----------|--------|-----|
| GitHub | 1 hora | 10:00 | 11:00 |
| Screenshots | 45 min | 11:00 | 11:45 |
| PDF | 2 horas | 11:45 | 1:45 |
| **TOTAL** | **3:45** | **10:00** | **1:45 PM** |

---

## 🎯 ESTADO ACTUAL

- **Sistema**: ✅ 100% Funcional
- **Base Datos**: ✅ Prolog + JSON
- **Módulos**: ✅ Paciente + Admin
- **GitHub**: ⏳ Pendiente (HOY)
- **Screenshots**: ⏳ Pendiente (HOY)
- **PDF**: ⏳ Pendiente (HOY)

**TIEMPO PARA LISTO: 3 HORAS 45 MINUTOS**

---

## ⚠️ PUNTOS CRÍTICOS

- **DEBE HABER**: GitHub público + 5+ commits
- **DEBE HABER**: Screenshots del sistema en acción
- **DEBE HABER**: PDF de 15-20 páginas con 6 queries documentadas
- **NO OLVIDES**: Agregar auxiliar como colaborador en GitHub
- **NO OLVIDES**: Exportar PDF NO como .docx (debe ser .pdf)

---

**Comenzar AHORA con PASO 1 de GIT_GUIA_RAPIDA.md**
