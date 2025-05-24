# 🚀 BIG DATA LEARNING PROJECT - SESIONES 0-6
## Ambiente Realista para Aprendizaje de Tecnologías Big Data

### 🎯 **OBJETIVO**
Proporcionar una experiencia **100% práctica y realista** con tecnologías Big Data, simulando problemas y herramientas de producción para formar ingenieros de datos competentes.

### 🏆 **VALOR DIFERENCIAL**
- ✅ **Cluster distribuido real** (no simulaciones)
- ✅ **Datos realistas** de transporte público  
- ✅ **Problemas de producción** (fallos, optimización, troubleshooting)
- ✅ **Herramientas profesionales** (Docker, HDFS, Spark, Kafka)
- ✅ **Metodología hands-on** (70% práctica, 30% teoría)

---

## 📋 **REQUISITOS MÍNIMOS**

### Hardware
- **RAM**: 16GB (mínimo 12GB)
- **CPU**: 4 cores físicos
- **Almacenamiento**: 50GB libres SSD
- **Red**: Conexión estable a internet

### Software
- **Docker Desktop** 20.10+
- **Docker Compose** 2.0+
- **Git** (para clonar repositorio)
- **VS Code** (recomendado)

---

## 🚀 **SETUP RÁPIDO (5 minutos)**

### 1. **Clonar y Configurar**
```bash
git clone <repository-url>
cd Global_BigData

# Para Windows (PowerShell)
.\00-setup\scripts\setup_bigdata_env.ps1 setup

# Para Linux/Mac (Bash)
chmod +x 00-setup/scripts/setup_bigdata_env.sh
./00-setup/scripts/setup_bigdata_env.sh setup
```

### 2. **Validar Instalación**
```bash
# Ejecutar validador automático
python 00-setup/scripts/validate_environment.py

# O verificar manualmente
docker-compose -f 03-environments/development/docker-compose.yml ps
```

### 3. **Acceder a Servicios**
- **Jupyter Lab**: http://localhost:8888
- **HDFS NameNode**: http://localhost:9870
- **Spark Master**: http://localhost:8080
- **Kafka Manager**: http://localhost:9000
- **Portainer**: http://localhost:9443

---

## 📚 **ESTRUCTURA DEL PROYECTO**

```
Global_BigData/
├── 📁 00-setup/                    # Scripts de configuración
│   ├── scripts/                    # Setup automático
│   └── validation/                 # Tests de validación
├── 📁 01-sessions/                 # Material por sesión
│   ├── [session-0-intro](01-sessions/session-0-intro/README.md)            # Sesión 0: Introducción + Setup
│   ├── [session-1-hdfs](01-sessions/session-1-hdfs/README.md)             # Sesión 1: HDFS Distribuido
│   ├── [session-2-mapreduce](01-sessions/session-2-mapreduce/README.md)        # Sesión 2: MapReduce
│   ├── [session-3-spark-rdd](01-sessions/session-3-spark-rdd/README.md)        # Sesión 3: Spark RDDs y DataFrames
│   ├── [session-4-spark-sql](01-sessions/session-4-spark-sql/README.md)        # Sesión 4: Spark SQL y MLlib
│   ├── [session-5-streaming](01-sessions/session-5-streaming/README.md)        # Sesión 5: Spark Structured Streaming
│   └── [session-6-kafka](01-sessions/session-6-kafka/README.md)            # Sesión 6: Apache Kafka
├── 📁 02-datasets/                 # Datos del proyecto
│   ├── raw/                        # Datos originales
│   ├── generators/                 # Generadores de datos
│   └── schemas/                    # Estructura de datos
├── 📁 03-environments/             # Configuraciones ambiente
│   └── development/                # Docker Compose + configs
├── 📁 04-cheatsheets/              # Referencias rápidas
├── 📁 05-monitoring/               # Herramientas monitoreo
├── 📁 06-solutions/                # Soluciones ejercicios
└── 📁 07-presentations/            # Presentaciones del curso
```

---

## 🎓 **ROADMAP DE SESIONES**

