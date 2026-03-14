# GitHub + Git - Guía Rápida para MediLogic
## Pasos exactos para crear repositorio y commits

---

## PASO 1: Crear Cuenta GitHub (si no tienes)
1. Ir a: https://github.com/signup
2. Email: tu_email@gmail.com
3. Contraseña: Segura
4. Click "Create account"

---

## PASO 2: Crear Repositorio
1. Ir a: https://github.com/new
2. Repository name: **MediLogic**
3. Description: "Sistema de Diagnóstico Médico con Prolog"
4. Seleccionar: **Public**
5. IMPORTANTE: NO inicializar con README
6. Click: "Create repository"

Verás instrucciones como:
```
…or push an existing repository from the command line
```

---

## PASO 3: Preparar Git en Tu Computadora

Abre PowerShell (cmd) como Administrador:

### Instalar Git (si no tienes)
- Windows: https://git-scm.com/download/win
- Descargar e instalar
- Siguiente, siguiente, siguiente

### Verificar que Git esté instalado
```powershell
git --version
```

Debe mostrar: `git version 2.x.x...`

---

## PASO 4: Configurar Git (Primera vez)
```powershell
git config --global user.name "Tu Nombre"
git config --global user.email "tu@email.com"
```

Verificar:
```powershell
git config --global user.name
git config --global user.email
```

---

## PASO 5: Navegar a la Carpeta del Proyecto

```powershell
cd h:\Usac\IA1\P1\backend
```

Verificar que estés en el lugar correcto:
```powershell
ls
```

Debes ver la mayoría de archivos:
```
Main.py
patient_module.py
diagnostic_rules.pl
prolog_engine.py
...
```

---

## PASO 6: Inicializar Git en La Carpeta

```powershell
git init
```

Respuesta:
```
Initialized empty Git repository in h:\Usac\IA1\P1\backend\.git
```

---

## PASO 7: Agregar Archivos de Git

```powershell
git add .
```

Verificar qué se agregó:
```powershell
git status
```

Debes ver muchos archivos en verde (Changes to be committed)

---

## PASO 8: Hacer el Primer Commit

```powershell
git commit -m "Initial commit: MediLogic project structure"
```

Respuesta (algo como):
```
[main (root-commit) a1b2c3d] Initial commit: MediLogic project structure
 18 files changed, 2000 insertions(+)
```

---

## PASO 9: Conectar con GitHub

Copia la URL de tu repositorio:
- Ir a: https://github.com/[TU_USUARIO]/MediLogic
- Click botón verde "<> Code"
- Copiar la URL HTTPS

```powershell
git remote add origin https://github.com/[TU_USUARIO]/MediLogic.git
```

Verificar:
```powershell
git remote -v
```

---

## PASO 10: Cambiar a Rama "main"

```powershell
git branch -M main
```

---

## PASO 11: Subir a GitHub (Push)

```powershell
git push -u origin main
```

Se te pedirá autenticación (elige una):

**Opción A: Autenticación por navegador (Recomendado)**
- Se abrirá una ventana
- Click "Authorize git-for-windows"
- Confirmado

**Opción B: Token Personal**
1. GitHub → Settings → Developer settings → Personal access tokens → Generate new token
2. Seleccionar: repo, admin:repo_hook
3. Copiar token y pegarlo cuando pida contraseña

---

## PASO 12: Verificar que Subió

1. Ir a: https://github.com/[TU_USUARIO]/MediLogic
2. Deberías ver todos tus archivos

---

## HACER 5 COMMITS POSTERIORES

Para cumplir requisito de "5 commits", haz lo siguiente:

### Commit 2: Base de Conocimiento
```powershell
git add diagnostic_rules.pl
git commit -m "feat: Add Prolog knowledge base with 10 symptoms and 30+ conditions"
```

### Commit 3: Motor Prolog
```powershell
git add prolog_engine.py
git commit -m "feat: Implement Python-Prolog integration engine"
```

### Commit 4: Base de Datos
```powershell
git add database.py
git commit -m "feat: Integrate Prolog queries in database module"
```

### Commit 5: Módulo Pacientes
```powershell
git add patient_module.py
git commit -m "feat: Update patient module to use Prolog engine"
```

### Commit 6: Documentación
```powershell
git add *.md
git commit -m "docs: Add complete technical documentation"
```

---

## SUBIR TODOS LOS COMMITS

```powershell
git push origin main
```

---

## AGREGAR AUXILIAR COMO COLABORADOR

1. Ir a: https://github.com/[TU_USUARIO]/MediLogic
2. Settings → Collaborators
3. Agregar email del auxiliar
4. Enviar invitación

---

## VERIFICAR HISTORIAL

Para ver tus commits en terminall:
```powershell
git log --oneline
```

Verá algo como:
```
abc1234 docs: Add complete technical documentation
def5678 feat: Update patient module to use Prolog engine
...
```

---

## PROBLEMAS COMUNES

### Problema: "fatal: not a git repository"
**Solución:** No estás en la carpeta correcta
```powershell
cd h:\Usac\IA1\P1\backend
```

### Problema: "error: src refspec main does not match any"
**Solución:** Debes hacer al menos un commit primero
```powershell
git commit -m "Initial commit"
```

### Problema: "fatal: could not read Username"
**Solución:** 
- Asegúrate de tener Git configurado
- O usa GitHub Desktop en lugar de línea de comandos

### Problema: Cambios que no se ven en GitHub
**Solución:** Asegúrate de hacer `git push origin main`

---

## USAR GIT DESKTOP (MÁS FÁCIL)

Si prefieres interfaz gráfica:

1. Descargar: https://desktop.github.com/
2. Instalar
3. Iniciar sesión con tu usuario de GitHub
4. File → Clone Repository
5. Seleccionar tu repositorio
6. Cambiar ruta a: h:\Usac\IA1\P1\backend
7. Clone

Luego:
- Cambios se cargan automáticamente
- Click "Commit to main"
- Escribir mensaje
- Click "Push origin"

---

## RESUMEN RÁPIDO

```bash
# 1. Entrar a carpeta
cd h:\Usac\IA1\P1\backend

# 2. Inicializar
git init

# 3. Configurar usuario
git config --global user.name "Tu Nombre"
git config --global user.email "tu@email.com"

# 4. Agregar archivos
git add .

# 5. Primer commit
git commit -m "Initial commit"

# 6. Conectar a GitHub
git remote add origin https://github.com/[USUARIO]/MediLogic.git

# 7. Cambiar rama
git branch -M main

# 8. Subir
git push -u origin main

# 9. Siguientes commits (repite)
git add archivo.py
git commit -m "descripción"
git push origin main
```

---

## CAPTURA DE PANTALLA DEL REPOSITORIO

Una vez que subas todo, toma una captura:
1. Abre tu repositorio: https://github.com/[TU_USUARIO]/MediLogic
2. Presiona: Print Screen o Snipping Tool
3. Guarda como: github_repository.png
4. Incluye en PDF

---

**¿Dudas? Ve a RESPUESTA_FINAL.txt para el contexto completo**
