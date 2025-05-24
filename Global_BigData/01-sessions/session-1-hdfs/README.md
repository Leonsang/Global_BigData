# Sesión 1: Hadoop Distributed File System (HDFS)

## 🎯 Objetivos de la Sesión
- Comprender la arquitectura y funcionamiento de HDFS
- Aprender a interactuar con HDFS mediante comandos básicos
- Realizar operaciones de lectura y escritura en HDFS
- Analizar el rendimiento y características de HDFS

## 🎬 Hook Inicial: El Problema de Google
> "En 2003, Google tenía un problema: El internet crecía más rápido que su capacidad de almacenarlo. Una supercomputadora de $50 millones no era la solución... necesitaban algo diferente."

### La Solución de Google
- Conectó 1000 computadoras baratas ($500 c/u)
- Total: $500,000 vs $50,000,000
- Resultado: 100x más capacidad, 100x menos costo
- Nació Google File System (GFS)
- HDFS es la versión open source de GFS

## 📚 Contenido

### 1. Fundamentos de HDFS
- Arquitectura de HDFS
  - NameNode (Master)
    - Metadatos del sistema
    - Ubicación de archivos
    - Coordinación general
  - DataNode (Slave)
    - Almacenamiento de bloques
    - Reporte de estado
    - Replicación de datos
- Características y limitaciones
  - Escalabilidad horizontal
  - Tolerancia a fallos
  - Consistencia eventual
  - Limitaciones de latencia
- Modelo de replicación de datos
  - Factor de replicación (default: 3)
  - Estrategias de colocación
  - Balanceo de datos

### 2. Operaciones Básicas con HDFS
- Comandos fundamentales de HDFS
  ```bash
  hdfs dfs -ls /          # Listar directorios
  hdfs dfs -put file /    # Subir archivo
  hdfs dfs -get /file     # Descargar archivo
  hdfs dfs -rm /file      # Eliminar archivo
  ```
- Gestión de archivos y directorios
  - Creación y eliminación
  - Permisos y propietarios
  - Cuotas y límites
- Monitoreo del sistema
  - Estado del clúster
  - Uso de espacio
  - Nodos activos

### 3. Análisis de Clúster HDFS
- Estructura del clúster
  ```
  ┌─────────────────────────────────────────┐
  │              HDFS CLUSTER                │
  ├─────────────────────────────────────────┤
  │  NameNode (Master)                      │
  │  - Metadatos del sistema                │
  │  - Ubicación de archivos                │
  │  - Coordinación general                 │
  ├─────────────────────────────────────────┤
  │  DataNode 1     DataNode 2              │
  │  - Almacena     - Almacena              │
  │    bloques        bloques               │
  │  - Reporta      - Reporta               │
  │    estado         estado                │
  ├─────────────────────────────────────────┤
  │  Replicación Factor: 2                  │
  │  Block Size: 128MB                      │
  │  Total Capacity: Escalable              │
  └─────────────────────────────────────────┘
  ```
- Configuración de nodos
  - Parámetros de rendimiento
  - Límites de recursos
  - Políticas de replicación
- Monitoreo de recursos
  - Uso de CPU y memoria
  - I/O de disco y red
  - Latencia de operaciones

### 4. Ejercicios Prácticos
- Creación y gestión de archivos en HDFS
  - Subir datasets de ejemplo
  - Organizar estructura de directorios
  - Gestionar permisos
- Análisis de rendimiento
  - Medir throughput
  - Analizar latencia
  - Optimizar configuración
- Resolución de problemas comunes
  - Recuperación de nodos caídos
  - Balanceo de datos
  - Corrupción de bloques

## 💡 Casos de Uso Real
- Almacenamiento de logs
- Análisis de datos masivos
- Backup distribuido
- Procesamiento de datos en batch

## 📊 Evaluación
- Completar ejercicios prácticos (40%)
- Demostrar comprensión de comandos HDFS (30%)
- Analizar y resolver problemas de clúster (30%)

## 🔧 Recursos Adicionales
- [Documentación oficial de HDFS](https://hadoop.apache.org/docs/current/hadoop-project-dist/hadoop-hdfs/HdfsDesign.html)
- [Guía de comandos HDFS](https://hadoop.apache.org/docs/current/hadoop-project-dist/hadoop-common/FileSystemShell.html)
- [Mejores prácticas de HDFS](https://hadoop.apache.org/docs/current/hadoop-project-dist/hadoop-hdfs/HdfsDesign.html#Best_Practices)
- [Tutorial de administración de HDFS](https://hadoop.apache.org/docs/current/hadoop-project-dist/hadoop-hdfs/HdfsUserGuide.html)

## 📝 Notas Importantes
- Asegúrate de tener acceso al clúster HDFS
- Mantén un registro de los comandos utilizados
- Documenta cualquier problema encontrado
- Practica las operaciones básicas hasta dominarlas
- Realiza backups antes de operaciones críticas

## 🎓 Valor Profesional
Al completar esta sesión tendrás:
- Experiencia práctica con HDFS en producción
- Habilidades de troubleshooting distribuido
- Conocimientos de optimización de storage
- Comprensión de trade-offs arquitectónicos

## 💰 Oportunidades Laborales
Estas habilidades son valoradas en:
- Ingeniero de Datos Senior: $80k-120k
- DevOps Engineer: $70k-110k
- Solutions Architect: $90k-140k
- Big Data Consultant: $100k-150k