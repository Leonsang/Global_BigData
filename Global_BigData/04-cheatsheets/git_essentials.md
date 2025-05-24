
# Jupyter Notebooks
.ipynb_checkpoints/
*.ipynb_checkpoints

# Data files (¡IMPORTANTE!)
*.csv
*.parquet
*.json
data/
datasets/
raw_data/
processed_data/

# Logs
*.log
logs/

# Docker
.dockerignore

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Spark
metastore_db/
derby.log
spark-warehouse/

# Checkpoints
checkpoints/
/tmp/

# Credentials (¡CRÍTICO!)
.env
config.ini
secrets.yaml
*.key
*.pem

# Large files
*.zip
*.tar.gz
*.gz
models/
*.model

EOF
```

### **Comandos Útiles para Gitignore**
```bash
# Ver qué archivos están siendo ignorados
git status --ignored

# Si ya commitiste algo que debería estar en .gitignore
git rm --cached archivo_grande.csv
git commit -m "Remover archivo grande del repositorio"

# Forzar agregar archivo ignorado (si realmente lo necesitas)
git add -f archivo_especial.csv
```

---

## 🚨 **COMANDOS DE EMERGENCIA**

### **Deshacer Cambios**
```bash
# Deshacer cambios NO commitados en un archivo
git checkout -- archivo.py

# Deshacer TODOS los cambios no commitados
git reset --hard HEAD

# Deshacer último commit (pero mantener cambios)
git reset --soft HEAD~1

# Deshacer último commit (y perder cambios)
git reset --hard HEAD~1

# Deshacer cambios en staging (git add)
git reset HEAD archivo.py
```

### **Stash (Guardar Temporalmente)**
```bash
# Guardar cambios sin commit (para cambiar de branch)
git stash

# Ver stashes guardados
git stash list

# Recuperar último stash
git stash pop

# Recuperar stash específico
git stash apply stash@{0}

# Eliminar stash
git stash drop stash@{0}
```

### **Recuperar Archivos Eliminados**
```bash
# Ver archivos eliminados
git log --diff-filter=D --summary

# Recuperar archivo eliminado
git checkout HEAD~1 -- archivo_eliminado.py
```

---

## 🔍 **BÚSQUEDA Y EXPLORACIÓN**

### **Buscar en Historial**
```bash
# Buscar en commits por mensaje
git log --grep="bug fix"

# Buscar por autor
git log --author="Juan"

# Buscar cambios en archivo específico
git log --follow -- archivo.py

# Ver cambios en rango de fechas
git log --since="2024-01-01" --until="2024-01-31"

# Buscar texto en contenido de archivos
git log -S "función_importante" --source --all
```

### **Comparar Versiones**
```bash
# Comparar con commit anterior
git diff HEAD~1

# Comparar dos commits específicos
git diff abc123 def456

# Comparar branches
git diff main feature/nueva-funcionalidad

# Ver cambios en archivo específico
git diff HEAD~1 HEAD -- archivo.py
```

---

## 📊 **WORKFLOWS PARA DATA SCIENCE**

### **Feature Branch Workflow**
```bash
# 1. Estar al día con main
git checkout main
git pull origin main

# 2. Crear branch para nueva feature
git checkout -b feature/analisis-ventas

# 3. Trabajar en tu feature
# ... hacer cambios en notebooks, scripts, etc.

# 4. Commit frecuentes
git add notebooks/analisis_ventas.ipynb
git commit -m "Agregar análisis inicial de ventas"

git add scripts/procesamiento_datos.py
git commit -m "Implementar limpieza de datos"

# 5. Subir branch
git push -u origin feature/analisis-ventas

# 6. Crear Pull Request en GitHub/GitLab
# (desde la interfaz web)

# 7. Después del merge, limpiar
git checkout main
git pull origin main
git branch -d feature/analisis-ventas
```

### **Hotfix Workflow**
```bash
# Para arreglos urgentes en producción
git checkout main
git pull origin main
git checkout -b hotfix/corregir-bug-critico

# Hacer el fix
git add .
git commit -m "Corregir bug crítico en cálculo de métricas"

