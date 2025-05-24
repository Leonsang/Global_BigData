# ⚡ SESIÓN 2: MAPREDUCE - DIVIDE Y VENCERÁS
## Procesamiento Distribuido Real con Hadoop MapReduce

### 🎯 **OBJETIVOS DE APRENDIZAJE**
Al finalizar esta sesión, serás capaz de:
- ✅ Implementar jobs MapReduce reales para procesar datos masivos
- ✅ Optimizar performance de procesamiento distribuido
- ✅ Resolver problemas de data skew y cuellos de botella
- ✅ Comparar MapReduce vs Spark en casos reales
- ✅ Monitorear y debuggear jobs distribuidos

### 🧠 **CONCEPTOS CORE QUE DOMINARÁS**
- **Map Phase**: Divide el problema en sub-problemas
- **Shuffle & Sort**: Redistribuye datos eficientemente  
- **Reduce Phase**: Combina resultados parciales
- **Combiners**: Optimización de red y performance
- **Partitioners**: Control de distribución de datos

---

## 🎬 **HOOK INICIAL: El Problema de Netflix**

> *"En 2006, Netflix procesaba 1TB de logs diarios. Un servidor tardaba 18 horas. Con 100 servidores... ¿18 minutos? ¡NO! Tardaba 6 horas. ¿Por qué?"*

**El Problema**:
- Network I/O era el cuello de botella
- Datos se transferían múltiples veces
- No había optimización de localidad

**La Solución MapReduce**:
- "Mover código a los datos, no datos al código"
- Procesamiento local en cada nodo
- Mínima transferencia de red
- **Resultado**: 18 horas → 45 minutos

**¡Hoy vas a experimentar esta transformación!**

---

## 🏗️ **ARQUITECTURA MAPREDUCE QUE IMPLEMENTAREMOS**

```
📊 DATOS DE ENTRADA (HDFS)
         ↓
🗂️ INPUT SPLITS (128MB cada uno)
         ↓
⚡ MAP PHASE (Paralelo en cada nodo)
  ├─ Mapper 1 (DataNode 1)
  ├─ Mapper 2 (DataNode 1) 
  ├─ Mapper 3 (DataNode 2)
  └─ Mapper 4 (DataNode 2)
         ↓
🔄 SHUFFLE & SORT (Red mínima)
         ↓
⚡ REDUCE PHASE (Paralelo)
  ├─ Reducer 1 → Resultados parciales
  └─ Reducer 2 → Resultados parciales
         ↓
📊 SALIDA FINAL (HDFS)
```

---

## ⚡ **EJERCICIOS PRÁCTICOS REALISTAS**

### **Ejercicio 1: Análisis de Rutas de Transporte (45 min)**
**Problema Real**: Identificar rutas con mayor demanda y retrasos

**Tu Job MapReduce**:
1. **Map**: Extraer (ruta, pasajeros, retraso) de cada viaje
2. **Reduce**: Sumar pasajeros totales y retraso promedio por ruta
3. **Output**: Top 10 rutas por demanda y problemas

**Código Base**:
```python
def map_rutas(line):
    # Procesar línea JSON de viaje
    trip = json.loads(line)
    route_id = trip['route_id']
    passengers = trip['passengers_on_board']
    delay = trip['delay_minutes']
    
    emit(route_id, (passengers, delay, 1))

def reduce_rutas(route_id, values):
    total_passengers = sum(v[0] for v in values)
    total_delay = sum(v[1] for v in values)
    total_trips = sum(v[2] for v in values)
    avg_delay = total_delay / total_trips
    
    emit(route_id, (total_passengers, avg_delay, total_trips))
```

### **Ejercicio 2: Análisis de Patrones Temporales (60 min)**
**Problema Real**: Optimizar frecuencias de buses por hora del día

**Tu Job MapReduce**:
1. **Map**: Extraer (hora, distrito, demanda) de cada viaje
2. **Combiner**: Pre-agregar datos localmente (¡Optimización!)
3. **Reduce**: Calcular demanda total por hora y distrito
4. **Analysis**: Identificar patrones de horas pico

