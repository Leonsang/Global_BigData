# 🔥 Sesión 3: Spark RDDs y DataFrames

## 📚 Objetivos de la Sesión
- Comprender los fundamentos de Apache Spark
- Dominar el concepto de RDDs
- Implementar transformaciones y acciones
- Trabajar con DataFrames en Spark

## 🎯 Contenido

### 1. Introducción a Apache Spark
- ¿Qué es Spark?
- Ventajas sobre MapReduce
- Componentes principales
- Casos de uso

### 2. Resilient Distributed Datasets (RDDs)
- Concepto de RDD
- Características principales
- Creación de RDDs
- Persistencia y caching

### 3. Transformaciones y Acciones
- Transformaciones básicas
- Transformaciones avanzadas
- Acciones comunes
- Lazy evaluation

### 4. DataFrames en Spark
- Introducción a DataFrames
- Creación y manipulación
- Operaciones básicas
- Optimización con Catalyst

## 🛠️ Hands-on

### Ejercicio 1: Creación de RDDs
```python
from pyspark import SparkContext

sc = SparkContext("local", "RDD Example")
# Crear RDD desde lista
data = [1, 2, 3, 4, 5]
rdd = sc.parallelize(data)

# Crear RDD desde archivo
text_rdd = sc.textFile("hdfs:///input/data.txt")
```

### Ejercicio 2: Transformaciones y Acciones
```python
# Transformaciones
filtered_rdd = rdd.filter(lambda x: x > 2)
mapped_rdd = rdd.map(lambda x: x * 2)

# Acciones
sum_result = rdd.sum()
count_result = rdd.count()
```

### Ejercicio 3: DataFrames
```python
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("DataFrame Example").getOrCreate()

# Crear DataFrame
df = spark.createDataFrame([
    (1, "Alice", 25),
    (2, "Bob", 30)
], ["id", "name", "age"])

# Operaciones
df.select("name", "age").filter("age > 25").show()
```

## 📊 Entregables
- Notebook con ejemplos de RDDs
- Implementación de transformaciones
- Análisis de datos con DataFrames

## 🔍 Recursos Adicionales
- [Spark Programming Guide](https://spark.apache.org/docs/latest/rdd-programming-guide.html)
- [Spark SQL Guide](https://spark.apache.org/docs/latest/sql-programming-guide.html)
- [Spark Performance Tuning](https://spark.apache.org/docs/latest/tuning.html)

## 🎯 Próxima Sesión
- Spark SQL
- Spark MLlib
- Análisis Avanzado
- Optimización de Queries 