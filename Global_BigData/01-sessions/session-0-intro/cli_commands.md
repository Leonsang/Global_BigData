# 📝 Comandos CLI para Verificación del Entorno

## 🐳 Comandos Docker

### Verificar Estado de Docker
```bash
# Verificar que Docker está corriendo
docker info

# Listar contenedores activos
docker ps

# Listar todos los contenedores (incluyendo detenidos)
docker ps -a

# Ver logs de un contenedor específico
docker logs namenode
docker logs datanode
docker logs jupyter
```

### Gestión de Contenedores
```bash
# Iniciar todos los servicios
docker-compose up -d

# Detener todos los servicios
docker-compose down

# Reiniciar un servicio específico
docker-compose restart namenode

# Ver uso de recursos
docker stats
```

## 🗄️ Comandos HDFS

### Verificación del Cluster
```bash
# Ver estado del cluster
hdfs dfsadmin -report

# Ver estado del NameNode
hdfs dfsadmin -safemode get

# Ver espacio disponible
hdfs dfs -df -h

# Ver estado de los DataNodes
hdfs dfsadmin -printTopology
```

### Operaciones Básicas
```bash
# Listar directorio raíz
hdfs dfs -ls /

# Crear directorio de prueba
hdfs dfs -mkdir /test_env

# Crear archivo de prueba
echo "Hello HDFS" > test.txt
hdfs dfs -put test.txt /test_env/

# Ver contenido del archivo
hdfs dfs -cat /test_env/test.txt

# Eliminar recursos de prueba
hdfs dfs -rm -r /test_env
```

## 🔍 Verificación de Servicios

### NameNode UI
```bash
# Verificar que el puerto está abierto
curl -I http://localhost:9870

# Verificar estado del NameNode
curl http://localhost:9870/jmx
```

### DataNode UI
```bash
# Verificar que el puerto está abierto
curl -I http://localhost:9864

# Verificar estado del DataNode
curl http://localhost:9864/jmx
```

### Jupyter Lab
```bash
# Verificar que el puerto está abierto
curl -I http://localhost:8888

# Verificar logs de Jupyter
docker logs jupyter
```

## 🛠️ Comandos de Diagnóstico

### Verificar Red
```bash
# Verificar conectividad entre contenedores
docker exec namenode ping datanode
docker exec datanode ping namenode

# Verificar puertos abiertos
netstat -an | findstr "9870"
netstat -an | findstr "9864"
netstat -an | findstr "8888"
```

### Verificar Logs
```bash
# Ver logs de todos los servicios
docker-compose logs

# Ver logs de un servicio específico con seguimiento
docker-compose logs -f namenode

# Ver últimos 100 líneas de logs
docker-compose logs --tail=100
```

### Verificar Recursos
```bash
# Ver uso de CPU y memoria
docker stats --no-stream

# Ver espacio en disco
docker system df

# Ver información detallada del sistema
docker system info
```

## 🧹 Limpieza

### Limpiar Recursos
```bash
# Eliminar contenedores detenidos
docker container prune

# Eliminar imágenes no utilizadas
docker image prune

# Eliminar volúmenes no utilizados
docker volume prune

# Limpiar todo (¡usar con precaución!)
docker system prune
```

## 📝 Notas
- Ejecuta los comandos en orden secuencial
- Documenta cualquier error encontrado
- Verifica los resultados de cada comando
- Mantén un registro de los comandos ejecutados
- Consulta la documentación si tienes dudas

## ⚠️ Solución de Problemas
Si encuentras errores:
1. Verifica que Docker esté corriendo
2. Comprueba que los puertos no estén en uso
3. Revisa los logs de los servicios
4. Asegúrate de tener los permisos necesarios
5. Consulta la documentación oficial 