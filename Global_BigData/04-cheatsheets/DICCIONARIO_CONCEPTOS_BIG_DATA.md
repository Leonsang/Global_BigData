# 📚 DICCIONARIO DE CONCEPTOS BIG DATA
## Guía Completa de Términos para el Módulo Completo

---

## 🎯 **CÓMO USAR ESTE DICCIONARIO**

**Para Estudiantes:**
- 📖 Consulta ANTES de cada sesión para prepararte
- 🔍 Busca términos durante exercises prácticos
- ✅ Valida tu entendimiento después de cada sesión

**Para Instructores:**
- 🎓 Reference rápida durante explicaciones
- 📋 Checklist de conceptos que estudiantes deben dominar
- 🔧 Troubleshooting cuando estudiantes se confunden

**Nivel de Dificultad:**
- 🟢 **Básico**: Fundamental para entender
- 🟡 **Intermedio**: Importante para practice
- 🔴 **Avanzado**: Para optimization y troubleshooting

---

## 🎪 **SESIÓN 0: FOUNDATION - CONCEPTOS BASE**

### **🟢 SISTEMAS DISTRIBUIDOS**
**Definición**: Múltiples computadoras trabajando juntas como si fueran una sola
**Analogía**: Como una orquesta - muchos músicos, un director, una sinfonía
**Ejemplo Real**: Google Search usa miles de servidores para responderte en 0.3 segundos
**Por qué Importa**: Base de todo Big Data moderno
**Relacionado con**: Cluster, Load Balancing, Fault Tolerance

### **🟢 DOCKER**
**Definición**: Tecnología que empaca aplicaciones con todo lo que necesitan
**Analogía**: Como contenedores de barco - todo empacado, funciona en cualquier puerto
**Ejemplo Real**: Netflix despliega miles de containers por día
**Por qué Importa**: Hace que setup sea automático y reproducible
**Comandos Clave**: `docker ps`, `docker-compose up -d`

### **🟢 CLUSTER**
**Definición**: Grupo de computadoras coordinadas que trabajan juntas
**Componentes**: Master (coordinador) + Workers (ejecutores)
**Ejemplo Real**: Cluster de Spark con 1 Master + múltiples Workers
**Por qué Importa**: Permite escalabilidad horizontal
**Relacionado con**: HDFS Cluster, Spark Cluster, Kafka Cluster

### **🟡 ESCALABILIDAD HORIZONTAL vs VERTICAL**
**Vertical (Scale Up)**: Hacer UNA computadora más poderosa
- Pros: Simple, no coordinación
- Cons: Límites físicos, muy caro
**Horizontal (Scale Out)**: Agregar MÁS computadoras
- Pros: Sin límites, más barato
- Cons: Complejidad de coordinación
**Big Data Choice**: Siempre horizontal

### **🟡 CAP THEOREM**
**Definición**: En sistemas distribuidos solo puedes tener 2 de 3:
- **C**onsistency: Todos ven los mismos datos
- **A**vailability: Sistema siempre disponible  
- **P**artition Tolerance: Funciona aunque fallen conexiones
**Ejemplos Reales**:
- Google Search: A + P (disponible, datos pueden variar)
- Bancos: C + P (datos exactos, puede no estar disponible)
**Por qué Importa**: Entender trade-offs de diseño

### **🟡 DATA LOCALITY**
**Definición**: Mover código hacia datos, no datos hacia código
**Regla de Oro**: Código (KB) viaja fácil, Datos (GB) viajan caro
**Ejemplo**: En lugar de traer 10GB a 1 servidor, enviar 10KB de código a 10 servidores
**Impacto**: Reduce network I/O en 1000x
**Aplicación**: Fundamento de MapReduce, Spark, HDFS

### **🟡 IDEMPOTENCY**
**Definición**: Ejecutar operación múltiples veces = mismo resultado que una vez
**Ejemplo Bueno**: `SET balance = 1000` (seguro repetir)
**Ejemplo Malo**: `ADD 100 to balance` (peligroso repetir)
**Por qué Importa**: Permite retry seguro cuando fallan operaciones
**Aplicación**: Kafka consumers, Spark tasks, API calls

