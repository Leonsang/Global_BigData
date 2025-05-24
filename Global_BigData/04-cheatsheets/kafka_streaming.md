---

## ⚡ **SPARK STREAMING CON KAFKA**

### **Setup Básico Spark Streaming**
```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

# Configurar Spark con Kafka
spark = SparkSession.builder \
    .appName("KafkaStreaming") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.1") \
    .getOrCreate()

# Schema de los datos de transacciones
transaction_schema = StructType([
    StructField("user_id", StringType(), True),
    StructField("amount", DoubleType(), True),
    StructField("location", StringType(), True),
    StructField("timestamp", TimestampType(), True)
])

# Leer stream desde Kafka
kafka_stream = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "transacciones") \
    .option("startingOffsets", "latest") \
    .load()

# Parsear mensajes JSON
parsed_stream = kafka_stream \
    .select(
        col("key").cast("string").alias("user_key"),
        from_json(col("value").cast("string"), transaction_schema).alias("data"),
        col("timestamp").alias("kafka_timestamp")
    ) \
    .select("user_key", "data.*", "kafka_timestamp")

# Mostrar stream
query = parsed_stream \
    .writeStream \
    .outputMode("append") \
    .format("console") \
    .trigger(processingTime="10 seconds") \
    .start()

query.awaitTermination()
```

### **Agregaciones en Tiempo Real**
```python
# Agregaciones por ventanas de tiempo
windowed_aggregations = parsed_stream \
    .withWatermark("timestamp", "10 minutes") \
    .groupBy(
        window(col("timestamp"), "5 minutes", "1 minute"),
        col("location")
    ) \
    .agg(
        count("*").alias("transaction_count"),
        sum("amount").alias("total_amount"),
        avg("amount").alias("avg_amount"),
        max("amount").alias("max_amount")
    )

# Escribir a Kafka topic de salida
kafka_output = windowed_aggregations \
    .select(
        to_json(struct("*")).alias("value")
    ) \
    .writeStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("topic", "transaction_analytics") \
    .option("checkpointLocation", "/tmp/checkpoint") \
    .outputMode("update") \
    .start()
```

### **Detección de Anomalías en Tiempo Real**
```python
# Detectar transacciones sospechosas
anomaly_detection = parsed_stream \
    .filter(
        (col("amount") > 5000) |  # Monto alto
        (col("location").isin(["suspicious_country1", "suspicious_country2"]))
    ) \
    .withColumn("alert_type", 
        when(col("amount") > 10000, "high_amount")
        .when(col("location").isin(["suspicious_country1"]), "suspicious_location")
        .otherwise("general_alert")
    ) \
    .withColumn("severity", 
        when(col("amount") > 10000, "critical")
        .when(col("amount") > 5000, "high")
        .otherwise("medium")
    )

# Enviar alertas a topic especial
alert_output = anomaly_detection \
    .select(
        col("user_id").alias("key"),
        to_json(struct("*")).alias("value")
    ) \
    .writeStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("topic", "fraud_alerts") \
    .option("checkpointLocation", "/tmp/fraud_checkpoint") \
    .start()
```

---

## 🔧 **CONFIGURACIÓN DOCKER COMPOSE KAFKA**

