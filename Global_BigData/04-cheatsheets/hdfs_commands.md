# 🗂️ HDFS COMMANDS CHEATSHEET
## Los comandos que SÍ vas a usar (90% del tiempo)

### 🧭 **Navegación HDFS**
```bash
hdfs dfs -ls /                     # Listar directorio raíz
hdfs dfs -ls /mi_proyecto          # Listar directorio específico
hdfs dfs -ls -R /                  # Listar TODO recursivamente
```

### 📁 **Crear Directorios**
```bash
hdfs dfs -mkdir /mi_proyecto       # Crear directorio
hdfs dfs -mkdir -p /a/b/c          # Crear path completo
```

### 📤 **Subir Archivos** 
```bash
hdfs dfs -put archivo.csv /destino/              # Subir archivo
hdfs dfs -put *.csv /destino/                    # Subir múltiples archivos
hdfs dfs -copyFromLocal archivo.txt /destino/   # Igual que put
```

### 📥 **Descargar Archivos**
```bash
hdfs dfs -get /hdfs/archivo.csv .               # Descargar aquí
hdfs dfs -copyToLocal /hdfs/archivo.txt .       # Igual que get
```

### 👀 **Ver Contenido**
```bash
hdfs dfs -cat /archivo.txt                      # Ver todo el archivo
hdfs dfs -head /archivo.txt                     # Primeras líneas
hdfs dfs -tail /archivo.txt                     # Últimas líneas
```

### 📊 **Información del Sistema**
```bash
hdfs dfs -du -h /directorio                     # Tamaño legible
hdfs dfs -df -h                                 # Espacio disponible cluster
hdfs dfs -stat "%r %o %b %n" /archivo           # Info detallada archivo
```

### 🔧 **Mantenimiento**
```bash
hdfs dfs -rm /archivo.txt                       # Borrar archivo
hdfs dfs -rm -r /directorio                     # Borrar directorio completo
hdfs dfs -cp /origen /destino                   # Copiar dentro de HDFS
hdfs dfs -mv /origen /destino                   # Mover dentro de HDFS
```

### 🔍 **Diagnóstico Avanzado**
```bash
hdfs fsck /archivo -files -blocks -locations    # Análisis completo
hdfs dfsadmin -report                           # Estado del cluster
hdfs dfs -setrep 3 /archivo                    # Cambiar replicación
```

## 🎓 **Patrones Comunes de Trabajo**

### **Setup Inicial de Proyecto**
```bash
hdfs dfs -mkdir /transporte_proyecto
hdfs dfs -mkdir /transporte_proyecto/{raw,procesados,resultados}
hdfs dfs -put *.csv /transporte_proyecto/raw/
```

### **Verificar que Todo Subió Bien**
```bash
hdfs dfs -ls /transporte_proyecto/raw/
hdfs dfs -du -h /transporte_proyecto/raw/
hdfs dfs -head /transporte_proyecto/raw/datos.csv
```

### **Analizar Distribución (Para Sesión 1)**
```bash
hdfs fsck /transporte_proyecto -files -blocks -locations
hdfs dfsadmin -report
```