### **🟢 FAULT TOLERANCE**
**Definición**: Sistema sigue funcionando aunque componentes fallen
**Filosofía**: Diseñar ASUMIENDO que cosas van a fallar
**Estrategias**: Replicación, Redundancia, Auto-recovery
**Ejemplo Real**: Netflix pierde 100 servidores/día, usuarios no se dan cuenta
**Relacionado con**: Replication, High Availability, Disaster Recovery

---

## 🗂️ **SESIÓN 1: HDFS - STORAGE DISTRIBUIDO**

### **🟢 HDFS (Hadoop Distributed File System)**
**Definición**: Sistema de archivos que distribuye datos entre múltiples servidores
**Inspiración**: Google File System (GFS)
**Característica Clave**: Write-once, read-many
**Use Cases**: Data Lakes, ETL storage, Analytics datasets
**No es bueno para**: Random access, low latency, small files

### **🟢 NAMENODE**
**Definición**: Master node que guarda metadatos del filesystem
**Función**: "Bibliotecario" que sabe dónde está cada archivo
**Almacena**: Ubicaciones de blocks, permisos, timestamps
**NO almacena**: Los datos reales (esos están en DataNodes)
**Punto Crítico**: Si falla = cluster no funciona (necesita HA)

### **🟢 DATANODE**
**Definición**: Worker nodes que almacenan los datos reales
**Función**: "Estantes" que guardan los blocks de archivos
**Responsabilidades**: Reportar estado, servir reads/writes, replicar data
**Heartbeat**: Reporta a NameNode cada 3 segundos
**Auto-recovery**: Si falla, NameNode usa réplicas automáticamente

### **🟡 BLOCKS**
**Definición**: Pedazos de 128MB en que HDFS divide archivos grandes
**Por qué 128MB**: Balance entre overhead y distribución
**Distribución**: Cada block se replica en múltiples DataNodes
**Ejemplo**: Archivo 1GB = 8 blocks de 128MB cada uno
**Benefit**: Paralelismo (multiple DataNodes leen simultáneamente)

### **🟡 REPLICATION**
**Definición**: Cada block se copia automáticamente en múltiples DataNodes
**Default**: Factor 3 (cada block en 3 lugares diferentes)
**Rack Awareness**: Primera copia local, segunda en diferente rack
**Trade-off**: Más réplicas = más seguridad + más espacio usado
**Auto-management**: Si nodo falla, HDFS crea nuevas réplicas automáticamente

### **🟡 METADATA**
**Definición**: Información SOBRE los datos (no los datos mismos)
**Incluye**: Ubicación de blocks, tamaños, permisos, checksums
**Storage**: Todo en memoria del NameNode para velocidad
**Backup**: FSImage (snapshot) + EditLog (cambios incrementales)
**Insight Crítico**: Metadata más importante que datos (sin metadata = datos inaccesibles)

### **🔴 FSIMAGE & EDITLOG**
**FSImage**: Snapshot completo de metadatos en disco
**EditLog**: Log de cambios desde último FSImage
**Checkpoint**: Secondary NameNode combina FSImage + EditLog periódicamente
**Recovery**: En caso de fallo, reconstruye metadata desde FSImage + EditLog
**HA Setup**: Usa Journal Nodes para compartir EditLog entre NameNodes

### **🟡 RACK AWARENESS**
**Definición**: HDFS conoce topología física del datacenter
**Estrategia de Replicación**: 
- Copia 1: Mismo rack (rápido)
- Copia 2: Diferente rack (seguro)
- Copia 3: Mismo rack que copia 2 (balance)
**Benefit**: Optimiza velocidad + tolerancia a fallos de rack completo

---

## ⚡ **SESIÓN 2: PROCESSING DISTRIBUIDO**

### **🟢 MAPREDUCE**
**Definición**: Paradigma de programación para procesar datos masivos en paralelo
**Fases**: Map → Shuffle → Reduce
**Inspiración**: Functional programming (map/reduce functions)
**Fortaleza**: Muy robusto, fault tolerant, simple conceptualmente
**Debilidad**: Lento para workflows complejos (escribe a disco entre steps)

