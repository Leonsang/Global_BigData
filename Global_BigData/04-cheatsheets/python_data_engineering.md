    # TRANSFORM
    print("Transformando datos...")
    df_clean = limpiar_datos(df)
    df_agregado = df_clean.groupby(['categoria', 'region']).agg({
        'ventas': 'sum',
        'cantidad': 'sum'
    }).reset_index()
    
    # LOAD
    print(f"Cargando resultados a {archivo_salida}")
    df_agregado.to_csv(archivo_salida, index=False)
    
    return df_agregado

# Uso
resultado = etl_pipeline("datos_raw.csv", "datos_procesados.csv")
```

### **Validación y Logging**
```python
import logging
from datetime import datetime

def setup_logging(nombre_job):
    """Configura logging para el job"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = f"logs/{nombre_job}_{timestamp}.log"
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(nombre_job)

def job_con_validacion(df, nombre_job="data_processing"):
    """Job con validación y logging completo"""
    logger = setup_logging(nombre_job)
    
    try:
        logger.info(f"Iniciando job {nombre_job}")
        logger.info(f"Dataset inicial: {df.shape[0]} filas, {df.shape[1]} columnas")
        
        # Validaciones
        if df.empty:
            raise ValueError("DataFrame vacío")
        
        # Procesamiento
        resultado = procesar_datos(df)
        
        logger.info(f"Job completado exitosamente")
        logger.info(f"Dataset final: {resultado.shape[0]} filas")
        
        return resultado
        
    except Exception as e:
        logger.error(f"Error en job {nombre_job}: {str(e)}")
        raise
```

---

## 🔗 **INTEGRACIÓN CON SPARK**

### **Convertir entre Pandas y Spark**
```python
# Pandas → Spark
spark_df = spark.createDataFrame(pandas_df)

# Spark → Pandas (CUIDADO: solo para DataFrames pequeños)
pandas_df = spark_df.toPandas()

# Muestra de Spark → Pandas para exploración
sample_df = spark_df.sample(0.1).toPandas()
```

### **UDFs (User Defined Functions)**
```python
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType, FloatType

# Función Python simple
def categorizar_precio(precio):
    if precio > 100:
        return "Premium"
    elif precio > 50:
        return "Medio"
    else:
        return "Básico"

# Convertir a UDF
categorizar_udf = udf(categorizar_precio, StringType())

# Usar en Spark DataFrame
df_spark = df_spark.withColumn("categoria_precio", 
                               categorizar_udf(col("precio")))
```

---

## 📋 **CHECKLIST DE COMPETENCIAS PYTHON**

### **Básico** ✅
- [ ] Leo y escribo archivos CSV, JSON, Excel
- [ ] Uso pandas para exploración básica
- [ ] Manejo fechas y tiempo
- [ ] Creo funciones simples de limpieza

### **Intermedio** ✅
- [ ] Conecto a bases de datos (MongoDB, SQL)
- [ ] Hago requests a APIs
- [ ] Uso list/dict comprehensions
- [ ] Manejo errores con try-except

### **Avanzado** ✅
- [ ] Creo pipelines ETL completos
- [ ] Integro Python con Spark (UDFs)
- [ ] Optimizo performance con chunks
- [ ] Implemento logging y monitoreo

---

## 🚨 **ERRORES COMUNES Y SOLUCIONES**

### **MemoryError con Pandas**
```python
# ❌ Cargar todo en memoria
df = pd.read_csv("archivo_10gb.csv")

# ✅ Usar chunks
def procesar_en_chunks(archivo):
    resultado = []
    for chunk in pd.read_csv(archivo, chunksize=10000):
        chunk_procesado = chunk.groupby('categoria').sum()
        resultado.append(chunk_procesado)
    return pd.concat(resultado).groupby(level=0).sum()
```

### **Encodings Problems**
```python
# ❌ Sin especificar encoding
df = pd.read_csv("archivo.csv")

# ✅ Con encoding correcto
df = pd.read_csv("archivo.csv", encoding="utf-8")
# o si falla, probar:
df = pd.read_csv("archivo.csv", encoding="latin1")
```

### **Performance Lento con Loops**
```python
# ❌ Loop para transformar datos
for i, row in df.iterrows():
    df.at[i, 'nueva_col'] = row['col1'] * 2

# ✅ Operación vectorizada
df['nueva_col'] = df['col1'] * 2
```

### **Fechas no se Reconocen**
```python
# ❌ Formato de fecha raro
df['fecha'] = pd.to_datetime(df['fecha_str'])

# ✅ Especificar formato
df['fecha'] = pd.to_datetime(df['fecha_str'], format="%d/%m/%Y")
# o si varía:
df['fecha'] = pd.to_datetime(df['fecha_str'], infer_datetime_format=True)
```

---

## 🎯 **EJERCICIO INTEGRADOR**

```python
"""
Ejercicio: Procesar datos de transporte usando todo lo aprendido
"""
import pandas as pd
import numpy as np
from datetime import datetime
import logging

def analisis_transporte_completo():
    logger = setup_logging("analisis_transporte")
    
    try:
        # 1. EXTRACT - Cargar datos
        logger.info("Cargando datos de transporte...")
        df = pd.read_csv("datos/viajes_transporte.csv")
        logger.info(f"Datos cargados: {df.shape}")
        
        # 2. VALIDATE - Validar estructura
        columnas_requeridas = ['fecha', 'tipo_vehiculo', 'distancia', 'precio']
        validar_dataframe(df, columnas_requeridas)
        
        # 3. TRANSFORM - Limpiar y transformar
        logger.info("Limpiando datos...")
        df['fecha'] = pd.to_datetime(df['fecha'])
        df['año'] = df['fecha'].dt.year
        df['mes'] = df['fecha'].dt.month
        df['dia_semana'] = df['fecha'].dt.day_name()
        
        # Filtrar datos válidos
        df_clean = df[
            (df['distancia'] > 0) & 
            (df['precio'] > 0) & 
            (df['fecha'] >= datetime(2024, 1, 1))
        ].copy()
        
        # 4. ANALYZE - Crear análisis
        logger.info("Generando análisis...")
        
        # Análisis por tipo de vehículo
        analisis_vehiculo = df_clean.groupby('tipo_vehiculo').agg({
            'distancia': ['mean', 'sum'],
            'precio': ['mean', 'sum'],
            'fecha': 'count'
        }).round(2)
        
        # Análisis temporal
        analisis_temporal = df_clean.groupby(['año', 'mes']).agg({
            'precio': 'sum',
            'distancia': 'sum'
        }).reset_index()
        
        # Top rutas
        df_clean['precio_por_km'] = df_clean['precio'] / df_clean['distancia']
        top_rutas = df_clean.nlargest(10, 'precio_por_km')[
            ['tipo_vehiculo', 'distancia', 'precio', 'precio_por_km']
        ]
        
        # 5. LOAD - Guardar resultados
        logger.info("Guardando resultados...")
        analisis_vehiculo.to_csv("resultados/analisis_por_vehiculo.csv")
        analisis_temporal.to_csv("resultados/analisis_temporal.csv")
        top_rutas.to_csv("resultados/top_rutas.csv", index=False)
        
        # 6. REPORT - Generar reporte
        logger.info("=== RESUMEN EJECUTIVO ===")
        logger.info(f"Total viajes procesados: {len(df_clean):,}")
        logger.info(f"Ingresos totales: ${df_clean['precio'].sum():,.2f}")
        logger.info(f"Distancia total: {df_clean['distancia'].sum():,.2f} km")
        logger.info(f"Precio promedio por km: ${df_clean['precio_por_km'].mean():.2f}")
        
        return {
            'analisis_vehiculo': analisis_vehiculo,
            'analisis_temporal': analisis_temporal,
            'top_rutas': top_rutas,
            'metricas': {
                'total_viajes': len(df_clean),
                'ingresos_totales': df_clean['precio'].sum(),
                'distancia_total': df_clean['distancia'].sum()
            }
        }
        
    except Exception as e:
        logger.error(f"Error en análisis: {e}")
        raise

# Ejecutar análisis completo
if __name__ == "__main__":
    resultado = analisis_transporte_completo()
    print("Análisis completado exitosamente!")
```

**💡 Este cheatsheet cubre el 90% de lo que necesitarás para Data Engineering con Python. ¡Practícalo con datos reales!**