git push -u origin hotfix/corregir-bug-critico
# Crear Pull Request urgente
```

---

## 🤝 **COLABORACIÓN EN EQUIPO**

### **Mantener Fork Actualizado**
```bash
# Si trabajas con fork (común en open source)
# 1. Agregar upstream (solo una vez)
git remote add upstream https://github.com/usuario-original/proyecto.git

# 2. Sincronizar con original
git checkout main
git fetch upstream
git merge upstream/main
git push origin main
```

### **Resolver Conflictos de Merge**
```bash
# Cuando git merge dice que hay conflictos:
# 1. Ver archivos con conflictos
git status

# 2. Abrir archivo con conflicto, verás algo como:
<<<<<<< HEAD
tu_codigo_aqui
=======
codigo_de_otro_developer
>>>>>>> branch_name

# 3. Editar manualmente, decidir qué mantener
# 4. Quitar las marcas de conflicto (<<<<, ====, >>>>)
# 5. Agregar y commitear
git add archivo_resuelto.py
git commit -m "Resolver conflicto de merge"
```

### **Rebase (Alternativa a Merge)**
```bash
# Reescribir historial para que sea más limpio
git checkout feature/mi-feature
git rebase main

# Si hay conflictos, resolver y continuar
git add .
git rebase --continue

# O abortar si es muy complicado
git rebase --abort
```

---

## 🔧 **CONFIGURACIÓN AVANZADA**

### **Aliases Útiles**
```bash
# Crear shortcuts para comandos frecuentes
git config --global alias.st status
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.cm commit
git config --global alias.pl pull
git config --global alias.ps push

# Ahora puedes usar:
git st    # en lugar de git status
git co main    # en lugar de git checkout main
```

### **Git Hooks (Automatización)**
```bash
# Pre-commit hook para linting automático
cat << 'EOF' > .git/hooks/pre-commit
#!/bin/bash
# Ejecutar flake8 en archivos Python antes de commit
flake8 *.py
if [ $? -ne 0 ]; then
    echo "❌ Errores de linting encontrados. Commit cancelado."
    exit 1
fi
echo "✅ Linting pasado. Procediendo con commit."
EOF

chmod +x .git/hooks/pre-commit
```

---

## 📈 **CASOS DE USO ESPECÍFICOS BIG DATA**

### **Versionado de Notebooks**
```bash
# Limpiar outputs antes de commit
jupyter nbconvert --clear-output --inplace notebook.ipynb
git add notebook.ipynb
git commit -m "Actualizar análisis en notebook"

# O usar nbstripout para automatizar
pip install nbstripout
nbstripout --install  # Se ejecuta automáticamente en cada commit
```

### **Gestión de Datasets Grandes**
```bash
# Para archivos muy grandes, usar Git LFS
git lfs install
git lfs track "*.csv"
git lfs track "*.parquet"
git lfs track "*.model"

git add .gitattributes
git commit -m "Configurar Git LFS para archivos grandes"

# Ahora los archivos grandes se almacenan eficientemente
git add dataset_grande.csv
git commit -m "Agregar dataset principal"
```

### **Branching para Experimentos**
```bash
# Cada experimento en su propia branch
git checkout -b experiment/random-forest-tuning
# ... hacer experimento ...
git commit -am "Probar Random Forest con nuevos parámetros"

git checkout -b experiment/neural-network-approach
# ... otro experimento ...
git commit -am "Implementar red neuronal para clasificación"

# Mantener solo los experimentos exitosos
git checkout main
git merge experiment/random-forest-tuning  # Si fue exitoso
git branch -d experiment/neural-network-approach  # Si no funcionó
```

---

## 🔍 **DEBUGGING CON GIT**

### **Git Bisect (Encontrar Bug)**
```bash
# Cuando sabes que algo funcionaba antes pero ahora no
git bisect start
git bisect bad HEAD          # Commit actual (con bug)
git bisect good v1.0.0       # Último commit que funcionaba

# Git irá probando commits automáticamente
# Para cada commit que te muestre:
# - Probar si el bug existe
# - git bisect good (si no hay bug)
# - git bisect bad (si hay bug)