### **🟢 MAP FUNCTION**
**Definición**: Transforma/filtra datos en paralelo
**Input**: Key-value pairs
**Output**: Nuevos key-value pairs
**Ejemplo**: Extraer (route_id, passenger_count) de cada línea de log
**Paralelismo**: Un mapper por input split (típicamente 1 por block)

### **🟢 REDUCE FUNCTION**
**Definición**: Agrega/combina datos con misma key
**Input**: Key + lista de todos los values para esa key
**Output**: Key + valor agregado
**Ejemplo**: Sumar passenger_count por route_id
**Constraint**: Solo ve datos de UNA key a la vez

### **🟡 SHUFFLE**
**Definición**: Fase donde datos se reorganizan por key entre Map y Reduce
**Proceso**: Agrupa todos values con misma key, los envía al mismo reducer
**Network Intensive**: Única fase que transfiere datos por red
**Optimization**: Combiners pueden reducir datos antes de shuffle

### **🟡 COMBINER**
**Definición**: "Mini-reducer" que pre-agrega datos localmente antes de shuffle
**Benefit**: Reduce tráfico de red dramáticamente (80-95% típico)
**Requirement**: Función debe ser asociativa y conmutativa
**Ejemplo Válido**: Sum, Count, Max, Min
**Ejemplo Inválido**: Average (necesita numerador + denominador separados)

### **🟡 PARTITIONER**
**Definición**: Decide qué reducer recibe cada key
**Default**: Hash partitioner (hash(key) % num_reducers)
**Custom**: Puedes crear lógica custom para balancear carga
**Problema**: Default puede causar data skew si keys no distribuidas uniformemente

### **🟢 SPARK**
**Definición**: Motor de procesamiento distribuido optimizado para velocidad
**Key Innovation**: In-memory computing entre operaciones
**Performance**: 10-100x más rápido que MapReduce para workflows iterativos
**APIs**: Python (PySpark), SQL, Scala, Java
**Use Cases**: Analytics interactivo, Machine Learning, Streaming

### **🟢 RDD (Resilient Distributed Dataset)**
**Definición**: Estructura de datos distribuida e inmutable de Spark
**Resilient**: Se reconstruye automáticamente si partición falla
**Distributed**: Particionado automáticamente entre workers
**Immutable**: No se modifica, solo se crean nuevos RDDs
**Lazy**: Transformaciones no ejecutan hasta action

### **🟡 TRANSFORMATIONS vs ACTIONS**
**Transformations**: Operaciones lazy que definen nuevo RDD
- Ejemplos: map(), filter(), groupBy(), join()
- No ejecutan inmediatamente
**Actions**: Operaciones que disparan ejecución y retornan resultados
- Ejemplos: collect(), count(), save(), show()
- Fuerzan evaluation de todo el pipeline

### **🟡 LAZY EVALUATION**
**Definición**: Spark espera hasta action para ejecutar transformations
**Benefit**: Puede optimizar todo el pipeline antes de ejecutar
**Ejemplo**: Combina múltiples filters en una sola pasada
**Catalyst**: Optimizer que aprovecha lazy evaluation para generar código optimal

### **🔴 DAG (Directed Acyclic Graph)**
**Definición**: Spark crea grafo de dependencias entre RDDs
**Optimization**: Analiza DAG completo para optimizar ejecución
**Stage Boundaries**: Shuffle operations crean nuevos stages
**Fault Recovery**: Si partition falla, recalcula desde dependencias en DAG

---

## 🚀 **SESIÓN 3: SPARK AVANZADO + SQL**

### **🟢 DATAFRAME**
**Definición**: RDD con schema (estructura de columnas tipadas)
**Benefit**: Optimización automática + API más simple que RDD
**Performance**: 2-5x más rápido que RDDs por optimizaciones de Catalyst
**API**: Similar a tablas SQL o pandas DataFrames
**Schema**: Estructura se infiere automáticamente o se define explícitamente

