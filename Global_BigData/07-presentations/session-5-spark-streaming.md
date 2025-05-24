# ⚡ Sesión 5: Spark Structured Streaming

## 📚 Objetivos de la Sesión
- Comprender el procesamiento en tiempo real
- Implementar pipelines de streaming
- Aplicar ventanas y agregaciones
- Integrar con fuentes de datos

## 🎯 Contenido

### 1. Introducción al Streaming
- ¿Qué es Structured Streaming?
- Casos de uso
- Ventajas sobre batch
- Arquitectura general

### 2. Fuentes y Sinks
- Kafka como fuente
- File sources
- Console sink
- Custom sinks

### 3. Operaciones de Streaming
- Windowing
- Agregaciones
- Joins
- Watermarking

### 4. Monitoreo y Optimización
- Checkpointing
- Recovery
- Performance tuning
- Best practices

## 🛠️ Hands-on

### Ejercicio 1: Streaming Básico
```python
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("Streaming Example") \
    .getOrCreate()

# Leer stream
stream_df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "topic") \
    .load()
```

### Ejercicio 2: Windowing
```python
# Agregación con ventana
windowed_df = stream_df \
    .groupBy(
        window("timestamp", "5 minutes"),
        "key"
    ) \
    .agg({"value": "count"})
```

### Ejercicio 3: Output
```python
# Escribir stream
query = windowed_df.writeStream \
    .format("console") \
    .outputMode("complete") \
    .option("checkpointLocation", "/checkpoint") \
    .start()

query.awaitTermination()
```

## 📊 Entregables
- Pipeline de streaming implementado
- Análisis en tiempo real
- Reporte de performance

## 🔍 Recursos Adicionales
- [Structured Streaming Guide](https://spark.apache.org/docs/latest/structured-streaming-programming-guide.html)
- [Kafka Integration](https://spark.apache.org/docs/latest/structured-streaming-kafka-integration.html)
- [Streaming Best Practices](https://spark.apache.org/docs/latest/structured-streaming-programming-guide.html#handling-late-data-and-watermarking)

## 🎯 Próxima Sesión
- Apache Kafka
- Casos de Uso
- Implementación de Productores
- Implementación de Consumidores 