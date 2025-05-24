# ⚡ SPARK & PYSPARK ESSENTIALS CHEATSHEET
## Lo que SÍ vas a usar todos los días (80% del tiempo)

---

## 🚀 **INICIALIZACIÓN BÁSICA**

### **Setup Spark Session**
```python
from pyspark.sql import SparkSession

# Crear Spark Session (SIEMPRE primero)
spark = SparkSession.builder \
    .appName("MiProyecto") \
    .master("spark://spark-master:7077") \
    .config("spark.executor.memory", "2g") \
    .config("spark.executor.cores", "2") \
    .getOrCreate()

# Para uso local sin cluster
spark = SparkSession.builder \
    .appName("Local") \
    .master("local[*]") \
    .getOrCreate()
```

### **Verificar que Todo Funciona**
```python
# Test básico
spark.version
spark.sparkContext.getConf().getAll()

# Test con datos
df = spark.range(1000)
df.count()  # Debería devolver 1000
```

---

## 📁 **LECTURA DE DATOS**

### **Desde HDFS**
```python
# CSV desde HDFS
df = spark.read \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .csv("hdfs://namenode:9000/mi_proyecto/raw/datos.csv")

# Parquet (formato optimizado)
df = spark.read.parquet("hdfs://namenode:9000/mi_proyecto/parquet/")

# JSON
df = spark.read.json("hdfs://namenode:9000/mi_proyecto/json/")
```

### **Desde Archivos Locales**
```python
# CSV local
df = spark.read \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .csv("file:///opt/spark-data/datos.csv")

# Múltiples archivos
df = spark.read \
    .option("header", "true") \
    .csv("hdfs://namenode:9000/mi_proyecto/raw/*.csv")
```

### **Desde Bases de Datos**
```python
# PostgreSQL/MySQL
df = spark.read \
    .format("jdbc") \
    .option("url", "jdbc:postgresql://localhost:5432/midb") \
    .option("dbtable", "transacciones") \
    .option("user", "usuario") \
    .option("password", "password") \
    .load()
```

---

## 🔍 **EXPLORACIÓN BÁSICA**

### **Información General**
```python
# Ver estructura
df.printSchema()
df.columns
df.count()
df.describe().show()

# Primeras filas
df.show(10)
df.head(5)

# Tipos de datos
df.dtypes
```

### **Estadísticas Rápidas**
```python
# Resumen estadístico
df.describe("columna_numerica").show()

# Valores únicos
df.select("categoria").distinct().count()

# Valores nulos
df.filter(df.columna.isNull()).count()

# Distribución de valores
df.groupBy("categoria").count().show()
```

---

## 🛠️ **TRANSFORMACIONES ESENCIALES**

### **Seleccionar y Filtrar**
```python
# Seleccionar columnas
df.select("columna1", "columna2").show()

# Filtrar filas
df.filter(df.edad > 25).show()
df.filter("edad > 25 AND salario < 50000").show()

# Renombrar columnas
df.withColumnRenamed("old_name", "new_name")

# Agregar nueva columna
from pyspark.sql.functions import col, lit
df.withColumn("nueva_col", col("col1") + col("col2"))
df.withColumn("constante", lit("valor_fijo"))
```

### **Agregaciones Básicas**
```python
from pyspark.sql.functions import sum, avg, max, min, count

# Group by simple
df.groupBy("categoria") \
  .agg(sum("ventas").alias("total_ventas"),
       avg("precio").alias("precio_promedio")) \
  .show()

# Múltiples agregaciones
df.groupBy("region", "categoria") \
  .agg(count("*").alias("total_registros"),
       max("fecha").alias("ultima_fecha")) \
  .show()
```

### **Joins**
```python
# Inner join (más común)
resultado = df1.join(df2, df1.id == df2.customer_id, "inner")

# Left join
resultado = df1.join(df2, "id", "left")

# Join con múltiples condiciones
resultado = df1.join(df2, 
    (df1.id == df2.customer_id) & (df1.fecha == df2.fecha))
```

---

## 🕐 **FUNCIONES DE TIEMPO**

```python
from pyspark.sql.functions import year, month, dayofweek, date_format

# Extraer componentes de fecha
df.withColumn("año", year("fecha")) \
  .withColumn("mes", month("fecha")) \
  .withColumn("dia_semana", dayofweek("fecha")) \
  .show()

# Formatear fechas
df.withColumn("fecha_formato", 
    date_format("timestamp", "yyyy-MM-dd HH:mm:ss")).show()
```

---

## 💾 **GUARDAR RESULTADOS**

### **A HDFS**
```python
# Parquet (recomendado para Big Data)
df.write \
  .mode("overwrite") \
  .parquet("hdfs://namenode:9000/mi_proyecto/procesados/resultado")

# CSV
df.coalesce(1) \
  .write \
  .mode("overwrite") \
  .option("header", "true") \
  .csv("hdfs://namenode:9000/mi_proyecto/resultados/")

# Particionado por columna (para archivos grandes)
df.write \
  .mode("overwrite") \
  .partitionBy("año", "mes") \
  .parquet("hdfs://namenode:9000/mi_proyecto/particionado/")
```

---

## 🎯 **SQL EN SPARK**

```python
# Crear vista temporal
df.createOrReplaceTempView("ventas")

# Ejecutar SQL
resultado = spark.sql("""
    SELECT categoria,
           SUM(monto) as total_ventas,
           AVG(precio) as precio_promedio
    FROM ventas 
    WHERE fecha >= '2024-01-01'
    GROUP BY categoria
    ORDER BY total_ventas DESC
""")

resultado.show()
```

---

## ⚡ **OPTIMIZACIÓN PERFORMANCE**