### **🟡 CATALYST OPTIMIZER**
**Definición**: Motor de optimización que mejora queries automáticamente
**Fases**: Parse → Analyze → Optimize → Code Generation
**Optimizations**: Predicate pushdown, join reordering, constant folding
**Result**: Código Java generado optimally
**Benefit**: Escribes SQL simple, obtienes performance de expert

### **🟡 PREDICATE PUSHDOWN**
**Definición**: Mover filtros lo más cerca posible de los datos
**Ejemplo**: En lugar de cargar tabla completa y luego filtrar, filtrar durante carga
**Storage Benefit**: Para formatos columnares (Parquet), lee solo partitions necesarias
**Network Benefit**: Transfiere menos datos por red

### **🟡 JOIN STRATEGIES**
**Broadcast Join**: Para tablas pequeñas (<10MB), copia tabla a todos los nodos
**Sort-Merge Join**: Para tablas grandes, particiona por join key y ordena
**Hash Join**: Construye hash table de tabla más pequeña
**Auto-selection**: Catalyst elige estrategia optimal automáticamente

### **🟡 PARTITIONING**
**Definición**: Control de cómo datos se distribuyen entre workers
**Hash Partitioning**: Distribución uniforme por hash de key
**Range Partitioning**: Por rangos de valores (útil para data ordenada)
**Custom Partitioning**: Lógica específica del negocio
**Benefit**: Queries por partition key no necesitan shuffle

### **🟡 CACHING/PERSISTENCE**
**Definición**: Mantener RDD/DataFrame en memoria para reuso
**Levels**: MEMORY_ONLY, MEMORY_AND_DISK, DISK_ONLY, etc.
**When to Cache**: Cuando mismo dataset se usa múltiples veces
**Memory Management**: Spark automáticamente desaloja cache cuando necesita memoria
**Performance**: 10-100x speedup para accesos posteriores

### **🟡 WINDOW FUNCTIONS**
**Definición**: Operaciones que analizan filas relacionadas sin GROUP BY
**Tipos**: RANK(), LAG(), LEAD(), SUM() OVER(), etc.
**Partitioning**: Define scope de window (PARTITION BY)
**Ordering**: Define orden dentro de window (ORDER BY)
**Use Cases**: Rankings, moving averages, comparaciones temporales

### **🔴 DATA SKEW**
**Definición**: Distribución desigual de datos que causa cuellos de botella
**Problema**: Una partition con millones de records, otras con miles
**Detection**: Analizar partition sizes, buscar outliers
**Solutions**: Salting, custom partitioning, separate processing para hot keys
**Impact**: Puede convertir job de 5 minutos en 45 minutos

### **🔴 SALTING**
**Definición**: Técnica para distribuir hot keys agregando randomness
**Proceso**: Agregar suffix random a keys problemáticas
**Ejemplo**: "route_001" → "route_001_0", "route_001_1", etc.
**Trade-off**: Más complejidad pero mejor distribución
**When to Use**: Cuando tienes keys con 10x+ más datos que otras

### **🔴 ADAPTIVE QUERY EXECUTION (AQE)**
**Definición**: Optimización dinámica durante ejecución del query
**Features**: Dynamic coalescing, skew handling, join strategy switching
**Process**: Ejecuta stage → analiza estadísticas → re-optimiza próximo stage
**Configuration**: spark.sql.adaptive.enabled=true
**Benefit**: 2-5x speedup automático en muchos casos

### **🟡 BROADCAST VARIABLES**
**Definición**: Variables read-only compartidas eficientemente a todos los workers
**Use Case**: Lookup tables, configuration data, small reference datasets
**Efficiency**: Se envía una vez por worker, no una vez por task
**Example**: Broadcast pequeña tabla para joins

### **🟡 ACCUMULATORS**
**Definición**: Variables shared que solo se pueden "agregar" (counters)
**Use Cases**: Contadores, métricas, debugging info
**Thread Safety**: Spark garantiza updates atómicos
**Visibility**: Solo driver puede leer valor final

---

## 🌊 **CONCEPTOS PARA SESIONES FUTURAS (4-6)**

