# 🚀 Sesión 6: Apache Kafka

## 📚 Objetivos de la Sesión
- Comprender los fundamentos de Kafka
- Implementar productores y consumidores
- Diseñar arquitecturas event-driven
- Optimizar el rendimiento

## 🎯 Contenido

### 1. Introducción a Kafka
- ¿Qué es Apache Kafka?
- Casos de uso típicos
- Arquitectura general
- Componentes principales

### 2. Conceptos Fundamentales
- Topics y Partitions
- Brokers y Clusters
- Producers y Consumers
- Consumer Groups

### 3. Implementación de Productores
- Configuración básica
- Serialización
- Acks y retries
- Batching y compresión

### 4. Implementación de Consumidores
- Configuración de grupos
- Offset management
- Rebalancing
- Error handling

## 🛠️ Hands-on

### Ejercicio 1: Productor Básico
```python
from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

# Enviar mensaje
producer.send('topic', {'key': 'value'})
producer.flush()
```

### Ejercicio 2: Consumidor Básico
```python
from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'topic',
    bootstrap_servers=['localhost:9092'],
    value_deserializer=lambda x: json.loads(x.decode('utf-8')),
    group_id='my-group'
)

# Consumir mensajes
for message in consumer:
    print(message.value)
```

### Ejercicio 3: Configuración Avanzada
```python
# Productor con configuración avanzada
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    acks='all',
    retries=3,
    batch_size=16384,
    compression_type='gzip'
)

# Consumidor con configuración avanzada
consumer = KafkaConsumer(
    'topic',
    bootstrap_servers=['localhost:9092'],
    group_id='my-group',
    auto_offset_reset='earliest',
    enable_auto_commit=False
)
```

## 📊 Entregables
- Implementación de productor
- Implementación de consumidor
- Arquitectura event-driven
- Reporte de optimización

## 🔍 Recursos Adicionales
- [Kafka Documentation](https://kafka.apache.org/documentation/)
- [Kafka Python Client](https://kafka-python.readthedocs.io/)
- [Kafka Best Practices](https://www.confluent.io/blog/kafka-client-side-tuning-file-uploads/)

## 🎯 Próximos Pasos
- Integración con Spark
- Arquitecturas Lambda
- Event Sourcing
- Microservicios 