### **📖 SESIÓN 0: INTRODUCCIÓN Y SETUP** *(1.5 horas)*
**Objetivo**: Contexto y ambiente funcionando
- ✅ Introducción a Big Data
- ✅ Sociedad interconectada
- ✅ Setup automático
- ✅ Primer "win" técnico

### **🗂️ SESIÓN 1: HDFS - EL EJÉRCITO DE COMPUTADORAS** *(1.5 horas)*
**Objetivo**: Dominar almacenamiento distribuido
- ⚡ Cluster HDFS multi-nodo
- 📊 Análisis de distribución
- 🔥 Simulación de fallos
- 📈 Optimización

### **⚡ SESIÓN 2: MAPREDUCE - DIVIDE Y VENCERÁS** *(3 horas)*
**Objetivo**: Procesamiento distribuido
- 🧮 Jobs MapReduce
- 🚀 Optimización
- 🆚 Comparativa con Spark
- 🔧 Troubleshooting

### **🔥 SESIÓN 3: SPARK RDDs Y DATAFRAMES** *(2 horas)*
**Objetivo**: Procesamiento con Spark
- 📊 RDDs y transformaciones
- 🎯 DataFrames
- ⚡ Optimización
- 🔄 Persistencia

### **📊 SESIÓN 4: SPARK SQL Y MLlib** *(2 horas)*
**Objetivo**: Análisis y ML
- 🎯 Spark SQL
- 🤖 MLlib
- 📈 Optimización
- 📊 Visualización

### **⚡ SESIÓN 5: SPARK STRUCTURED STREAMING** *(2 horas)*
**Objetivo**: Procesamiento en tiempo real
- 🌊 Structured Streaming
- ⏰ Windowing
- 📊 Agregaciones
- 🔄 Integración Kafka

### **🚀 SESIÓN 6: APACHE KAFKA** *(2 horas)*
**Objetivo**: Event streaming
- 📨 Productores
- 📥 Consumidores
- 🔄 Event sourcing
- 📈 Performance

"aqui yatendremos un proyecto git completo que nos servira de ejemplo para aplicar los conocimientos adquiridos en las sesiones anteriores con ejemplos reales y tareas y proyectos que nos permitiran demostrar la aplicacion de los conocimientos adquiridos en las sesiones anteriores"

---

## 🛠️ **STACK TECNOLÓGICO**

### **Almacenamiento**
- **Hadoop HDFS 3.2.1**: Distributed file system
- **Docker Volumes**: Persistencia de datos

### **Procesamiento**
- **Apache Spark 3.4.0**: Distributed computing
- **Hadoop MapReduce 3.2.1**: Batch processing
- **Apache Kafka 3.4.0**: Event streaming

### **Orquestación**
- **Docker 20.10+**: Containerización
- **Docker Compose**: Multi-container

### **Desarrollo**
- **Jupyter Lab**: IDE interactivo
- **Python 3.9**: Lenguaje principal
- **Pandas/NumPy**: Data manipulation

### **Monitoreo**
- **Portainer**: Container management
- **Hadoop Web UIs**: HDFS monitoring
- **Spark Web UI**: Job monitoring
- **Kafka Manager**: Topic management

---

## 📊 **DATOS DEL PROYECTO**

### **Dataset: Transporte Público de Lima**
- **Volumen**: 30 días de datos históricos
- **Registros**: ~100,000 viajes
- **Rutas**: 50 rutas diferentes
- **Distritos**: 15 distritos de Lima
- **Formato**: JSON particionado por fecha/distrito

### **Esquema de Datos**
```json
{
  "trip_id": "T20240115081234",
  "route_id": "R001",
  "date": "2024-01-15",
  "scheduled_time": "08:30:00",
  "delay_minutes": 2.5,
  "passengers_on_board": 45,
  "occupancy_rate": 0.75,
  "district_origin": "Lima Centro",
  "district_destination": "Miraflores",
  "driver_id": "D1234",
  "weather_condition": "Sunny"
}
```

---

## 🔧 **COMANDOS ÚTILES**

