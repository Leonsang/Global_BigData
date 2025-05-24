# ⚡ Práctica 2: Procesamiento con Spark

## Descripción
Este entorno está configurado para la práctica de Apache Spark, enfocándose en el procesamiento distribuido de datos. Incluye un cluster Spark con HDFS para almacenamiento persistente.

## Servicios Disponibles

### Spark Cluster
- **Master UI**: http://localhost:8080
- **Worker UI**: http://localhost:8081
- **Configuración**:
  - 2 Workers
  - 2GB RAM por Worker
  - 2 Cores por Worker

### HDFS (Hadoop Distributed File System)
- **NameNode UI**: http://localhost:9870
- **API**: hdfs://namenode:9000

### Jupyter Lab
- **URL**: http://localhost:8888
- **Volúmenes Montados**:
  - `/home/jovyan/sessions`: Sesiones de trabajo
  - `/home/jovyan/datasets`: Datos del proyecto

## Ejercicios

### 1. Configuración de Spark
```python
# Inicializar Spark
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("MiAplicacion") \
    .config("spark.executor.memory", "2g") \
    .getOrCreate()
```

### 2. Procesamiento de Datos
```python
# Leer datos de HDFS
df = spark.read.csv("hdfs://namenode:9000/datos/archivo.csv")

# Transformaciones básicas
df_transformed = df.select("columna1", "columna2") \
    .filter("columna1 > 0") \
    .groupBy("columna2") \
    .count()
```

### 3. Análisis Avanzado
```python
# Joins y agregaciones
df1 = spark.read.parquet("hdfs://namenode:9000/datos/df1")
df2 = spark.read.parquet("hdfs://namenode:9000/datos/df2")

resultado = df1.join(df2, "id") \
    .groupBy("categoria") \
    .agg({"valor": "avg", "cantidad": "sum"})
```

## Estructura de Directorios
```
practice-02/
├── docker-compose.yml    # Configuración Spark + HDFS
├── hadoop.env           # Variables de entorno
└── README.md           # Este archivo
```

## Comandos Útiles

### Gestión del Cluster
```bash
# Ver estado del cluster
curl http://localhost:8080

# Ver logs del master
docker logs spark_master

# Ver logs de un worker
docker logs spark_worker_1
```

### Spark Submit
```bash
# Ejecutar aplicación
spark-submit \
    --master spark://spark_master:7077 \
    --deploy-mode cluster \
    mi_aplicacion.py
```

## Solución de Problemas

### Spark Master
- Si el Master no inicia:
  ```bash
  docker logs spark_master
  ```
- Para reiniciar el cluster:
  ```bash
  docker-compose restart
  ```

### Spark Workers
- Si los Workers no conectan:
  ```bash
  docker logs spark_worker_1
  ```
- Para verificar recursos:
  ```bash
  curl http://localhost:8080/metrics/json
  ```

## Notas de Aprendizaje

1. **Conceptos Clave**:
   - RDDs vs DataFrames
   - Transformaciones y Acciones
   - Particionamiento
   - Persistencia de datos

2. **Buenas Prácticas**:
   - Usa DataFrames en lugar de RDDs cuando sea posible
   - Aprovecha el particionamiento para optimizar
   - Persiste datos frecuentemente usados
   - Monitorea el uso de memoria

3. **Optimización**:
   - Ajusta el número de particiones
   - Configura la memoria del executor
   - Usa broadcast variables para joins
   - Implementa checkpointing para DAGs largos

## Próximos Pasos

1. Familiarízate con la UI de Spark
2. Practica operaciones básicas con DataFrames
3. Experimenta con diferentes configuraciones
4. Prepara para la integración con Kafka en la siguiente práctica 