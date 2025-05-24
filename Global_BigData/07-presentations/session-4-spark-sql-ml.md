# 📊 Sesión 4: Spark SQL y MLlib

## 📚 Objetivos de la Sesión
- Dominar Spark SQL para análisis de datos
- Implementar consultas SQL en Spark
- Aplicar algoritmos de MLlib
- Optimizar consultas y modelos

## 🎯 Contenido

### 1. Spark SQL
- Introducción a Spark SQL
- Creación de vistas temporales
- Consultas SQL
- Optimización de queries

### 2. API Estructurada
- Lectura de datos
- Escritura de datos
- Manipulación de DataFrames
- Joins y agregaciones

### 3. Spark MLlib
- Introducción a MLlib
- Pipeline de ML
- Algoritmos supervisados
- Algoritmos no supervisados

### 4. Optimización
- Tuning de queries
- Caching y persistencia
- Particionamiento
- Best practices

## 🛠️ Hands-on

### Ejercicio 1: Spark SQL
```python
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("SQL Example").getOrCreate()

# Crear vista temporal
df.createOrReplaceTempView("people")

# Consulta SQL
result = spark.sql("""
    SELECT name, AVG(age) as avg_age
    FROM people
    GROUP BY name
    HAVING avg_age > 25
""")
```

### Ejercicio 2: API Estructurada
```python
# Lectura de datos
df = spark.read.format("csv") \
    .option("header", "true") \
    .load("hdfs:///input/data.csv")

# Manipulación
df_transformed = df \
    .select("name", "age") \
    .filter("age > 25") \
    .groupBy("name") \
    .agg({"age": "avg"})
```

### Ejercicio 3: MLlib
```python
from pyspark.ml import Pipeline
from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml.feature import VectorAssembler

# Preparar datos
assembler = VectorAssembler(
    inputCols=["feature1", "feature2"],
    outputCol="features"
)

# Crear modelo
rf = RandomForestClassifier(
    labelCol="label",
    featuresCol="features"
)

# Pipeline
pipeline = Pipeline(stages=[assembler, rf])
model = pipeline.fit(training_data)
```

## 📊 Entregables
- Notebook de análisis SQL
- Pipeline de ML implementado
- Reporte de optimización

## 🔍 Recursos Adicionales
- [Spark SQL Guide](https://spark.apache.org/docs/latest/sql-programming-guide.html)
- [MLlib Guide](https://spark.apache.org/docs/latest/ml-guide.html)
- [Spark Performance Tuning](https://spark.apache.org/docs/latest/tuning.html)

## 🎯 Próxima Sesión
- Spark Structured Streaming
- Procesamiento en Tiempo Real
- Windowing y Agregaciones
- Integración con Fuentes de Datos 