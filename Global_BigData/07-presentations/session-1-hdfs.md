# 🗂️ Sesión 1: HDFS y MapReduce

## 📚 Objetivos de la Sesión
- Comprender la arquitectura y funcionamiento de HDFS
- Entender los principios fundamentales de MapReduce
- Analizar los casos de uso típicos de HDFS
- Conocer las mejores prácticas de diseño

## 🎯 Contenido

### 1. Apertura con Analogía
- "Imagina una biblioteca gigante donde cada libro está dividido en partes y guardado en diferentes estantes"
- "¿Cómo encontrarías un libro específico si no supieras dónde están sus partes?"
- "HDFS es como un bibliotecario maestro que sabe exactamente dónde está cada parte"

### 2. Introducción a HDFS
- La historia del problema:
  * "En 2003, Google enfrentaba un desafío: almacenar y procesar petabytes de datos"
  * "Las soluciones tradicionales no escalaban"
  * "Necesitaban un nuevo paradigma"
- La solución:
  * "Divide y vencerás: el principio fundamental"
  * "Si un servidor no puede manejar los datos, usa muchos servidores"
  * "Si un disco no es suficiente, usa muchos discos"

### 3. Arquitectura de HDFS
- El NameNode como el cerebro:
  * "El NameNode es como el director de una orquesta"
  * "Sabe dónde está cada pieza de información"
  * "Coordina a todos los músicos (DataNodes)"
- Los DataNodes como los trabajadores:
  * "Cada DataNode es como un estante en nuestra biblioteca"
  * "Almacena partes de los libros (bloques)"
  * "Mantiene copias de seguridad"
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

### 4. Comandos de HDFS
- La interfaz de usuario:
  * "Como un control remoto para nuestra biblioteca"
  * "Comandos simples para tareas complejas"
  * "De la teoría a la práctica"
- Operaciones básicas:
  * Listado de directorios
  * Carga y descarga de archivos
  * Eliminación de recursos
- Gestión de archivos:
  * Creación y eliminación
  * Permisos y propietarios
  * Cuotas y límites

### 5. Programación Distribuida y MapReduce
- La historia de MapReduce:
  * "De procesar un libro a procesar una biblioteca"
  * "El poder de dividir y conquistar"
  * "De Google a Hadoop"
- Patrones de diseño:
  * "WordCount: El 'Hola Mundo' de Big Data"
  * "Inverted Index: La base de los motores de búsqueda"
  * "PageRank: El algoritmo que hizo a Google"

### 6. Conceptos Clave
- **Componentes HDFS**
  * NameNode: Metadatos y coordinación
  * DataNode: Almacenamiento y replicación
  * Secondary NameNode: Checkpointing
  * JournalNode: High Availability

- **Conceptos de Almacenamiento**
  * Bloques (default 128MB)
  * Replicación (default 3x)
  * Rack Awareness
  * Quotas y permisos

- **Patrones MapReduce**
  * Map: Transformación paralela
  * Reduce: Agregación de resultados
  * Combiner: Optimización local
  * Partitioner: Distribución de datos

- **Optimizaciones**
  * Compresión de datos
  * Esquemas de archivos
  * Estrategias de particionamiento
  * Tuning de rendimiento

## 📊 Entregables
- Comprensión de arquitectura HDFS
- Análisis de casos de uso
- Diseño de soluciones MapReduce

## 🔍 Recursos Adicionales
- [Documentación oficial de HDFS](https://hadoop.apache.org/docs/current/hadoop-project-dist/hadoop-hdfs/HdfsDesign.html)
- [Tutorial de MapReduce](https://hadoop.apache.org/docs/current/hadoop-mapreduce-client/hadoop-mapreduce-client-core/MapReduceTutorial.html)
- [Patrones de Diseño MapReduce](https://www.oreilly.com/library/view/mapreduce-design-patterns/9781449327297/)
- [Mejores Prácticas HDFS](https://hadoop.apache.org/docs/current/hadoop-project-dist/hadoop-hdfs/HdfsDesign.html#Best_Practices)

## 🎯 Próxima Sesión
- Spark: Procesamiento en Memoria
- RDDs y DataFrames
- Transformaciones y Acciones
- Optimización de Jobs 