### **Docker Compose Optimizado**
```yaml
version: '3.8'

services:
  zookeeper:
    image: confluentinc/cp-zookeeper:7.0.1
    container_name: zookeeper
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181
      ZOOKEEPER_TICK_TIME: 2000
      ZOOKEEPER_SYNC_LIMIT: 2
    networks:
      - kafka-net

  kafka-1:
    image: confluentinc/cp-kafka:7.0.1
    container_name: kafka-1
    depends_on:
      - zookeeper
    ports:
      - "9092:9092"
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka-1:29092,PLAINTEXT_HOST://localhost:9092
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: PLAINTEXT:PLAINTEXT,PLAINTEXT_HOST:PLAINTEXT
      KAFKA_INTER_BROKER_LISTENER_NAME: PLAINTEXT
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 2
      KAFKA_AUTO_CREATE_TOPICS_ENABLE: 'true'
      KAFKA_DELETE_TOPIC_ENABLE: 'true'
      KAFKA_GROUP_INITIAL_REBALANCE_DELAY_MS: 0
    networks:
      - kafka-net

  kafka-2:
    image: confluentinc/cp-kafka:7.0.1
    container_name: kafka-2
    depends_on:
      - zookeeper
    ports:
      - "9093:9093"
    environment:
      KAFKA_BROKER_ID: 2
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka-2:29093,PLAINTEXT_HOST://localhost:9093
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: PLAINTEXT:PLAINTEXT,PLAINTEXT_HOST:PLAINTEXT
      KAFKA_INTER_BROKER_LISTENER_NAME: PLAINTEXT
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 2
    networks:
      - kafka-net

  # Kafka UI para monitoreo
  kafka-ui:
    image: provectuslabs/kafka-ui:latest
    container_name: kafka-ui
    depends_on:
      - kafka-1
      - kafka-2
    ports:
      - "8090:8080"
    environment:
      KAFKA_CLUSTERS_0_NAME: local
      KAFKA_CLUSTERS_0_BOOTSTRAPSERVERS: kafka-1:29092,kafka-2:29093
      KAFKA_CLUSTERS_0_ZOOKEEPER: zookeeper:2181
    networks:
      - kafka-net

networks:
  kafka-net:
    driver: bridge
```

### **Comandos Útiles Docker**
```bash
# Iniciar cluster Kafka
docker-compose up -d

# Verificar que funciona
docker-compose ps

# Acceder a Kafka UI
# http://localhost:8090

# Ejecutar comandos Kafka dentro del container
docker exec -it kafka-1 kafka-topics --list --bootstrap-server localhost:29092

# Ver logs
docker-compose logs kafka-1
```

---

## 📊 **PATRONES COMUNES DE STREAMING**

### **ETL en Tiempo Real**
```python
def kafka_etl_pipeline():
    # Extract: Leer desde Kafka
    raw_stream = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("subscribe", "raw_events") \
        .load()
    
    # Transform: Limpiar y enriquecer datos
    cleaned_stream = raw_stream \
        .select(from_json(col("value").cast("string"), event_schema).alias("data")) \
        .select("data.*") \
        .filter(col("user_id").isNotNull()) \
        .withColumn("processed_timestamp", current_timestamp()) \
        .withColumn("date_partition", date_format(col("event_time"), "yyyy-MM-dd"))
    
    # Load: Escribir a HDFS particionado
    hdfs_output = cleaned_stream \
        .writeStream \
        .format("parquet") \
        .option("path", "hdfs://namenode:9000/data/events") \
        .option("checkpointLocation", "/tmp/etl_checkpoint") \
        .partitionBy("date_partition") \
        .trigger(processingTime="1 minute") \
        .start()
    
    return hdfs_output
```

### **Join entre Streams**
```python
# Stream de transacciones
transactions = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "transactions") \
    .load() \
    .select(from_json(col("value").cast("string"), transaction_schema).alias("txn")) \
    .select("txn.*")

# Stream de información de usuarios
user_updates = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "user_updates") \
    .load() \
    .select(from_json(col("value").cast("string"), user_schema).alias("user")) \
    .select("user.*")

# Stream-stream join
enriched_transactions = transactions \
    .withWatermark("timestamp", "10 minutes") \
    .join(
        user_updates.withWatermark("update_time", "5 minutes"),
        expr("""
            user_id = user_id AND
            timestamp >= update_time AND
            timestamp <= update_time + interval 1 hour
        """)
    )
```

### **Manejo de Late Data y Watermarks**
```python
# Configurar watermark para manejo de datos tardíos
late_data_stream = parsed_stream \
    .withWatermark("timestamp", "5 minutes") \
    .groupBy(
        window(col("timestamp"), "10 minutes"),
        col("user_id")
    ) \
    .agg(
        count("*").alias("transaction_count"),
        sum("amount").alias("total_spent")
    )

# Los datos que lleguen más de 5 minutos tarde serán descartados
# Las ventanas se cerrarán 5 minutos después del watermark
```

---

## 🚨 **MONITOREO Y ALERTAS**

