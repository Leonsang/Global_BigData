# 🐳 DOCKER & DOCKER COMPOSE CHEATSHEET
## Todo lo que necesitas para Big Data (enfoque práctico)

---

## 🎯 **CONCEPTOS CLAVE (en 30 segundos)**

- **Container**: Aplicación empacada con todo lo que necesita
- **Image**: Template para crear containers
- **Docker Compose**: Orquestador para múltiples containers
- **Volume**: Persistir datos entre reinicios
- **Network**: Comunicación entre containers

---

## 🚀 **COMANDOS ESENCIALES DOCKER**

### **Información y Estado**
```bash
# Ver versión
docker --version
docker-compose --version

# Ver containers corriendo
docker ps

# Ver TODOS los containers (incluso parados)
docker ps -a

# Ver imágenes descargadas
docker images

# Información del sistema
docker system df
docker system info
```

### **Gestión de Containers**
```bash
# Iniciar container
docker run -d --name mi_container nginx

# Parar container
docker stop mi_container

# Reiniciar container
docker restart mi_container

# Eliminar container
docker rm mi_container

# Eliminar container forzado (si está corriendo)
docker rm -f mi_container

# Ver logs
docker logs mi_container
docker logs -f mi_container  # Seguir logs en tiempo real
```

### **Gestión de Imágenes**
```bash
# Descargar imagen
docker pull ubuntu:20.04

# Construir imagen desde Dockerfile
docker build -t mi_app:1.0 .

# Eliminar imagen
docker rmi mi_app:1.0

# Limpiar imágenes sin usar
docker image prune
```

---

## 🏗️ **DOCKER COMPOSE PARA BIG DATA**

### **Comandos Básicos**
```bash
# Iniciar todo el stack (modo detached)
docker-compose up -d

# Ver estado de servicios
docker-compose ps

# Ver logs de todos los servicios
docker-compose logs

# Ver logs de un servicio específico
docker-compose logs namenode
docker-compose logs spark-master

# Parar todo
docker-compose down

# Parar y eliminar volúmenes (¡CUIDADO! Pierdes datos)
docker-compose down -v

# Reiniciar un servicio específico
docker-compose restart namenode

# Reconstruir servicios
docker-compose up -d --build
```

### **Escalado y Gestión**
```bash
# Escalar un servicio (ej: más workers)
docker-compose up -d --scale spark-worker=3

# Ejecutar comando en servicio corriendo
docker-compose exec namenode bash
docker-compose exec spark-master /opt/spark/bin/pyspark

# Ver uso de recursos
docker stats
```

---

## 📋 **DOCKER-COMPOSE.YML EXPLICADO**

### **Estructura Básica para Big Data**
```yaml
version: '3.8'

services:
  # ===== HADOOP ECOSYSTEM =====
  namenode:
    image: bde2020/hadoop-namenode:2.0.0-hadoop3.2.1-java8
    container_name: namenode
    restart: always                    # Reinicio automático
    ports:
      - "9870:9870"                    # Puerto para Web UI
      - "9000:9000"                    # Puerto para HDFS
    volumes:
      - hadoop_namenode:/hadoop/dfs/name  # Persistir metadatos
    environment:
      - CLUSTER_NAME=bigdata-cluster
      - CORE_CONF_fs_defaultFS=hdfs://namenode:9000
    networks:
      - bigdata                        # Red interna

  datanode1:
    image: bde2020/hadoop-datanode:2.0.0-hadoop3.2.1-java8
    container_name: datanode1
    restart: always
    volumes:
      - hadoop_datanode1:/hadoop/dfs/data  # Persistir datos
    environment:
      SERVICE_PRECONDITION: "namenode:9870"  # Esperar a namenode
      CORE_CONF_fs_defaultFS: hdfs://namenode:9000
    depends_on:
      - namenode                       # Orden de inicio
    networks:
      - bigdata

# ===== VOLÚMENES PERSISTENTES =====
volumes:
  hadoop_namenode:
  hadoop_datanode1:
  hadoop_datanode2:

# ===== RED INTERNA =====
networks:
  bigdata:
    driver: bridge
```

### **Explicación de Secciones Clave**

**Ports:**
```yaml
ports:
  - "9870:9870"  # host_port:container_port
```
- Puerto 9870 del container se mapea al 9870 de tu máquina
- Accedes via: http://localhost:9870

**Volumes:**
```yaml
volumes:
  - hadoop_namenode:/hadoop/dfs/name  # named_volume:container_path
  - ./data:/opt/spark-data            # host_path:container_path
```
- Named volumes: gestionados por Docker, persisten datos
- Bind mounts: carpeta de tu máquina mapeada al container

**Environment:**
```yaml
environment:
  - CLUSTER_NAME=bigdata-cluster      # Variable de entorno
  - CORE_CONF_fs_defaultFS=hdfs://namenode:9000
```

**Networks:**
```yaml
networks:
  - bigdata  # Containers en misma red pueden comunicarse por nombre
```

---

## 🔧 **CONFIGURACIÓN ESPECÍFICA PARA CADA SERVICIO**

