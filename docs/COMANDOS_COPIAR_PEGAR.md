# COMANDOS LISTOS PARA COPIAR Y PEGAR
## Para PowerShell/CMD - Windows

---

## 📋 ANTES DE EMPEZAR
Asegúrate de:
- [ ] Tener Git instalado: https://git-scm.com/download/win
- [ ] Tener PowerShell abierto
- [ ] Tener cuenta GitHub creada: https://github.com/signup

---

## 🚀 OPCIÓN 1: RÁPIDO (Todo automático)

### Paso 1: Configurar Git (PRIMERA VEZ SOLO)
Copia y pega esto en PowerShell:

```powershell
git config --global user.name "Tu Nombre"
git config --global user.email "tu@email.com"
```

Reemplaza "Tu Nombre" y "tu@email.com" con tus datos.

---

### Paso 2: Entrar a la Carpeta
```powershell
cd h:\Usac\IA1\P1\backend
```

Verificar que entraste correctamente:
```powershell
ls
```

Debes ver archivo Main.py, diagnostic_rules.pl, etc.

---

### Paso 3: Inicializar Git
```powershell
git init
git add .
git commit -m "Initial commit: MediLogic project structure"
```

---

### Paso 4: Conectar con GitHub
REEMPLAZA [USUARIO] con tu usuario de GitHub:

```powershell
git remote add origin https://github.com/[USUARIO]/MediLogic.git
git branch -M main
git push -u origin main
```

---

### Paso 5: Hacer 5 Commits Adicionales

**Commit 2:**
```powershell
git add diagnostic_rules.pl
git commit -m "feat: Add Prolog knowledge base with 10 symptoms and 30+ conditions"
```

**Commit 3:**
```powershell
git add prolog_engine.py
git commit -m "feat: Implement Python-Prolog integration engine with pyswip"
```

**Commit 4:**
```powershell
git add database.py
git commit -m "feat: Integrate Prolog queries in database module"
```

**Commit 5:**
```powershell
git add patient_module.py
git commit -m "feat: Update patient module to use dynamic Prolog engine"
```

**Commit 6:**
```powershell
git add *.md
git commit -m "docs: Add complete technical documentation and guides"
```

---

### Paso 6: Subir Todo a GitHub
```powershell
git push origin main
```

Si te pregunta por contraseña:
- **Opción A**: Se abre navegador → Click Authorize
- **Opción B**: Pega tu token personal de GitHub

---

### Paso 7: Verificar
1. Abre navegador
2. Ve a: https://github.com/[TU_USUARIO]/MediLogic
3. Deberías ver todos archivos + 6 commits

---

## 🎯 OPCIÓN 2: PASO A PASO (Con verificación)

Si es la primera vez o preferes ir lento:

### 1. Verificar que Git está instalado
```powershell
git --version
```
Debe mostrar: `git version 2.x.x`

---

### 2. Configurar usuario (PRIMERA VEZ)
```powershell
git config --global user.name "Tu Nombre Aquí"
```

```powershell
git config --global user.email "tu@email.com"
```

Verificar:
```powershell
git config --global user.name
```

Debe mostrar el nombre que escribiste.

---

### 3. Navegar a carpeta del proyecto
```powershell
cd h:\Usac\IA1\P1\backend
```

---

### 4. Verificar que estamos en el lugar correcto
```powershell
pwd
```

Debe mostrar: `h:\Usac\IA1\P1\backend`

---

### 5. Ver archivos
```powershell
ls
```

Debes ver:
```
Main.py
patient_module.py
admin_module.py
database.py
diagnostic_rules.pl
prolog_engine.py
...
```

---

### 6. Inicializar Git
```powershell
git init
```

Se crea carpeta `.git` (oculta)

---

### 7. Ver estado
```powershell
git status
```

Dice: "Untracked files:" + lista archivos

---

### 8. Agregar archivos
```powershell
git add .
```

---

### 9. Ver status nuevamente
```powershell
git status
```

Ahora dice: "Changes to be committed:" (en verde)

---

### 10. Primer Commit
```powershell
git commit -m "Initial commit: MediLogic project structure"
```

Respuesta:
```
[main (root-commit) xxxx] Initial commit...
 18 files changed, 2000 insertions
```

---

### 11. Ver historial
```powershell
git log --oneline
```

Debes ver 1 línea con tu commit

---

### 12. Crear repositorio en GitHub CON ANTICIPACIÓN

Abre navegador y ve a: https://github.com/new

Llena:
- **Repository name**: MediLogic
- **Description**: Sistema de Diagnóstico Médico con Prolog
- **Public**: ✓ Marcado
- NO inicializar con README
- Click: Create repository

Copia la URL HTTPS que te da (algo como):
```
https://github.com/[TU_USUARIO]/MediLogic.git
```

---

### 13. Conectar con GitHub
Pega esto (pero reemplaza la URL con la tuya):

