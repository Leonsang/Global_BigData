# 🗂️ Práctica 1: Introducción a HDFS

## Descripción
Este entorno está configurado específicamente para la práctica de HDFS (Hadoop Distributed File System). Se enfoca en el almacenamiento distribuido y la gestión de datos en un cluster Hadoop.

## Servicios Disponibles

### HDFS (Hadoop Distributed File System)
- **NameNode UI**: http://localhost:9870
- **API**: hdfs://namenode:9000
- **Configuración**: 
  - Replicación: 2
  - Block Size: 128MB
  - Permisos: Desactivados para aprendizaje

### Jupyter Lab
- **URL**: http://localhost:8888
- **Volúmenes Montados**:
  - `/home/jovyan/sessions`: Sesiones de trabajo
  - `/home/jovyan/datasets`: Datos del proyecto

## Ejercicios

### 1. Exploración Básica de HDFS
```bash
# Listar directorio raíz
hdfs dfs -ls /

# Crear directorio
hdfs dfs -mkdir /datos

# Ver espacio disponible
hdfs dfs -df -h
```

### 2. Gestión de Archivos
```bash
# Subir archivo local
hdfs dfs -put archivo.csv /datos/

# Ver contenido
hdfs dfs -cat /datos/archivo.csv

# Copiar entre directorios
hdfs dfs -cp /datos/archivo.csv /datos/backup/
```

### 3. Análisis de Distribución
```bash
# Ver estado del cluster
hdfs dfsadmin -report

# Ver bloques de un archivo
hdfs fsck /datos/archivo.csv -blocks
```

## Estructura de Directorios
```
practice-01/
├── docker-compose.yml    # Configuración HDFS
├── hadoop.env           # Variables de entorno
└── README.md           # Este archivo
```

## Comandos Útiles

### Gestión de Archivos
```bash
# Listar archivos
hdfs dfs -ls /ruta

# Subir archivo
hdfs dfs -put archivo.csv /ruta/

# Descargar archivo
hdfs dfs -get /ruta/archivo.csv ./

# Eliminar archivo
hdfs dfs -rm /ruta/archivo.csv
```

### Información del Sistema
```bash
# Estado del cluster
hdfs dfsadmin -report

# Espacio disponible
hdfs dfs -df -h

# Verificación de archivos
hdfs fsck /ruta
```

## Solución de Problemas

### NameNode
- Si el NameNode no inicia:
  ```bash
  docker logs hdfs_namenode
  ```
- Para problemas de permisos:
  ```bash
  hdfs dfs -chmod 755 /directorio
  ```

### DataNode
- Si el DataNode no conecta:
  ```bash
  docker logs hdfs_datanode
  ```
- Para verificar estado:
  ```bash
  hdfs dfsadmin -report
  ```

## Notas de Aprendizaje

1. **Conceptos Clave**:
   - NameNode vs DataNode
   - Replicación de datos
   - Block size y su importancia
   - Permisos y seguridad

2. **Buenas Prácticas**:
   - Organiza los datos en directorios lógicos
   - Usa nombres descriptivos para archivos
   - Mantén un registro de la estructura de datos
   - Verifica la replicación de datos importantes

3. **Monitoreo**:
   - Revisa regularmente el estado del cluster
   - Monitorea el espacio disponible
   - Verifica la salud de los DataNodes

## Próximos Pasos

1. Familiarízate con la interfaz web del NameNode
2. Practica los comandos básicos de HDFS
3. Experimenta con la replicación de datos
4. Prepara los datos para la siguiente práctica 