# Al final Git te dirá exactamente qué commit introdujo el bug
git bisect reset  # Volver al estado original
```

### **Blame (¿Quién escribió esto?)**
```bash
# Ver quién modificó cada línea de un archivo
git blame archivo.py

# Ver solo líneas específicas
git blame -L 10,20 archivo.py

# Ignorar commits de reformateo
git blame -w archivo.py
```

---

## 🎯 **EJEMPLO COMPLETO: PROYECTO BIG DATA**

```bash
# Setup inicial del proyecto
git clone https://github.com/empresa/analisis-transporte.git
cd analisis-transporte

git checkout -b feature/implementar-kafka-streaming

# Estructura típica de proyecto
mkdir -p {data,notebooks,scripts,tests,config,docs}

# Crear .gitignore apropiado
cat << 'EOF' > .gitignore
# Data
data/raw/
data/processed/
*.csv
*.parquet

# Python
__pycache__/
*.pyc
.ipynb_checkpoints/

# Environments
.env
venv/

# Logs
logs/
*.log

# Spark
spark-warehouse/
metastore_db/
EOF

# Primer commit
git add .gitignore
git commit -m "Setup inicial del proyecto con gitignore"

# Desarrollo iterativo
# 1. Implementar producer de Kafka
git add scripts/kafka_producer.py
git commit -m "Implementar producer de Kafka para datos de transporte"

# 2. Agregar notebook de análisis
git add notebooks/analisis_exploratorio.ipynb
git commit -m "Agregar análisis exploratorio de datos de transporte"

# 3. Implementar pipeline de Spark
git add scripts/spark_processing.py
git commit -m "Implementar pipeline de procesamiento con Spark"

# 4. Agregar tests
git add tests/test_kafka_producer.py
git commit -m "Agregar tests unitarios para Kafka producer"

# 5. Documentación
git add README.md docs/architecture.md
git commit -m "Documentar arquitectura y setup del proyecto"

# Subir feature completa
git push -u origin feature/implementar-kafka-streaming

# Crear Pull Request y merge
# ... después del merge ...

# Limpiar
git checkout main
git pull origin main
git branch -d feature/implementar-kafka-streaming
```

---

## 📋 **CHECKLIST DE COMPETENCIAS GIT**

### **Básico** ✅
- [ ] Configuro Git con mi identidad
- [ ] Hago clone, add, commit, push, pull
- [ ] Uso .gitignore para excluir archivos
- [ ] Veo historial con git log

### **Intermedio** ✅
- [ ] Trabajo con branches y merge
- [ ] Resuelvo conflictos de merge
- [ ] Uso stash para cambios temporales
- [ ] Deshago cambios con reset/checkout

### **Avanzado** ✅
- [ ] Uso rebase para historial limpio
- [ ] Implemento workflows de equipo
- [ ] Configuro hooks y automatización
- [ ] Uso Git LFS para archivos grandes

---

## 🚨 **COMANDOS DE EMERGENCIA RESUMIDOS**

```bash
# "¡Ayuda! ¿Qué hice mal?"
git status                    # Ver estado actual
git log --oneline -10        # Ver últimos commits

# "Quiero deshacer cambios"
git checkout -- archivo.py   # Deshacer cambios en archivo
git reset --hard HEAD        # Deshacer TODO lo no commitado
git reset --soft HEAD~1      # Deshacer último commit

# "Necesito cambiar de branch pero tengo cambios"
git stash                    # Guardar cambios temporalmente
git checkout otra-branch     # Cambiar
git stash pop               # Recuperar cambios

# "Rompí algo, quiero volver a como estaba"
git reflog                   # Ver historial completo
git reset --hard abc123      # Volver a commit específico

# "Ayuda, conflictos de merge!"
git status                   # Ver archivos con conflictos
# Editar archivos, resolver conflictos
git add .                    # Marcar como resueltos
git commit                   # Completar merge
```

**💡 Tip Final: Git parece complejo, pero el 90% del tiempo solo usas: add, commit, push, pull. ¡Lo demás es para casos especiales!**