### **Hadoop NameNode**
```yaml
namenode:
  image: bde2020/hadoop-namenode:2.0.0-hadoop3.2.1-java8
  ports:
    - "9870:9870"    # Web UI
    - "9000:9000"    # HDFS API
  environment:
    - CLUSTER_NAME=bigdata-cluster
    - CORE_CONF_fs_defaultFS=hdfs://namenode:9000
```
**Acceso:** http://localhost:9870

### **Spark Master**
```yaml
spark-master:
  image: bde2020/spark-master:3.1.1-hadoop3.2
  ports:
    - "8080:8080"    # Web UI
    - "7077:7077"    # Spark API
  environment:
    - CORE_CONF_fs_defaultFS=hdfs://namenode:9000
  volumes:
    - ./data:/opt/spark-data          # Datos compartidos
    - ./notebooks:/opt/spark-notebooks # Notebooks
```
**Acceso:** http://localhost:8080

### **Jupyter con PySpark**
```yaml
jupyter-spark:
  image: jupyter/pyspark-notebook:spark-3.1.1
  ports:
    - "8888:8888"
  environment:
    - JUPYTER_ENABLE_LAB=yes
    - SPARK_MASTER=spark://spark-master:7077
  volumes:
    - ./notebooks:/home/jovyan/work
    - ./data:/home/jovyan/data
  command: start-notebook.sh --NotebookApp.token='' --NotebookApp.password=''
```
**Acceso:** http://localhost:8888

### **Kafka Cluster**
```yaml
zookeeper:
  image: confluentinc/cp-zookeeper:7.0.1
  environment:
    ZOOKEEPER_CLIENT_PORT: 2181
    ZOOKEEPER_TICK_TIME: 2000

kafka-1:
  image: confluentinc/cp-kafka:7.0.1
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
```

---

## 📊 **MONITOREO Y DEBUGGING**

### **Verificar que Todo Funciona**
```bash
# 1. Verificar que containers están corriendo
docker-compose ps

# Debería mostrar algo como:
#     Name                 Command               State           Ports
# namenode         /entrypoint.sh /run.sh         Up      0.0.0.0:9000->9000/tcp, 0.0.0.0:9870->9870/tcp
# datanode1        /entrypoint.sh /run.sh         Up      9864/tcp
# spark-master     /bin/bash /master.sh           Up      0.0.0.0:7077->7077/tcp, 0.0.0.0:8080->8080/tcp

# 2. Verificar logs si algo falla
docker-compose logs namenode | tail -20

# 3. Verificar conectividad interna
docker-compose exec namenode ping datanode1
```

### **URLs de Acceso**
```bash
# Web UIs importantes
http://localhost:9870    # Hadoop NameNode
http://localhost:8080    # Spark Master
http://localhost:8888    # Jupyter Lab
http://localhost:3000    # Grafana (si está configurado)
```

### **Debugging Común**
```bash
# Ver logs en tiempo real
docker-compose logs -f namenode

# Entrar al container para debugging
docker-compose exec namenode bash
docker-compose exec spark-master bash

# Ver uso de recursos
docker stats

# Ver redes
docker network ls
docker network inspect $(docker-compose config | grep -A1 networks | tail -1 | cut -d: -f1)
```

---

## 🆘 **TROUBLESHOOTING COMÚN**

### **Error: "Port already in use"**
```bash
# Verificar qué usa el puerto
netstat -tulpn | grep 9870
# o en Windows:
netstat -ano | findstr 9870

# Cambiar puerto en docker-compose.yml
ports:
  - "9871:9870"  # Usar puerto diferente en host
```

### **Error: "Container name already exists"**
```bash
# Limpiar containers existentes
docker-compose down
docker rm $(docker ps -aq)  # Eliminar todos los containers parados

# O forzar recreación
docker-compose up -d --force-recreate
```

### **Error: "No space left on device"**
```bash
# Limpiar sistema Docker
docker system prune -f

# Limpiar volúmenes sin usar
docker volume prune

# Ver uso de espacio
docker system df
```

### **Containers se Paran Inmediatamente**
```bash
# Ver logs para identificar el error
docker-compose logs servicio_que_falla

# Verificar dependencias
docker-compose up namenode    # Iniciar solo namenode primero
docker-compose up datanode1   # Luego datanode
```

### **Performance Lento**
```bash
# Verificar recursos asignados
docker stats

# Ajustar memoria en docker-compose.yml
deploy:
  resources:
    limits:
      memory: 4g
    reservations:
      memory: 2g
```

---

## 🎯 **WORKFLOWS COMUNES**

### **Setup Inicial Completo**
```bash
# 1. Clonar proyecto
git clone [tu_repo]
cd proyecto_bigdata

# 2. Crear directorios necesarios
mkdir -p data logs notebooks

# 3. Iniciar servicios básicos primero
docker-compose up -d zookeeper
sleep 10
docker-compose up -d namenode
sleep 15
docker-compose up -d datanode1 datanode2

# 4. Iniciar el resto
docker-compose up -d

# 5. Verificar
docker-compose ps
```