### **Producer con Métricas**
```python
import time
from kafka.errors import KafkaError

class MonitoredProducer:
    def __init__(self, bootstrap_servers):
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        self.messages_sent = 0
        self.errors = 0
        self.start_time = time.time()
    
    def send_message(self, topic, message):
        try:
            future = self.producer.send(topic, message)
            future.get(timeout=10)  # Bloquear para detectar errores
            self.messages_sent += 1
            
            # Log estadísticas cada 1000 mensajes
            if self.messages_sent % 1000 == 0:
                self.log_stats()
                
        except KafkaError as e:
            self.errors += 1
            print(f"Error enviando mensaje: {e}")
    
    def log_stats(self):
        elapsed_time = time.time() - self.start_time
        rate = self.messages_sent / elapsed_time if elapsed_time > 0 else 0
        print(f"Estadísticas: {self.messages_sent} enviados, "
              f"{self.errors} errores, "
              f"{rate:.2f} msg/seg")
    
    def close(self):
        self.producer.flush()
        self.producer.close()
        self.log_stats()

# Uso
producer = MonitoredProducer(['localhost:9092'])
for i in range(10000):
    message = {"id": i, "timestamp": time.time()}
    producer.send_message("test_topic", message)
producer.close()
```

### **Consumer Lag Monitoring**
```python
from kafka.admin import KafkaAdminClient, ConfigResource, ConfigResourceType
from kafka import TopicPartition

def monitor_consumer_lag(bootstrap_servers, group_id, topic):
    """Monitorear lag de consumer group"""
    
    consumer = KafkaConsumer(
        bootstrap_servers=bootstrap_servers,
        group_id=group_id
    )
    
    # Obtener particiones del topic
    partitions = consumer.partitions_for_topic(topic)
    topic_partitions = [TopicPartition(topic, p) for p in partitions]
    
    # Obtener latest offsets
    latest_offsets = consumer.end_offsets(topic_partitions)
    
    # Obtener committed offsets del grupo
    committed_offsets = consumer.committed(set(topic_partitions))
    
    total_lag = 0
    for tp in topic_partitions:
        latest = latest_offsets[tp]
        committed = committed_offsets.get(tp)
        
        if committed is not None:
            lag = latest - committed.offset
            print(f"Partition {tp.partition}: lag = {lag}")
            total_lag += lag
        else:
            print(f"Partition {tp.partition}: no committed offset")
    
    print(f"Total lag: {total_lag}")
    consumer.close()
    return total_lag

# Ejecutar monitoreo
lag = monitor_consumer_lag(['localhost:9092'], 'analytics-group', 'transactions')
if lag > 10000:
    print("⚠️ Alto lag detectado!")
```

---

## 🔄 **CASOS DE USO PRÁCTICOS**

### **Sistema de Recomendaciones en Tiempo Real**
```python
# Producer de eventos de usuario
def send_user_activity(user_id, action, item_id):
    activity = {
        'user_id': user_id,
        'action': action,  # 'view', 'click', 'purchase'
        'item_id': item_id,
        'timestamp': datetime.now().isoformat()
    }
    
    producer.send('user_activity', key=str(user_id), value=activity)

# Consumer para actualizar modelo
def process_user_activity():
    consumer = KafkaConsumer(
        'user_activity',
        bootstrap_servers=['localhost:9092'],
        group_id='recommendation_engine',
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )
    
    for message in consumer:
        activity = message.value
        
        # Actualizar perfil de usuario
        update_user_profile(activity['user_id'], activity)
        
        # Generar recomendaciones inmediatas
        if activity['action'] == 'purchase':
            recommendations = generate_recommendations(activity['user_id'])
            send_recommendations(activity['user_id'], recommendations)
```

### **Monitoreo de IoT en Tiempo Real**
```python
# Stream processing para sensores IoT
def iot_monitoring_pipeline():
    # Schema para datos de sensores
    sensor_schema = StructType([
        StructField("sensor_id", StringType(), True),
        StructField("temperature", DoubleType(), True),
        StructField("humidity", DoubleType(), True),
        StructField("pressure", DoubleType(), True),
        StructField("timestamp", TimestampType(), True)
    ])
    
    # Leer datos de sensores
    sensor_stream = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("subscribe", "sensor_data") \
        .load() \
        .select(from_json(col("value").cast("string"), sensor_schema).alias("data")) \
        .select("data.*")
    
    # Detectar anomalías
    anomalies = sensor_stream \
        .filter(
            (col("temperature") > 80) |  # Temperatura alta
            (col("humidity") > 90) |     # Humedad alta
            (col("pressure") < 950)      # Presión baja
        ) \
        .withColumn("alert_level",
            when(col("temperature") > 100, "critical")
            .when(col("temperature") > 80, "warning")
            .otherwise("info")
        )
    
    # Enviar alertas
    alert_query = anomalies \
        .select(
            col("sensor_id").alias("key"),
            to_json(struct("*")).alias("value")
        ) \
        .writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("topic", "sensor_alerts") \
        .start()
    
    return alert_query
```

