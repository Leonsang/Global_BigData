# 🔧 TROUBLESHOOTING GUIDE
## Soluciones a Problemas Comunes - Big Data Environment

### 🎯 **FILOSOFÍA DE TROUBLESHOOTING**
Como ingeniera de datos experta, siempre sigo este proceso:
1. **Reproducir** el problema
2. **Aislar** la causa raíz  
3. **Verificar** la solución
4. **Documentar** para futuros casos

---

## 🐳 **PROBLEMAS DOCKER**

### **Error: "Docker not running"**
```bash
# Síntomas
Cannot connect to the Docker daemon at unix:///var/run/docker.sock

# Solución Windows
1. Abrir Docker Desktop
2. Esperar que inicie completamente
3. Verificar: docker version

# Solución Linux/Mac
sudo systemctl start docker
# o
sudo service docker start
```

### **Error: "Container fails to start"**
```bash
# Diagnóstico
docker-compose logs [nombre_servicio]

# Solución común: Conflicto de puertos
netstat -ano | findstr :9870
# Si puerto ocupado, cambiar en docker-compose.yml

# Solución: Limpiar containers corruptos
docker-compose down
docker system prune -f
docker-compose up -d
```

### **Error: "Out of disk space"**
```bash
# Verificar espacio
docker system df

# Limpiar imágenes no usadas
docker system prune -a

# Limpiar volúmenes
docker volume prune
```

---

## 🗂️ **PROBLEMAS HDFS**

### **Error: "NameNode not accessible"**
```bash
# Síntomas
http://localhost:9870 no responde

# Diagnóstico
docker logs hdfs_namenode

# Soluciones comunes
1. Reiniciar NameNode:
   docker-compose restart namenode

2. Si persiste, reset completo:
   docker-compose down -v
   docker-compose up -d

3. Verificar logs detallados:
   docker exec hdfs_namenode cat /hadoop/logs/hadoop-root-namenode-*.log
```

### **Error: "DataNode disconnected"**
```bash
# Síntomas
hdfs dfsadmin -report muestra nodos muertos

# Diagnóstico  
docker logs hdfs_datanode1
docker logs hdfs_datanode2

# Solución
docker-compose restart datanode1 datanode2

# Verificar reconexión
hdfs dfsadmin -report
```

### **Error: "Permission denied in HDFS"**
```bash
# Síntomas
hdfs dfs -put: Permission denied

# Solución rápida (desarrollo)
hdfs dfs -chmod 777 /
hdfs dfs -mkdir /mi_directorio
hdfs dfs -chmod 755 /mi_directorio

# Solución robusta
hdfs dfs -chown $USER:$USER /mi_directorio
```

### **Error: "SafeMode enabled"**
```bash
# Síntomas
Name node is in safe mode

# Verificar estado
hdfs dfsadmin -safemode get

# Salir del safe mode (SOLO desarrollo)
hdfs dfsadmin -safemode leave

# Si persiste, verificar replicación
hdfs fsck / -files -blocks
```

---

## ⚡ **PROBLEMAS SPARK**

### **Error: "Spark Master not accessible"**
```bash
# Síntomas
http://localhost:8080 no responde

# Diagnóstico
docker logs spark_master

# Solución
docker-compose restart spark-master

# Verificar configuración
docker exec spark_master cat /spark/conf/spark-env.sh
```

### **Error: "Workers not connecting"**
```bash
# Síntomas
Spark UI muestra 0 workers

# Diagnóstico
docker logs spark_worker_1
docker logs spark_worker_2

# Solución común: Network issues
docker-compose down
docker network prune
docker-compose up -d

# Verificar conectividad
docker exec spark_worker_1 ping spark-master
```

### **Error: "OutOfMemoryError en Spark"**
```bash
# Síntomas
Job fails with java.lang.OutOfMemoryError

# Solución 1: Ajustar configuración en docker-compose.yml
SPARK_WORKER_MEMORY=4g
SPARK_EXECUTOR_MEMORY=2g

# Solución 2: En código PySpark
spark.conf.set("spark.executor.memory", "2g")
spark.conf.set("spark.driver.memory", "1g")

# Solución 3: Reducir tamaño de datos
df.sample(0.1).write.parquet("sample_data")
```

### **Error: "Spark job muy lento"**
```bash
# Diagnóstico en Spark UI
http://localhost:4040

# Optimizaciones comunes
1. Aumentar paralelismo:
   df.repartition(8)

2. Usar cache inteligentemente:
   df.cache()

3. Evitar shuffles innecesarios:
   df.coalesce(4) en lugar de repartition()

4. Optimizar joins:
   broadcast(df_pequeño).join(df_grande)
```

---

## 📓 **PROBLEMAS JUPYTER**

### **Error: "Jupyter not accessible"**
```bash
# Síntomas
http://localhost:8888 no responde

# Diagnóstico
docker logs jupyter_bigdata

# Solución común
docker-compose restart jupyter

# Si pide token
docker logs jupyter_bigdata | grep token
# Copiar URL completa con token
```