### **Desarrollo Diario**
```bash
# Iniciar ambiente
docker-compose up -d

# Trabajar en notebooks
# http://localhost:8888

# Ver logs si hay problemas
docker-compose logs -f spark-master

# Al terminar el día
docker-compose stop  # Para servicios pero conserva datos
```

### **Reset Completo (Emergencia)**
```bash
# ⚠️ CUIDADO: Esto borra TODOS los datos
docker-compose down -v
docker system prune -f
docker volume prune -f

# Reiniciar desde cero
docker-compose up -d
```

---

## 📈 **OPTIMIZACIÓN Y BEST PRACTICES**

### **Configuración de Memoria**
```yaml
# En docker-compose.yml para servicios pesados
spark-master:
  deploy:
    resources:
      limits:
        memory: 4g
        cpus: '2'
      reservations:
        memory: 2g
        cpus: '1'
```

### **Variables de Entorno en Archivo**
```bash
# Crear archivo .env
cat << EOF > .env
SPARK_WORKER_MEMORY=2g
SPARK_WORKER_CORES=2
HADOOP_REPLICATION_FACTOR=2
EOF
```

```yaml
# Usar en docker-compose.yml
environment:
  - SPARK_WORKER_MEMORY=${SPARK_WORKER_MEMORY}
  - SPARK_WORKER_CORES=${SPARK_WORKER_CORES}
```

### **Health Checks**
```yaml
namenode:
  healthcheck:
    test: ["CMD", "curl", "-f", "http://localhost:9870"]
    interval: 30s
    timeout: 10s
    retries: 3
    start_period: 40s
```

---

## 🎪 **EJEMPLO COMPLETO DE PROYECTO**

```yaml
# docker-compose.yml optimizado para clases
version: '3.8'

services:
  # HDFS
  namenode:
    image: bde2020/hadoop-namenode:2.0.0-hadoop3.2.1-java8
    container_name: namenode
    restart: unless-stopped
    ports:
      - "9870:9870"
      - "9000:9000"
    volumes:
      - hadoop_namenode:/hadoop/dfs/name
      - ./data:/data
    environment:
      - CLUSTER_NAME=bigdata-clase
      - CORE_CONF_fs_defaultFS=hdfs://namenode:9000
    networks:
      - bigdata

  datanode:
    image: bde2020/hadoop-datanode:2.0.0-hadoop3.2.1-java8
    container_name: datanode
    restart: unless-stopped
    volumes:
      - hadoop_datanode:/hadoop/dfs/data
    environment:
      SERVICE_PRECONDITION: "namenode:9870"
      CORE_CONF_fs_defaultFS: hdfs://namenode:9000
    depends_on:
      - namenode
    networks:
      - bigdata

  # SPARK
  spark-master:
    image: bde2020/spark-master:3.1.1-hadoop3.2
    container_name: spark-master
    ports:
      - "8080:8080"
      - "7077:7077"
    environment:
      - CORE_CONF_fs_defaultFS=hdfs://namenode:9000
    volumes:
      - ./data:/opt/spark-data
      - ./notebooks:/opt/spark-notebooks
    depends_on:
      - namenode
    networks:
      - bigdata

  spark-worker:
    image: bde2020/spark-worker:3.1.1-hadoop3.2
    container_name: spark-worker
    depends_on:
      - spark-master
    ports:
      - "8081:8081"
    environment:
      - SPARK_MASTER=spark://spark-master:7077
      - SPARK_WORKER_CORES=2
      - SPARK_WORKER_MEMORY=2g
    volumes:
      - ./data:/opt/spark-data
    networks:
      - bigdata

  # JUPYTER
  jupyter:
    image: jupyter/pyspark-notebook:spark-3.1.1
    container_name: jupyter
    ports:
      - "8888:8888"
    environment:
      - JUPYTER_ENABLE_LAB=yes
      - SPARK_MASTER=spark://spark-master:7077
    volumes:
      - ./notebooks:/home/jovyan/work
      - ./data:/home/jovyan/data
    command: start-notebook.sh --NotebookApp.token='' --NotebookApp.password=''
    depends_on:
      - spark-master
    networks:
      - bigdata

volumes:
  hadoop_namenode:
  hadoop_datanode:

networks:
  bigdata:
    driver: bridge
```

**💡 Con este setup tienes un ambiente completo de Big Data en menos de 5 minutos!**

---

## 📋 **CHECKLIST DE COMPETENCIAS**

### **Básico** ✅
- [ ] Puedo iniciar/parar el stack completo
- [ ] Accedo a las Web UIs principales
- [ ] Veo logs para debugging
- [ ] Entiendo la estructura del docker-compose.yml

### **Intermedio** ✅
- [ ] Modifico configuraciones de servicios
- [ ] Agrego nuevos volúmenes y variables
- [ ] Escalo servicios (más workers)
- [ ] Troubleshoot problemas comunes

### **Avanzado** ✅
- [ ] Creo mis propios servicios personalizados
- [ ] Optimizo performance y recursos
- [ ] Implemento health checks y monitoring
- [ ] Gestiono múltiples ambientes (dev/prod)

**🎯 ¡Domina Docker Compose y tendrás ambientes reproducibles para cualquier proyecto Big Data!**
