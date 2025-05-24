# 🔄 Práctica 3: Procesamiento en Tiempo Real con Kafka y Spark

## Descripción
Este entorno está configurado para la práctica de procesamiento de datos en tiempo real, combinando Apache Kafka para la ingesta de datos y Apache Spark para el procesamiento. Incluye un pipeline completo de streaming.

## Servicios Disponibles

### Kafka Cluster
- **Broker**: localhost:9092
- **Zookeeper**: localhost:2181
- **Kafka UI**: http://localhost:8080
- **Configuración**:
  - 1 Broker
  - 3 particiones por tópico
  - Retención: 7 días

### Spark Cluster
- **Master UI**: http://localhost:8081
- **Worker UI**: http://localhost:8082
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

### 1. Configuración de Kafka
```python
# Configuración del productor
from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers=['kafka:9092'],
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

# Enviar mensaje
producer.send('mi-topico', {'key': 'value'})
```

### 2. Procesamiento con Spark Streaming
```python
# Configuración de Spark Streaming
from pyspark.sql import SparkSession
from pyspark.sql.functions import *

spark = SparkSession.builder \
    .appName("StreamingApp") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.0") \
    .getOrCreate()

# Leer stream de Kafka
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "mi-topico") \
    .load()

# Procesar datos
query = df.selectExpr("CAST(value AS STRING)") \
    .writeStream \
    .outputMode("append") \
    .format("console") \
    .start()
```

### 3. Pipeline Completo
```python
# Productor de datos
def generate_data():
    while True:
        data = {
            'timestamp': datetime.now().isoformat(),
            'value': random.randint(1, 100)
        }
        producer.send('sensores', data)
        time.sleep(1)

# Consumidor con Spark
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "sensores") \
    .load()

# Procesamiento y almacenamiento
query = df.selectExpr("CAST(value AS STRING)") \
    .select(from_json("value", schema).alias("data")) \
    .select("data.*") \
    .writeStream \
    .format("parquet") \
    .option("path", "hdfs://namenode:9000/datos/streaming") \
    .option("checkpointLocation", "/checkpoint") \
    .start()
```

## Estructura de Directorios
```
practice-03/
├── docker-compose.yml    # Configuración Kafka + Spark + HDFS
├── hadoop.env           # Variables de entorno
└── README.md           # Este archivo
```

## Comandos Útiles

### Gestión de Kafka
```bash
# Listar tópicos
kafka-topics.sh --list --bootstrap-server kafka:9092

# Crear tópico
kafka-topics.sh --create \
    --bootstrap-server kafka:9092 \
    --topic mi-topico \
    --partitions 3 \
    --replication-factor 1

# Ver mensajes
kafka-console-consumer.sh \
    --bootstrap-server kafka:9092 \
    --topic mi-topico \
    --from-beginning
```

### Gestión del Cluster
```bash
# Ver estado de Kafka
docker logs kafka

# Ver estado de Spark
curl http://localhost:8081

# Ver logs de Zookeeper
docker logs zookeeper
```

## Solución de Problemas

### Kafka
- Si el broker no inicia:
  ```bash
  docker logs kafka
  ```
- Para problemas de conexión:
  ```bash
  kafka-topics.sh --describe --bootstrap-server kafka:9092
  ```

### Spark Streaming
- Si el job falla:
  ```bash
  docker logs spark_master
  ```
- Para verificar checkpoints:
  ```bash
  hdfs dfs -ls /checkpoint
  ```

## Notas de Aprendizaje

1. **Conceptos Clave**:
   - Tópicos y particiones en Kafka
   - Grupos de consumidores
   - Exactly-once processing
   - Checkpointing en Spark

2. **Buenas Prácticas**:
   - Diseña tópicos con el número correcto de particiones
   - Implementa manejo de errores robusto
   - Usa checkpoints para recuperación
   - Monitorea el lag de los consumidores

3. **Optimización**:
   - Ajusta el tamaño del batch en Spark
   - Configura el tiempo de retención en Kafka
   - Implementa backpressure
   - Usa ventanas para agregaciones

## Próximos Pasos

1. Familiarízate con la UI de Kafka
2. Practica la creación y gestión de tópicos
3. Experimenta con diferentes configuraciones de streaming
4. Implementa un pipeline completo de datos 