### **Análisis de Logs en Tiempo Real**
```python
# Parser de logs de Apache/Nginx
import re

def parse_log_line(log_line):
    # Regex para formato de log común
    pattern = r'(\S+) \S+ \S+ \[([\w:/]+\s[+\-]\d{4})\] "(\S+) (\S+) (\S+)" (\d{3}) (\d+|-)'
    match = re.match(pattern, log_line)
    
    if match:
        return {
            'ip': match.group(1),
            'timestamp': match.group(2),
            'method': match.group(3),
            'url': match.group(4),
            'protocol': match.group(5),
            'status_code': int(match.group(6)),
            'response_size': int(match.group(7)) if match.group(7) != '-' else 0
        }
    return None

# Stream processing de logs
def log_analysis_pipeline():
    # Leer logs desde Kafka
    log_stream = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("subscribe", "web_logs") \
        .load() \
        .select(col("value").cast("string").alias("log_line"))
    
    # Parsear logs usando UDF
    parse_log_udf = udf(parse_log_line, StructType([
        StructField("ip", StringType(), True),
        StructField("timestamp", StringType(), True),
        StructField("method", StringType(), True),
        StructField("url", StringType(), True),
        StructField("protocol", StringType(), True),
        StructField("status_code", IntegerType(), True),
        StructField("response_size", IntegerType(), True)
    ]))
    
    parsed_logs = log_stream \
        .withColumn("parsed", parse_log_udf(col("log_line"))) \
        .select("parsed.*") \
        .filter(col("ip").isNotNull())
    
    # Detectar errores 4xx y 5xx
    error_logs = parsed_logs \
        .filter(col("status_code") >= 400) \
        .withColumn("error_type",
            when(col("status_code") < 500, "client_error")
            .otherwise("server_error")
        )
    
    # Contar errores por minuto
    error_counts = error_logs \
        .withWatermark("timestamp", "2 minutes") \
        .groupBy(
            window(col("timestamp"), "1 minute"),
            col("error_type")
        ) \
        .count()
    
    return error_counts
```

---

## 🎯 **EJEMPLO INTEGRADOR: SISTEMA COMPLETO**