### **Ejercicio 3: Detección de Data Skew (45 min)**
**Problema Real**: Algunos distritos generan 10x más datos

**Tu Misión**:
1. Identificar distribución desigual de datos
2. Implementar partitioner customizado
3. Comparar performance antes/después
4. Documentar mejoras obtenidas

---

## 🔧 **HERRAMIENTAS DE MONITOREO**

### **Job Tracker Web UI**
- http://localhost:8088 - Resource Manager
- http://localhost:19888 - Job History Server
- http://localhost:8042 - Node Manager

### **Métricas Clave a Monitorear**
```bash
# Estado de jobs
yarn application -list -appStates RUNNING

# Performance de mappers/reducers  
yarn logs -applicationId application_xxx

# Utilización de recursos
yarn node -list -all

# Análisis de cuellos de botella
hadoop job -history all
```

---

## 📊 **OPTIMIZACIONES QUE IMPLEMENTAREMOS**

### **1. Combiners (Local Reduce)**
```python
# Sin Combiner: 1M records → Network → Reduce
# Con Combiner: 1M records → 100 records → Network → Reduce
# Reducción de tráfico: 99%
```

### **2. Custom Partitioner**  
```python
class DistrictPartitioner:
    def getPartition(key, value, numPartitions):
        # Distribuir uniformemente por distrito
        return hash(key.district) % numPartitions
```

### **3. Configuración Optimizada**
```xml
<property>
  <name>mapreduce.map.memory.mb</name>
  <value>1024</value>
</property>
<property>
  <name>mapreduce.reduce.memory.mb</name>
  <value>2048</value>
</property>
```

---

## 🆚 **MAPREDUCE vs SPARK: COMPARATIVA REAL**

### **Mismo Job, Diferentes Engines**

| Métrica | MapReduce | Spark |
|---------|-----------|-------|
| Tiempo de Ejecución | 8 min | 3 min |
| Uso de Memoria | 2GB | 6GB |
| Fault Tolerance | Disk-based | Memory-based |
| Learning Curve | Steeper | Gentler |
| Use Case Ideal | Batch ETL | Interactive Analytics |

### **¿Cuándo Usar Qué?**
- **MapReduce**: ETL masivo, datos muy grandes, presupuesto limitado
- **Spark**: Analytics iterativo, ML, desarrollo rápido

---

## 🎯 **ENTREGABLES DE LA SESIÓN**

### **1. Transport Analytics Report**
- Top 10 rutas por demanda
- Análisis de patrones temporales
- Identificación de cuellos de botella
- Recomendaciones operativas

### **2. Performance Optimization Case Study**
- Análisis before/after de optimizaciones
- Impacto de combiners y partitioners
- Recommendations para jobs futuros
- Documentación de best practices

### **3. MapReduce vs Spark Comparison**
- Benchmark del mismo job en ambos engines
- Trade-offs de performance vs recursos
- Decision framework para futuros proyectos

---

## 🚀 **VALOR PROFESIONAL**

**Habilidades que desarrollarás**:
- Pensamiento distribuido (clave para arquitectura)
- Optimización de performance (diferencia senior/junior)
- Troubleshooting de jobs distribuidos (skill escaso)
- Comparación de tecnologías (architectural decision making)

**Estas competencias te posicionan para**:
- **Data Engineer Sr**: $85k-125k
- **Big Data Architect**: $100k-150k  
- **Performance Engineer**: $95k-135k
- **Technical Lead**: $110k-160k

---

## 📋 **CHECKLIST DE FINALIZACIÓN**

- [ ] Job MapReduce ejecutándose en cluster distribuido
- [ ] Análisis de rutas completado con insights
- [ ] Optimizaciones implementadas y documentadas
- [ ] Comparativa MapReduce vs Spark realizada
- [ ] Performance tuning documentado
- [ ] Troubleshooting de al menos 1 problema real

**🎉 ¡Listo para dominar Spark en Sesión 3!**