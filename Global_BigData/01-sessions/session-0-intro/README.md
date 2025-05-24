# Sesión 0: Introducción al Entorno Big Data

## 🎯 Objetivos de la Sesión
- Verificar la correcta configuración del entorno de desarrollo
- Comprobar la conectividad con los servicios básicos
- Familiarizarse con las herramientas del ecosistema
- Realizar pruebas básicas de operación

## 🚀 Configuración del Entorno

### Opción 1: Setup Automático (Recomendado)
1. Navega a la carpeta `00-setup`:
   ```bash
   cd ../../00-setup
   ```

2. Ejecuta el script de configuración rápida:
   ```bash
   # En Windows
   .\quick_setup.bat
   
   # En Linux/Mac
   ./quick_setup.sh
   ```

3. Verifica la instalación:
   ```bash
   python test_environment.py
   ```

### Opción 2: Setup Manual
1. **Requisitos del Sistema**:
   - Python 3.8 o superior
   - Java 8 o superior
   - Docker Desktop
   - Mínimo 8GB RAM
   - 20GB espacio en disco

2. **Instalación de Dependencias**:
   ```bash
   pip install -r ../../requirements.txt
   ```

3. **Configuración de Docker**:
   ```bash
   cd ../../00-setup
   docker-compose up -d
   ```

## 📚 Contenido

### 1. Verificación de Docker
- Estado de los contenedores
- Logs de servicios
- Configuración de red
- Gestión de recursos

### 2. Verificación de HDFS
- Estado del NameNode
- Operaciones básicas
  - Creación de directorios
  - Listado de archivos
  - Gestión de permisos
- Reporte del cluster
  - Nodos activos
  - Espacio disponible
  - Estado de replicación

### 3. Verificación de Servicios
- NameNode UI (http://localhost:9870)
- DataNode UI (http://localhost:9864)
- Jupyter Lab (http://localhost:8888)
- Monitoreo de logs

### 4. Ejercicios Prácticos
- Verificación del entorno
  - Estado de Docker
  - Conectividad HDFS
  - Acceso a servicios
- Pruebas básicas
  - Operaciones HDFS
  - Monitoreo de logs
  - Gestión de recursos

## 💡 Casos de Uso
- Desarrollo local de aplicaciones Big Data
- Pruebas de integración
- Aprendizaje práctico
- Prototipado rápido

## 📊 Evaluación
- Verificación exitosa del entorno (40%)
- Completar pruebas básicas (30%)
- Documentación de problemas (30%)

## 🔧 Recursos Adicionales
- [Documentación de Docker](https://docs.docker.com/)
- [Documentación de HDFS](https://hadoop.apache.org/docs/current/hadoop-project-dist/hadoop-hdfs/HdfsDesign.html)
- [Guía de Jupyter](https://jupyter.org/documentation)
- [Troubleshooting Guide](https://hadoop.apache.org/docs/current/hadoop-project-dist/hadoop-common/FileSystemShell.html)

## 🚨 Solución de Problemas
Si encuentras problemas durante la configuración:
1. Revisa el archivo `00-setup/troubleshooting.md`
2. Verifica los logs de Docker:
   ```bash
   docker-compose logs
   ```
3. Asegúrate de que todos los servicios estén corriendo:
   ```bash
   docker-compose ps
   ```

## 📝 Notas Importantes
- Verifica que todos los servicios estén funcionando antes de continuar
- Documenta cualquier error o problema encontrado
- Mantén un registro de los comandos utilizados
- Realiza las pruebas en orden secuencial
- Consulta la documentación oficial si tienes dudas

## 🎓 Valor Profesional
Al completar esta sesión tendrás:
- Entorno de desarrollo Big Data funcional
- Conocimiento de herramientas básicas
- Habilidades de troubleshooting
- Preparación para sesiones avanzadas 