```powershell
git remote add origin https://github.com/[TU_USUARIO]/MediLogic.git
```

---

### 14. Cambiar rama a "main"
```powershell
git branch -M main
```

---

### 15. Subir a GitHub (requiere autenticación)
```powershell
git push -u origin main
```

- Si aparece ventana de navegador → Click "Authorize"
- Si pide contraseña → Es tu token de GitHub

---

### 16. Verificar en GitHub
1. Navegador: https://github.com/[TU_USUARIO]/MediLogic
2. Debes ver todos archivos ahora

---

### 17-22. Hacer commits adicionales

Repite esto 5 veces con cada mensaje diferente:

```powershell
git add [ARCHIVO]
git commit -m "[MENSAJE]"
git push origin main
```

**Para Commit 2:**
```powershell
git add diagnostic_rules.pl
git commit -m "feat: Add Prolog knowledge base with 10 symptoms and 30+ conditions"
git push origin main
```

**Para Commit 3:**
```powershell
git add prolog_engine.py
git commit -m "feat: Implement Python-Prolog integration engine with pyswip"
git push origin main
```

**Para Commit 4:**
```powershell
git add database.py
git commit -m "feat: Integrate Prolog queries in database module"
git push origin main
```

**Para Commit 5:**
```powershell
git add patient_module.py
git commit -m "feat: Update patient module to use dynamic Prolog engine"
git push origin main
```

**Para Commit 6:**
```powershell
git add *.md
git commit -m "docs: Add complete technical documentation and guides"
git push origin main
```

---

### 23. Verificar historial final
```powershell
git log --oneline
```

Debes ver 6 líneas (6 commits)

---

## 🆘 ERRORES COMUNES Y SOLUCIONES

### Error: `fatal: not a git repository`
**Solución:** No estás en la carpeta correcta
```powershell
cd h:\Usac\IA1\P1\backend
```

---

### Error: `fatal: not a directory`
**Solución:** La ruta tiene espacios o está mal
```powershell
# Intenta con comillas
cd "h:\Usac\IA1\P1\backend"
```

---

### Error: `error: src refspec main does not match`
**Solución:** No hiciste commit aún
```powershell
git commit -m "Initial commit"
```

---

### Error: `fatal: Could not read Username`
**Solución:** No tienes Git o credenciales configuradas
```powershell
# Opción A: Configura usuario
git config --global user.name "Tu Nombre"

# Opción B: Usa GitHub Desktop en lugar de CLI
# Descargar: https://desktop.github.com/
```

---

### Error: `remote origin already exists`
**Solución:** Ya agregaste remote, intenta:
```powershell
git remote remove origin
git remote add origin https://github.com/[USUARIO]/MediLogic.git
```

---

### Error: Cambios que no aparecen en GitHub
**Solución:** Olvidaste hacer push
```powershell
git push origin main
```

---

## 🔗 HERRAMIENTAS ALTERNATIVAS

Si PowerShell es complicado:

### Opción 1: GitHub Desktop (Más Fácil)
1. Descargar: https://desktop.github.com/
2. Instalar
3. Iniciar sesión con GitHub
4. File → Clone Repository (tu MediLogic)
5. Cambiar ruta a: h:\Usac\IA1\P1\backend
6. Clone
7. Changes aparecen automático
8. Escribir mensaje → Commit to main
9. Push origin

### Opción 2: Git Bash (Si prefieres terminal Unix)
1. Instala Git (incluye Git Bash)
2. Click derecho en carpeta → Git Bash Here
3. Mismos comandos que arriba

### Opción 3: Visual Studio Code integrado
1. Abre VS Code
2. File → Open Folder → Selecciona backend
3. Source Control (Ctrl+Shift+G)
4. Initialize Repository
5. Stage All Changes
6. Escribe mensaje
7. Commit
8. Publish to GitHub

---

## ✅ CHECKLIST FINAL

- [ ] Git instalado (`git --version` funciona)
- [ ] Usuario configurado (`git config --global user.name` muestra tu nombre)
- [ ] Repositorio GitHub creado (público)
- [ ] `git init` ejecutado en h:\Usac\IA1\P1\backend
- [ ] 1 commit inicial ("Initial commit...")
- [ ] Conectado con `git remote add origin`
- [ ] Primer push exitoso (`git push -u origin main`)
- [ ] 5 commits adicionales realizados
- [ ] Todos los commits visibles en GitHub
- [ ] Historlal visible en GitHub (`git log --oneline` muestra 6+)

---

## 📸 PRÓXIMO PASO: SCREENSHOTS

Una vez que GitHub esté listo, ve a: **CHECKLIST_EJECUCION.md → FASE 2**

Comandos para ejecutar sistema (para screenshot):
```powershell
python Main.py
```

Terminal demo:
```powershell
python demo_consultas_prolog.py
```

---

**¿Preguntas? Ve a GIT_GUIA_RAPIDA.md para explicación detallada**
