# 📝 Ejercicios Prácticos HDFS

## 🎯 Ejercicios de Clase (Obligatorios)

### Ejercicio 1: Exploración Básica
1. Lista el contenido del directorio raíz de HDFS
2. Crea un directorio llamado `/datos` en HDFS
3. Crea subdirectorios para organizar datos:
   - `/datos/raw` para datos sin procesar
   - `/datos/processed` para datos procesados

### Ejercicio 2: Comandos Esenciales
1. Usa `hdfs dfs -ls` para listar archivos
2. Usa `hdfs dfs -cat` para ver el contenido de un archivo
3. Usa `hdfs dfs -df` para ver el espacio disponible

## 🎯 Ejercicios Adicionales (Opcionales)

### Ejercicio 3: Gestión de Archivos
1. Sube un archivo de texto local a HDFS
2. Verifica que el archivo se haya subido correctamente
3. Crea una copia del archivo en el directorio de backup
4. Elimina el archivo original y verifica que la copia persista

### Ejercicio 4: Análisis de Bloques
1. Sube un archivo grande (>128MB) a HDFS
2. Usa `hdfs fsck` para ver cómo se dividió en bloques
3. Verifica la replicación de los bloques
4. Analiza la distribución de los bloques entre DataNodes

### Ejercicio 5: Gestión de Permisos
1. Crea un directorio `/datos/privado`
2. Establece permisos restrictivos (700)
3. Intenta acceder al directorio con diferentes usuarios
4. Modifica los permisos para permitir acceso de grupo

### Ejercicio 6: Monitoreo del Cluster
1. Usa `hdfs dfsadmin -report` para ver el estado del cluster
2. Identifica:
   - Número de DataNodes activos
   - Espacio total disponible
   - Espacio usado
   - Estado de replicación

## 🎯 Ejercicios Avanzados (Opcionales)

### Ejercicio 7: Optimización de Almacenamiento
1. Sube un conjunto de archivos pequeños
2. Analiza el impacto en el espacio usado
3. Combina los archivos pequeños en uno más grande
4. Compara el espacio usado antes y después

### Ejercicio 8: Recuperación de Datos
1. Simula la caída de un DataNode
2. Verifica cómo HDFS maneja la replicación
3. Recupera el DataNode
4. Analiza el proceso de rebalanceo

### Ejercicio 9: Análisis de Rendimiento
1. Mide el tiempo de escritura de archivos grandes
2. Mide el tiempo de lectura de archivos grandes
3. Analiza el throughput del cluster
4. Identifica cuellos de botella

## 🎯 Proyecto Final (Opcional)

### Ejercicio 10: Pipeline de Datos
1. Crea una estructura de directorios para un proyecto:
   ```
   /proyecto/
   ├── raw/           # Datos sin procesar
   ├── processed/     # Datos procesados
   ├── backup/        # Copias de seguridad
   └── logs/          # Logs del sistema
   ```

2. Implementa un proceso de:
   - Subida de datos
   - Procesamiento
   - Backup
   - Limpieza

## 💡 Notas Importantes

### Ejercicios de Clase
- Se desarrollarán durante la sesión
- Son fundamentales para entender HDFS
- Se recomienda completarlos todos

### Ejercicios Adicionales
- Son opcionales pero recomendados
- Ayudan a profundizar en el conocimiento
- Pueden realizarse en cualquier momento

### Ejercicios Avanzados
- Son completamente opcionales
- Requieren más tiempo y dedicación
- Ideales para práctica adicional

## 📚 Recursos de Ayuda
- Documentación oficial de HDFS
- Comandos básicos en el README
- Ejemplos en los notebooks de la sesión
- Foros y comunidades de Hadoop

## 📊 Criterios de Evaluación

### Nivel Básico
- Correcta ejecución de comandos básicos
- Comprensión de la estructura de directorios
- Manejo adecuado de archivos

### Nivel Intermedio
- Análisis correcto de bloques y replicación
- Gestión efectiva de permisos
- Monitoreo básico del cluster

### Nivel Avanzado
- Optimización de almacenamiento
- Manejo de fallos y recuperación
- Análisis de rendimiento

### Ejercicio Final
- Implementación completa del pipeline
- Documentación detallada
- Solución de problemas
- Optimización del sistema

## 💡 Consejos
- Mantén un registro de todos los comandos utilizados
- Documenta cualquier error encontrado
- Prueba diferentes configuraciones
- Analiza el impacto de cada operación
- Verifica regularmente el estado del cluster 