### **🟢 APACHE KAFKA**
**Definición**: Plataforma de streaming distribuida para eventos en tiempo real
**Architecture**: Producers → Brokers → Consumers
**Use Cases**: Event streaming, log aggregation, real-time analytics
**Key Features**: High throughput, fault tolerant, horizontally scalable

### **🟢 TOPICS & PARTITIONS**
**Topic**: Canal o categoría de mensajes (ej: "user_clicks", "transactions")
**Partition**: Subdivisión de topic para paralelismo y ordenamiento
**Ordering**: Garantizado dentro de partition, no entre partitions
**Scaling**: Más partitions = más paralelismo

### **🟡 PRODUCERS & CONSUMERS**
**Producer**: Aplicación que envía mensajes a Kafka topics
**Consumer**: Aplicación que lee mensajes de Kafka topics
**Consumer Groups**: Múltiples consumers trabajando juntos para paralelismo
**Offset**: Posición de último mensaje leído por consumer

### **🟡 SPARK STREAMING**
**Definición**: Extensión de Spark para procesamiento de streams en tiempo real
**Micro-batching**: Procesa streams como series de pequeños batches
**Sources**: Kafka, TCP sockets, file systems
**Fault Tolerance**: Exactly-once processing con checkpointing

### **🟡 WINDOWING**
**Definición**: Agrupar eventos de stream en ventanas de tiempo
**Tumbling Window**: Ventanas fijas sin overlap (0-5min, 5-10min)
**Sliding Window**: Ventanas con overlap (0-5min, 2-7min, 4-9min)
**Session Window**: Agrupación por periodos de actividad

---

## 🔧 **CONCEPTOS OPERACIONALES**

### **🟢 CLUSTER MANAGER**
**Definición**: Sistema que coordina recursos entre aplicaciones
**Tipos**: Spark Standalone, YARN, Kubernetes, Mesos
**Responsabilidad**: Asignar CPU/memoria, programar jobs, manejar fallos

### **🟢 EXECUTOR**
**Definición**: Proceso worker que ejecuta tasks en un nodo
**Resources**: CPU cores y memoria asignados por cluster manager
**Lifetime**: Dura toda la aplicación Spark
**Tasks**: Múltiples tasks pueden ejecutar en paralelo en un executor

### **🟡 DRIVER PROGRAM**
**Definición**: Proceso que ejecuta función main() y coordina workers
**Responsibilities**: Crear RDDs, enviar tasks a executors, recolectar resultados
**Location**: Puede correr en cluster o en máquina cliente
**Failure**: Si driver falla, toda la aplicación falla

### **🟡 CHECKPOINTING**
**Definición**: Guardar estado de RDD a storage confiable
**Purpose**: Evitar recomputation costosa de RDDs complejos
**Types**: RDD checkpointing, Streaming checkpointing
**Trade-off**: Overhead de write vs protection contra failure

### **🔴 GARBAGE COLLECTION (GC)**
**Definición**: Proceso de limpieza automática de memoria no usada
**Impact**: GC pauses pueden afectar performance
**Monitoring**: GC time debería ser <10% de task time
**Tuning**: Adjustar executor memory, usar off-heap storage

---

## 📊 **MÉTRICAS Y MONITORING**

### **🟡 THROUGHPUT**
**Definición**: Cantidad de datos procesados por unidad de tiempo
**Medidas**: Records/second, MB/second, GB/hour
**Factors**: Paralelismo, I/O efficiency, network bandwidth

### **🟡 LATENCY**
**Definición**: Tiempo desde que llega dato hasta que se produce resultado
**Types**: End-to-end latency, processing latency
**Trade-off**: Throughput vs latency (batch size tuning)

### **🟡 RESOURCE UTILIZATION**
**CPU**: Porcentaje de cores siendo usados
**Memory**: RAM usado vs disponible, cache hit rates
**Network**: Bandwidth usado para shuffle operations
**Storage**: I/O rates, disk utilization

### **🔴 BACKPRESSURE**
**Definición**: Mecanismo para manejar cuando producer va más rápido que consumer
**Streaming**: Adjustar batch sizes automáticamente
**Kafka**: Consumer lag monitoring
**Spark**: Dynamic allocation de resources