### **Gestión del Ambiente**
```bash
# Iniciar todos los servicios
docker-compose -f 03-environments/development/docker-compose.yml up -d

# Ver estado de servicios
docker-compose ps

# Ver logs en tiempo real
docker-compose logs -f namenode

# Parar todo
docker-compose down

# Reset completo
./00-setup/scripts/setup_bigdata_env.sh reset
```

### **Comandos HDFS**
```bash
# Listar directorios
hdfs dfs -ls /

# Subir archivos
hdfs dfs -put archivo.csv /destino/

# Ver contenido
hdfs dfs -cat /archivo.txt

# Estado del cluster
hdfs dfsadmin -report
```

### **Comandos Spark**
```bash
# Ejecutar job Spark
spark-submit script.py

# Shell interactivo
pyspark

# Conectar a cluster
pyspark --master spark://spark-master:7077
```

### **Comandos Kafka**
```bash
# Listar topics
kafka-topics.sh --list --bootstrap-server localhost:9092

# Crear topic
kafka-topics.sh --create --topic test --bootstrap-server localhost:9092

# Consumir mensajes
kafka-console-consumer.sh --topic test --bootstrap-server localhost:9092
```

---

## 🆘 **TROUBLESHOOTING**

### **Problemas Comunes**

#### **🐳 Docker Issues**
```bash
# Docker no inicia
sudo systemctl start docker

# Falta memoria
docker system prune -f

# Containers no responden
docker-compose restart
```

#### **🗂️ HDFS Issues**
```bash
# NameNode no inicia
docker logs hdfs_namenode

# DataNode desconectado
docker restart hdfs_datanode1

# Permisos negados
hdfs dfs -chmod 755 /directorio
```

#### **⚡ Spark Issues**
```bash
# Workers no conectan
docker logs spark_worker_1

# Out of memory
# Ajustar: spark.executor.memory en docker-compose.yml

# Jobs muy lentos
# Verificar: http://localhost:8080 para diagnóstico
```

#### **🚀 Kafka Issues**
```bash
# Broker no inicia
docker logs kafka_broker_1

# Problemas de conexión
# Verificar: kafka-topics.sh --describe --topic test

# Consumidores bloqueados
# Resetear offsets: kafka-consumer-groups.sh --reset-offsets
```

---

## 📈 **MÉTRICAS DE ÉXITO**

### **Técnicas**
- ✅ Cluster HDFS con replicación factor 2
- ✅ Spark cluster con 2+ workers
- ✅ Kafka cluster con 3+ brokers
- ✅ Jobs ejecutándose <5 min
- ✅ 0 bloques corruptos

### **Aprendizaje**
- ✅ Configurar cluster Big Data
- ✅ Troubleshoot problemas
- ✅ Optimizar performance
- ✅ Monitorear sistemas
- ✅ Tomar decisiones arquitectónicas

---

## 🎯 **PRÓXIMOS PASOS**

### **Al Completar Sesiones 0-6**
1. **Portfolio Update**: Agregar proyecto Big Data
2. **LinkedIn Skills**: Hadoop, Spark, Kafka
3. **Certificaciones**: Considerar Cloudera/Databricks
4. **Proyectos Avanzados**: ML, Cloud Migration

### **Extensiones Futuras**
- 🌊 **Kafka Streams** (Sesión 7)
- 🤖 **Machine Learning** (Sesión 8)
- ☁️ **Cloud Migration** (Sesión 9)
- 🔒 **Security & Governance** (Sesión 10)

---

## 👥 **CONTRIBUCIÓN**

### **Para Instructores**
- Cada sesión es modular e independiente
- Material diseñado para 70% práctica / 30% teoría
- Ejercicios escalables según nivel del grupo
- Soluciones completas incluidas

### **Para Estudiantes**
- Sigue el orden de sesiones
- Completa todos los checkpoints
- Documenta tus soluciones
- Experimenta más allá de los ejercicios

---

## 📞 **SOPORTE**

### **Documentación**
- 📖 README de cada sesión
- 📝 Cheatsheets en `/04-cheatsheets/`
- 🔧 Troubleshooting guides
- 💡 Solutions en `/06-solutions/`

