# ⚡ Sesión 2: MapReduce - Divide y Vencerás

## 📚 Objetivos de la Sesión
- Implementar jobs MapReduce de producción
- Optimizar el rendimiento de procesamiento
- Comparar MapReduce vs Spark
- Realizar troubleshooting distribuido

## 🎯 Contenido

### 1. Fundamentos de MapReduce
- Paradigma de programación
- Fases Map y Reduce
- Shuffle y Sort
- Combiner y Partitioner

### 2. Desarrollo de Jobs
- Estructura de un job
- Mappers y Reducers
- Configuración de jobs
- Testing y debugging

### 3. Optimización
- Tuning de memoria
- Configuración de slots
- Compresión de datos
- Combiners y Partitioners

### 4. Spark vs MapReduce
- Comparativa de rendimiento
- Casos de uso
- Migración de jobs
- Decisiones arquitectónicas

## 🛠️ Hands-on

### Ejercicio 1: Job Básico
```python
# WordCount en MapReduce
from mrjob.job import MRJob

class MRWordCount(MRJob):
    def mapper(self, _, line):
        for word in line.split():
            yield (word, 1)

    def reducer(self, word, counts):
        yield (word, sum(counts))

if __name__ == '__main__':
    MRWordCount.run()
```

### Ejercicio 2: Optimización
```bash
# Ejecutar job optimizado
hadoop jar hadoop-streaming.jar \
  -D mapreduce.job.reduces=10 \
  -D mapreduce.map.memory.mb=2048 \
  -files mapper.py,reducer.py \
  -mapper mapper.py \
  -reducer reducer.py \
  -input /input \
  -output /output
```

### Ejercicio 3: Comparativa
```python
# Mismo job en Spark
from pyspark import SparkContext

sc = SparkContext()
text_file = sc.textFile("hdfs:///input")
counts = text_file.flatMap(lambda line: line.split()) \
                  .map(lambda word: (word, 1)) \
                  .reduceByKey(lambda a, b: a + b)
counts.saveAsTextFile("hdfs:///output")
```

## 📊 Entregables
- Pipeline de análisis de transporte
- Reporte de optimización
- Comparativa tecnológica

## 🔍 Recursos Adicionales
- [MapReduce Tutorial](https://hadoop.apache.org/docs/current/hadoop-mapreduce-client/hadoop-mapreduce-client-core/MapReduceTutorial.html)
- [Spark Programming Guide](https://spark.apache.org/docs/latest/rdd-programming-guide.html)
- [Performance Tuning](https://hadoop.apache.org/docs/current/hadoop-mapreduce-client/hadoop-mapreduce-client-core/mapred-default.xml)

## 🎯 Próxima Sesión
- Kafka: Procesamiento en Tiempo Real
- Stream Processing
- Event Sourcing
- Arquitecturas Lambda 