---

## 🎯 **PATRONES COMUNES Y BEST PRACTICES**

### **🟡 ETL PATTERN**
**Extract**: Leer datos de múltiples fuentes (databases, APIs, files)
**Transform**: Limpiar, agregrar, enriquecer datos
**Load**: Escribir a data lake, data warehouse, o database
**Spark Role**: Procesar transformations distributively

### **🟡 LAMBDA ARCHITECTURE**
**Batch Layer**: Procesamiento batch para accuracy (HDFS + Spark)
**Speed Layer**: Procesamiento real-time para latency (Kafka + Spark Streaming)  
**Serving Layer**: Combine batch + real-time results
**Trade-off**: Complexity vs comprehensive coverage

### **🟡 KAPPA ARCHITECTURE**
**Single Pipeline**: Todo a través de streaming (Kafka + Spark Streaming)
**Simplicity**: Elimina complejidad de mantener dos systems
**Trade-off**: Menos optimization para pure batch workloads

### **🔴 SMALL FILES PROBLEM**
**Problem**: HDFS ineficiente con millones de archivos pequeños
**NameNode Impact**: Cada file consume ~150 bytes de memoria
**Performance**: Más overhead que datos útiles
**Solutions**: Compaction, sequence files, appropriate partitioning

---

## 🚨 **TROUBLESHOOTING COMÚN**

### **🟡 OUT OF MEMORY**
**Causes**: RDDs muy grandes, cache excesivo, data skew
**Solutions**: Increase executor memory, reduce data size, partition better
**Prevention**: Monitor memory usage, use appropriate storage levels

### **🟡 SLOW PERFORMANCE**
**Causes**: Data skew, small files, poor partitioning, network bottlenecks
**Diagnosis**: Spark UI, job timeline, task distribution
**Solutions**: Repartition, cache strategically, optimize joins

### **🟡 CONNECTION FAILURES**
**Causes**: Network issues, timeouts, firewall blocks
**Symptoms**: Tasks failing with connection errors
**Solutions**: Increase timeouts, check network config, retry policies

### **🔴 DATA CORRUPTION**
**Causes**: Hardware failures, software bugs, network errors
**Detection**: Checksums, data validation, monitoring
**Recovery**: Replication, backups, recomputation from source

---

## 📖 **RECURSOS PARA PROFUNDIZAR**

### **Documentación Oficial**
- Apache Spark: https://spark.apache.org/docs/
- Apache Hadoop: https://hadoop.apache.org/docs/
- Apache Kafka: https://kafka.apache.org/documentation/

### **Libros Recomendados**
- "Learning Spark" by Holden Karau
- "Hadoop: The Definitive Guide" by Tom White
- "Designing Data-Intensive Applications" by Martin Kleppmann

### **Cursos Online**
- Databricks Academy (gratuito)
- Coursera Big Data Specialization
- edX Introduction to Apache Spark

---

## 🎯 **CHECKLIST DE COMPETENCIAS**

### **Sesión 0: Foundation** ✅
- [ ] Entiendo distributed systems thinking
- [ ] Puedo configurar Docker environment
- [ ] Comprendo fault tolerance principles
- [ ] Domino data locality concept

### **Sesión 1: HDFS** ✅  
- [ ] Explico arquitectura NameNode/DataNode
- [ ] Entiendo replication y metadata
- [ ] Puedo troubleshoot cluster issues
- [ ] Analizo distribución de datos

### **Sesión 2: Processing** ✅
- [ ] Implemento MapReduce jobs
- [ ] Comparo MapReduce vs Spark
- [ ] Optimizo con combiners
- [ ] Entiendo lazy evaluation

### **Sesión 3: Advanced Spark** ✅
- [ ] Uso DataFrames y Catalyst
- [ ] Optimizo joins y partitioning  
- [ ] Resuelvo data skew
- [ ] Implemento complex analytics

**🎉 ¡Usa este diccionario como tu guía definitiva para dominar Big Data!**