```python
"""
Sistema completo de análisis de transacciones en tiempo real
Incluye: Producer, Consumer, Spark Streaming, y alertas
"""

class TransactionProcessingSystem:
    def __init__(self, kafka_servers):
        self.kafka_servers = kafka_servers
        self.setup_spark()
        self.setup_producer()
    
    def setup_spark(self):
        self.spark = SparkSession.builder \
            .appName("TransactionProcessing") \
            .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.1") \
            .getOrCreate()
    
    def setup_producer(self):
        self.producer = KafkaProducer(
            bootstrap_servers=self.kafka_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            key_serializer=lambda k: str(k).encode('utf-8')
        )
    
    def generate_transactions(self, num_transactions=1000):
        """Generar transacciones simuladas"""
        import random
        
        for i in range(num_transactions):
            transaction = {
                'transaction_id': f"txn_{i}",
                'user_id': f"user_{random.randint(1, 100)}",
                'amount': round(random.uniform(10, 5000), 2),
                'merchant': random.choice(['Amazon', 'Walmart', 'Target', 'Costco']),
                'category': random.choice(['Electronics', 'Groceries', 'Clothing', 'Gas']),
                'timestamp': datetime.now().isoformat(),
                'location': random.choice(['Madrid', 'Barcelona', 'Valencia', 'Sevilla'])
            }
            
            self.producer.send('transactions', 
                             key=transaction['user_id'], 
                             value=transaction)
            
            time.sleep(0.1)  # Simular flujo real
    
    def start_fraud_detection(self):
        """Detectar fraude en tiempo real"""
        transaction_schema = StructType([
            StructField("transaction_id", StringType(), True),
            StructField("user_id", StringType(), True),
            StructField("amount", DoubleType(), True),
            StructField("merchant", StringType(), True),
            StructField("category", StringType(), True),
            StructField("timestamp", TimestampType(), True),
            StructField("location", StringType(), True)
        ])
        
        # Leer stream de transacciones
        transactions = self.spark \
            .readStream \
            .format("kafka") \
            .option("kafka.bootstrap.servers", ','.join(self.kafka_servers)) \
            .option("subscribe", "transactions") \
            .load() \
            .select(from_json(col("value").cast("string"), transaction_schema).alias("txn")) \
            .select("txn.*")
        
        # Reglas de detección de fraude
        fraud_detection = transactions \
            .withColumn("is_fraud",
                when(col("amount") > 3000, True)  # Monto alto
                .when(col("category") == "Electronics" & col("amount") > 1000, True)
                .otherwise(False)
            ) \
            .withColumn("risk_score",
                when(col("amount") > 3000, 100)
                .when(col("amount") > 1000, 75)
                .when(col("amount") > 500, 50)
                .otherwise(25)
            )
        
        # Enviar alertas de fraude
        fraud_alerts = fraud_detection \
            .filter(col("is_fraud") == True) \
            .select(
                col("user_id").alias("key"),
                to_json(struct("*")).alias("value")
            ) \
            .writeStream \
            .format("kafka") \
            .option("kafka.bootstrap.servers", ','.join(self.kafka_servers)) \
            .option("topic", "fraud_alerts") \
            .option("checkpointLocation", "/tmp/fraud_checkpoint") \
            .start()
        
        return fraud_alerts
    
    def start_analytics(self):
        """Análisis en tiempo real"""
        # Leer transacciones
        transactions = self.spark \
            .readStream \
            .format("kafka") \
            .option("kafka.bootstrap.servers", ','.join(self.kafka_servers)) \
            .option("subscribe", "transactions") \
            .load() \
            .select(from_json(col("value").cast("string"), transaction_schema).alias("txn")) \
            .select("txn.*")
        
        # Agregaciones por ventana de tiempo
        analytics = transactions \
            .withWatermark("timestamp", "10 minutes") \
            .groupBy(
                window(col("timestamp"), "5 minutes"),
                col("category"),
                col("location")
            ) \
            .agg(
                count("*").alias("transaction_count"),
                sum("amount").alias("total_revenue"),
                avg("amount").alias("avg_transaction"),
                countDistinct("user_id").alias("unique_users")
            )
        
        # Escribir resultados
        analytics_output = analytics \
            .writeStream \
            .format("console") \
            .outputMode("update") \
            .trigger(processingTime="30 seconds") \
            .start()
        
        return analytics_output

# Uso del sistema
if __name__ == "__main__":
    system = TransactionProcessingSystem(['localhost:9092'])
    
    # Iniciar detección de fraude
    fraud_query = system.start_fraud_detection()
    
    # Iniciar analytics
    analytics_query = system.start_analytics()
    
    # Generar transacciones (en otro proceso)
    import threading
    generator_thread = threading.Thread(target=system.generate_transactions, args=(10000,))
    generator_thread.start()
    
    # Esperar por las queries
    fraud_query.awaitTermination()
```

---

## 📋 **CHECKLIST DE COMPETENCIAS KAFKA**

### **Básico** ✅
- [ ] Creo y gestiono topics con CLI
- [ ] Implemento producer y consumer básicos en Python
- [ ] Entiendo conceptos de particiones y offsets
- [ ] Configuro Docker Compose para Kafka

### **Intermedio** ✅
- [ ] Uso Spark Streaming con Kafka
- [ ] Implemento windowing y watermarks
- [ ] Manejo consumer groups y rebalancing
- [ ] Monitoreo lag y performance

### **Avanzado** ✅
- [ ] Diseño arquitecturas de streaming completas
- [ ] Optimizo performance y throughput
- [ ] Implemento exactly-once semantics
- [ ] Integro con sistemas de alertas y monitoreo

**💡 Tip Final: Kafka es el corazón de arquitecturas de datos modernas. ¡Domínalo y serás indispensable!**