### **Validación Automática**
```bash
# Ejecutar validador completo
python 00-setup/scripts/validate_environment.py

# Verificar servicios específicos
./00-setup/scripts/setup_bigdata_env.sh status
```

---

**🚀 ¡Listos para dominar Big Data como los ingenieros de Google, Netflix y Amazon!**

# 🌐 Big Data Transport Analysis

## Estructura del Proyecto

```
Global_BigData/
├── 00-setup/           # Configuración inicial y scripts
├── 01-sessions/        # Sesiones de trabajo
├── 02-datasets/        # Datos y generadores
├── 03-environments/    # Entornos de práctica
├── 04-cheatsheets/     # Referencias rápidas
├── 05-monitoring/      # Herramientas de monitoreo
├── 06-solutions/       # Soluciones a ejercicios
└── 07-presentations/   # Presentaciones
```

## Entornos de Práctica

El proyecto incluye diferentes entornos configurados para cada práctica:

### Entorno de Desarrollo
- Ubicación: `03-environments/development/`
- Servicios: HDFS, Spark, Jupyter, Kafka
- Uso: Desarrollo y pruebas generales

### Práctica 1: Introducción a HDFS
- Ubicación: `03-environments/practice-01/`
- Servicios: HDFS, Jupyter
- Enfoque: Almacenamiento distribuido

### Práctica 2: Procesamiento con Spark
- Ubicación: `03-environments/practice-02/`
- Servicios: HDFS, Spark, Jupyter
- Enfoque: Procesamiento distribuido

### Práctica 3: Análisis en Tiempo Real
- Ubicación: `03-environments/practice-03/`
- Servicios: HDFS, Spark, Kafka, Jupyter
- Enfoque: Procesamiento de streaming

## Gestión de Entornos

Para gestionar los entornos, usa el script `manage_environments.py`:

```bash
# Listar entornos disponibles
python manage_environments.py list

# Iniciar un entorno
python manage_environments.py start practice-01

# Verificar estado
python manage_environments.py status practice-01

# Cambiar de entorno
python manage_environments.py switch practice-02

# Detener entorno
python manage_environments.py stop practice-01
```

## Configuración Inicial

1. **Instalar Prerequisitos**:
   ```bash
   # Windows
   cd 00-setup/scripts/windows
   .\install_prerequisites.bat

   # Mac
   cd 00-setup/scripts/mac
   ./install_prerequisites.sh
   ```

2. **Inicializar Entornos**:
   ```bash
   cd 00-setup/scripts/common
   python init_environment.py
   ```

## Servicios Disponibles

- **Jupyter Notebook**: http://localhost:8888
- **Spark UI**: http://localhost:8080
- **HDFS UI**: http://localhost:9870
- **Kafka**: localhost:9092

## Requisitos del Sistema

- **Windows**:
  - Windows 10 Pro/Enterprise/Education (64-bit)
  - 8GB RAM mínimo (16GB recomendado)
  - 20GB espacio libre en disco
  - Procesador de 64 bits con soporte para virtualización

- **Mac**:
  - macOS 10.15 o superior
  - 8GB RAM mínimo (16GB recomendado)
  - 20GB espacio libre en disco
  - Procesador Intel o Apple Silicon

- **Linux**:
  - Ubuntu 20.04 LTS o superior
  - 8GB RAM mínimo (16GB recomendado)
  - 20GB espacio libre en disco
  - Docker y Docker Compose instalados

## Notas Importantes

1. Asegúrate de tener Docker Desktop corriendo antes de ejecutar los scripts
2. Los scripts deben ejecutarse con privilegios de administrador (excepto en Mac)
3. Se recomienda reiniciar el sistema después de la instalación
4. Mantén actualizado el archivo `requirements.txt` con las últimas versiones de las dependencias
5. En Mac, asegúrate de que Homebrew esté instalado y actualizado
6. En Linux, asegúrate de tener los permisos necesarios para ejecutar Docker sin sudo

## Solución de Problemas

Si encuentras algún problema durante la instalación o configuración, consulta:
- `00-setup/docs/troubleshooting.md` para problemas generales
- El README específico de cada entorno en `03-environments/[entorno]/README.md`

## Contribución

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request