### **Caching**
```python
# Cache para reutilizar DataFrame
df.cache()
df.persist()

# Verificar cache
spark.catalog.isCached("nombre_tabla")

# Limpiar cache
df.unpersist()
spark.catalog.clearCache()
```

### **Partitioning**
```python
# Repartir para balance
df.repartition(10)

# Repartir por columna (para joins)
df.repartition("id")

# Coalescer para reducir archivos
df.coalesce(1)
```

### **Broadcast para Joins**
```python
from pyspark.sql.functions import broadcast

# Para tablas pequeñas (<200MB)
resultado = df_grande.join(
    broadcast(df_pequeño), "id"
)
```

---

## 🐛 **DEBUGGING & TROUBLESHOOTING**

### **Ver Plan de Ejecución**
```python
# Ver qué va a hacer Spark
df.explain()
df.explain(True)  # Más detallado

# Ejecutar y ver métricas
df.show()
print(f"Particiones: {df.rdd.getNumPartitions()}")
```

### **Sampling para Tests**
```python
# Muestra pequeña para testing
df_sample = df.sample(0.1)  # 10% de los datos
df_small = df.limit(1000)   # Primeros 1000 registros
```

### **Manejo de Errores**
```python
try:
    resultado = df.collect()
except Exception as e:
    print(f"Error: {e}")
    
# Ver errores en logs
spark.sparkContext.setLogLevel("WARN")
```

---

## 📊 **WINDOW FUNCTIONS**

```python
from pyspark.sql.window import Window
from pyspark.sql.functions import row_number, rank, lag

# Ranking dentro de grupos
window = Window.partitionBy("categoria").orderBy(col("ventas").desc())

df.withColumn("ranking", row_number().over(window)) \
  .show()

# Comparación con valor anterior
window_tiempo = Window.partitionBy("producto").orderBy("fecha")
df.withColumn("ventas_anterior", lag("ventas").over(window_tiempo)) \
  .show()
```

---

## 🔄 **PATRONES COMUNES DE ETL**

### **Limpieza de Datos**
```python
# Eliminar nulls
df_clean = df.filter(df.columna.isNotNull())

# Reemplazar valores
df_clean = df.fillna({"columna_str": "Sin datos", "columna_num": 0})

# Eliminar duplicados
df_unique = df.dropDuplicates(["id"])
```

### **Transformación de Columnas**
```python
from pyspark.sql.functions import when, regexp_replace, upper

# Condicionales
df.withColumn("categoria_nueva", 
    when(col("precio") > 100, "Premium")
    .when(col("precio") > 50, "Medio")
    .otherwise("Básico")
).show()

# Limpiar texto
df.withColumn("nombre_limpio", 
    regexp_replace(upper(col("nombre")), "[^A-Z0-9]", "")
).show()
```

---

## 🎪 **EJEMPLO COMPLETO DE SESIÓN**

```python
# 1. Inicializar
from pyspark.sql import SparkSession
from pyspark.sql.functions import *

spark = SparkSession.builder \
    .appName("AnalisisTransporte") \
    .getOrCreate()

# 2. Cargar datos
df = spark.read \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .csv("hdfs://namenode:9000/transporte/raw/viajes.csv")

# 3. Explorar
print(f"Total registros: {df.count()}")
df.printSchema()
df.show(5)

# 4. Limpiar
df_clean = df.filter(df.distancia > 0) \
            .filter(df.precio.isNotNull())

# 5. Analizar
resultado = df_clean.groupBy("tipo_vehiculo") \
    .agg(
        avg("distancia").alias("distancia_promedio"),
        sum("precio").alias("ingresos_totales"),
        count("*").alias("total_viajes")
    ) \
    .orderBy(desc("ingresos_totales"))

# 6. Mostrar resultados
resultado.show()

# 7. Guardar
resultado.write \
    .mode("overwrite") \
    .parquet("hdfs://namenode:9000/transporte/procesados/analisis_vehiculos")

# 8. Limpiar
spark.stop()
```

---

## 🚨 **ERRORES COMUNES Y SOLUCIONES**

### **Error: "Master URL not set"**
```python
# ❌ Falta master
spark = SparkSession.builder.appName("test").getOrCreate()

# ✅ Con master
spark = SparkSession.builder \
    .appName("test") \
    .master("spark://spark-master:7077") \
    .getOrCreate()
```

### **Error: "File not found"**
```python
# ❌ Path incorrecto
df = spark.read.csv("/mi_archivo.csv")

# ✅ Path completo HDFS
df = spark.read.csv("hdfs://namenode:9000/mi_proyecto/mi_archivo.csv")
```

### **Error: "Out of memory"**
```python
# ❌ Cache de todo
df.cache()
df.collect()  # Trae todo a driver

# ✅ Solo cache lo necesario + sample
df.sample(0.1).cache()
df.show(20)  # No usar collect()
```

### **Performance Lento**
```python
# ❌ Sin partitioning
df.groupBy("categoria").count().show()

# ✅ Con repartitioning
df.repartition("categoria") \
  .groupBy("categoria") \
  .count() \
  .show()
```

---

## 🎯 **CHECKLIST DE COMPETENCIAS**

### **Básico** ✅
- [ ] Puedo iniciar Spark Session
- [ ] Leo archivos CSV y Parquet
- [ ] Uso select, filter, groupBy
- [ ] Guardo resultados en HDFS

### **Intermedio** ✅
- [ ] Optimizo con cache y repartition
- [ ] Uso joins entre DataFrames
- [ ] Aplico window functions
- [ ] Manejo errores comunes

### **Avanzado** ✅
- [ ] Entiendo explain() plans
- [ ] Resuelvo data skew
- [ ] Uso broadcast joins
- [ ] Optimizo para production

**💡 Tip Final: Siempre inicia con muestra pequeña (sample/limit), luego escala a datos completos!**
