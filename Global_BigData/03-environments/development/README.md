# 🚀 Entorno de Desarrollo Big Data

## Descripción
Este es el entorno completo de desarrollo para el proyecto Big Data Transport Analysis. Incluye todos los servicios necesarios para desarrollo y pruebas.

## Servicios Disponibles

### HDFS (Hadoop Distributed File System)
- **NameNode UI**: http://localhost:9870
- **API**: hdfs://namenode:9000
- **Configuración**: 
  - Replicación: 2
  - Block Size: 128MB
  - Permisos: Desactivados para desarrollo

### Spark Cluster
- **Master UI**: http://localhost:8080
- **Workers**: 2 instancias
- **Configuración**:
  - Worker Cores: 2 por worker
  - Worker Memory: 2GB por worker
  - Adaptive Query Execution: Activado

### Jupyter Lab
- **URL**: http://localhost:8888
- **Volúmenes Montados**:
  - `/home/jovyan/sessions`: Sesiones de trabajo
  - `/home/jovyan/datasets`: Datos del proyecto
  - `/home/jovyan/cheatsheets`: Referencias rápidas
  - `/home/jovyan/solutions`: Soluciones a ejercicios

### Kafka
- **Broker**: localhost:9092
- **Zookeeper**: localhost:2181
- **Configuración**:
  - Partitions: 3
  - Replication Factor: 1 (desarrollo)

## Uso

### 1. Iniciar el Entorno
```bash
docker-compose up -d
```

### 2. Verificar Servicios
```bash
docker-compose ps
```

### 3. Acceder a las Interfaces
- Jupyter Lab: http://localhost:8888
- Spark UI: http://localhost:8080
- HDFS UI: http://localhost:9870

### 4. Detener el Entorno
```bash
docker-compose down
```

## Estructura de Directorios
```
development/
├── docker-compose.yml    # Configuración principal
├── hadoop.env           # Variables de entorno Hadoop
└── README.md           # Este archivo
```

## Comandos Útiles

### HDFS
```bash
# Listar archivos
hdfs dfs -ls /

# Subir archivo
hdfs dfs -put archivo.csv /datos/

# Ver contenido
hdfs dfs -cat /datos/archivo.csv
```

### Spark
```bash
# Iniciar PySpark
pyspark --master spark://spark-master:7077

# Ejecutar script
spark-submit --master spark://spark-master:7077 script.py
```

### Kafka
```bash
# Listar topics
kafka-topics.sh --list --bootstrap-server localhost:9092

# Crear topic
kafka-topics.sh --create --topic test --bootstrap-server localhost:9092
```

## Solución de Problemas

### HDFS
- Si el NameNode no inicia, verifica los logs:
  ```bash
  docker logs hdfs_namenode
  ```
- Para problemas de permisos:
  ```bash
  hdfs dfs -chmod 755 /directorio
  ```

### Spark
- Si los workers no conectan:
  ```bash
  docker logs spark_worker_1
  ```
- Para problemas de memoria:
  ```bash
  # Ajustar en docker-compose.yml
  SPARK_WORKER_MEMORY=4g
  ```

### Kafka
- Si el broker no inicia:
  ```bash
  docker logs kafka_broker_1
  ```
- Para problemas de conexión:
  ```bash
  kafka-topics.sh --describe --topic test
  ```

## Notas de Desarrollo

1. **Persistencia de Datos**:
   - Los datos de HDFS se almacenan en volúmenes Docker
   - Los notebooks se guardan en `01-sessions/`
   - Los datasets se encuentran en `02-datasets/`

2. **Rendimiento**:
   - Ajusta la memoria de los workers según tu sistema
   - Considera aumentar el número de workers para procesamiento pesado
   - Monitorea el uso de recursos en las UIs

3. **Desarrollo**:
   - Usa Jupyter Lab para desarrollo interactivo
   - Mantén los notebooks organizados por sesión
   - Documenta tus soluciones en `06-solutions/`

## Próximos Pasos

1. Familiarízate con las interfaces web
2. Explora los datasets disponibles
3. Revisa los notebooks de ejemplo
4. Comienza con los ejercicios de la sesión actual 