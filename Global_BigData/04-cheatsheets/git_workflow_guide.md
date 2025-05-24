# 🚀 Guía de Git para el Proyecto Big Data

## 📋 Índice
1. [Configuración Inicial](#1-configuración-inicial)
2. [Fork del Repositorio](#2-fork-del-repositorio)
3. [Clonar el Repositorio](#3-clonar-el-repositorio)
4. [Flujo de Trabajo Diario](#4-flujo-de-trabajo-diario)
5. [Solución de Problemas Comunes](#5-solución-de-problemas-comunes)

## 1. Configuración Inicial

### 1.1 Instalar Git
- **Windows**: Descarga e instala [Git para Windows](https://git-scm.com/download/win)
- **Mac**: Instala con Homebrew: `brew install git`
- **Linux**: `sudo apt-get install git` (Ubuntu/Debian)

### 1.2 Configurar Git
```bash
# Configurar tu nombre
git config --global user.name "Tu Nombre"

# Configurar tu email
git config --global user.email "tu.email@ejemplo.com"

# Verificar la configuración
git config --list
```

## 2. Fork del Repositorio

1. Ve a [https://github.com/Leonsang/Global_BigData](https://github.com/Leonsang/Global_BigData)
2. Haz clic en el botón "Fork" en la esquina superior derecha
3. Selecciona tu cuenta de GitHub como destino del fork
4. ¡Listo! Ahora tienes tu propia copia del repositorio

## 3. Clonar el Repositorio

### 3.1 Clonar tu Fork
```bash
# Reemplaza TU_USUARIO con tu nombre de usuario de GitHub
git clone https://github.com/TU_USUARIO/Global_BigData.git

# Entrar al directorio
cd Global_BigData
```

### 3.2 Configurar el Repositorio Original
```bash
# Agregar el repositorio original como 'upstream'
git remote add upstream https://github.com/Leonsang/Global_BigData.git

# Verificar los remotos configurados
git remote -v
```

## 4. Flujo de Trabajo Diario

### 4.1 Mantener tu Fork Actualizado
```bash
# Obtener cambios del repositorio original
git fetch upstream

# Cambiar a la rama principal
git checkout main

# Combinar cambios del repositorio original
git merge upstream/main

# Subir cambios a tu fork
git push origin main
```

### 4.2 Trabajar en una Nueva Característica
```bash
# Crear y cambiar a una nueva rama
git checkout -b nombre-de-tu-caracteristica

# Hacer cambios en los archivos...

# Agregar cambios
git add .

# Hacer commit
git commit -m "Descripción de tus cambios"

# Subir cambios a tu fork
git push origin nombre-de-tu-caracteristica
```

### 4.3 Crear un Pull Request
1. Ve a tu fork en GitHub
2. Haz clic en "Pull Request"
3. Selecciona la rama con tus cambios
4. Describe tus cambios
5. Envía el Pull Request

## 5. Solución de Problemas Comunes

### 5.1 Deshacer Cambios Locales
```bash
# Descartar cambios en un archivo
git checkout -- nombre-archivo

# Descartar todos los cambios
git reset --hard HEAD
```

### 5.2 Resolver Conflictos
```bash
# Obtener últimos cambios
git pull origin main

# Si hay conflictos, resolverlos manualmente
# Luego:
git add .
git commit -m "Resuelve conflictos"
git push origin main
```

### 5.3 Comandos Útiles
```bash
# Ver estado del repositorio
git status

# Ver historial de commits
git log

# Ver cambios en un archivo
git diff nombre-archivo

# Ver ramas
git branch
```

## 📝 Buenas Prácticas

1. **Commits Atómicos**
   - Haz commits pequeños y específicos
   - Usa mensajes descriptivos
   - Ejemplo: "Agrega función de análisis de datos de transporte"

2. **Nombres de Ramas**
   - Usa nombres descriptivos
   - Ejemplos:
     - `feature/analisis-transporte`
     - `fix/error-calculadora`
     - `docs/actualiza-readme`

3. **Pull Requests**
   - Describe claramente los cambios
   - Incluye capturas de pantalla si es necesario
   - Responde a los comentarios

## 🔧 Recursos Adicionales

- [Documentación Oficial de Git](https://git-scm.com/doc)
- [GitHub Guides](https://guides.github.com/)
- [Git Cheat Sheet](https://education.github.com/git-cheat-sheet-education.pdf)

## 🎯 Ejercicios Prácticos

1. **Ejercicio Básico**
   - Haz fork del repositorio
   - Clónalo localmente
   - Crea una rama nueva
   - Haz un cambio simple
   - Sube los cambios

2. **Ejercicio Intermedio**
   - Actualiza tu fork con los últimos cambios
   - Resuelve un conflicto
   - Crea un pull request

3. **Ejercicio Avanzado**
   - Trabaja en una característica compleja
   - Usa ramas para diferentes aspectos
   - Combina los cambios
   - Crea un pull request detallado

---

## 📞 Soporte

Si tienes problemas:
1. Revisa la documentación
2. Busca en Stack Overflow
3. Pregunta en el canal de Discord del curso
4. Consulta con tus compañeros

---

**¡Recuerda!** Git es una herramienta poderosa que mejora con la práctica. No te desanimes si al principio parece complicado. ¡Sigue practicando! 🚀 