### **Error: "Kernel dies en notebooks"**
```bash
# Síntomas
Kernel keeps dying cuando ejecutas celdas

# Solución 1: Reiniciar kernel
Kernel -> Restart

# Solución 2: Aumentar memoria del container
En docker-compose.yml:
deploy:
  resources:
    limits:
      memory: 4G

# Solución 3: Limpiar outputs
Cell -> All Output -> Clear
```

### **Error: "No module named 'pyspark'"**
```bash
# Verificar instalación
docker exec jupyter_bigdata pip list | grep pyspark

# Si no está instalado
docker exec jupyter_bigdata pip install pyspark

# O reconstruir imagen
docker-compose build jupyter
docker-compose up -d jupyter
```

---

## 🌐 **PROBLEMAS DE RED**

### **Error: "Containers can't communicate"**
```bash
# Diagnóstico
docker network ls
docker network inspect bigdata_bigdata

# Solución: Recrear network
docker-compose down
docker network prune
docker-compose up -d

# Verificar comunicación
docker exec namenode ping datanode1
docker exec spark_master ping spark_worker_1
```

### **Error: "Port already in use"**
```bash
# Síntomas
Port 9870 is already allocated

# Encontrar proceso
netstat -ano | findstr :9870
# Windows: taskkill /PID <pid> /F
# Linux: kill -9 <pid>

# O cambiar puerto en docker-compose.yml
ports:
  - "9871:9870"  # Usar puerto diferente
```

---

## 💾 **PROBLEMAS DE DATOS**

### **Error: "No such file or directory en HDFS"**
```bash
# Verificar path exacto
hdfs dfs -ls /
hdfs dfs -ls /transport_data

# Crear directorios faltantes
hdfs dfs -mkdir -p /transport_data/historical

# Subir datos de nuevo
hdfs dfs -put datos.csv /transport_data/
```

### **Error: "Corrupted blocks in HDFS"**
```bash
# Diagnóstico
hdfs fsck / -files -blocks -locations

# Ver bloques corruptos
hdfs fsck / -list-corruptfileblocks

# Solución (desarrollo)
hdfs dfsadmin -report
# Si replicación baja, aumentar:
hdfs dfs -setrep 2 /archivo_problema
```

---

## 🔄 **RESET COMPLETO DEL AMBIENTE**

### **Cuando nada más funciona**
```bash
# Script automático
./00-setup/scripts/setup_bigdata_env.sh reset

# O manualmente:
cd 03-environments/development

# Parar todo
docker-compose down -v

# Limpiar completamente
docker system prune -a -f
docker volume prune -f

# Reiniciar
docker-compose up -d

# Esperar y validar
sleep 60
python ../../00-setup/scripts/validate_environment.py
```

---

## 📊 **VALIDACIÓN PASO A PASO**

### **Checklist de Diagnóstico**
```bash
# 1. Docker funcionando
docker version
docker-compose version

# 2. Servicios corriendo
docker-compose ps

# 3. Puertos accesibles
curl http://localhost:9870  # HDFS
curl http://localhost:8080  # Spark
curl http://localhost:8888  # Jupyter

# 4. HDFS operativo
hdfs dfs -ls /

# 5. Spark conectado
docker exec spark_master cat /spark/conf/spark-env.sh

# 6. Jupyter funcionando
docker logs jupyter_bigdata | tail -20
```

---

## 💡 **TIPS DE EXPERTA**

### **Desarrollo Eficiente**
1. **Siempre verifica logs** antes de buscar en Google
2. **Usa docker-compose logs -f** para debug en tiempo real
3. **Prueba con datos pequeños** antes de datasets grandes
4. **Documenta cada problema** que resuelvas

### **Performance**
1. **Monitorea recursos** con `docker stats`
2. **Usa cache** inteligentemente en Spark
3. **Particiona datos** por fecha/región en HDFS
4. **Ajusta paralelismo** según tu hardware

### **Debugging**
1. **Reproduce en ambiente limpio** antes de reportar bugs
2. **Aísla el problema** (¿Docker? ¿HDFS? ¿Spark? ¿Código?)
3. **Verifica logs** en orden cronológico
4. **Compara con configuración funcional**

---

## 🆘 **ÚLTIMA INSTANCIA**

Si después de todo esto sigues teniendo problemas:

1. **Documenta exactamente**:
   - Qué comando ejecutaste
   - Qué error obtuviste (screenshot)
   - Qué logs relevantes tienes
   - Qué ya intentaste

2. **Verifica el estado**:
   ```bash
   python 00-setup/scripts/validate_environment.py > debug_report.txt
   ```

3. **Reset y reinténtalo**:
   ```bash
   ./00-setup/scripts/setup_bigdata_env.sh reset
   ./00-setup/scripts/setup_bigdata_env.sh setup
   ```

**¡La mayoría de problemas se resuelven con reset + setup!** 🎯