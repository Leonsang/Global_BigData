# 🖥️ TERMINAL ESSENTIALS - Solo lo Necesario
## Para estudiantes que NO son expertos en terminal

### 🎯 **ENFOQUE**: Solo comandos que usaremos en Big Data

## 🗂️ **Navegación Básica**
```bash
pwd                    # ¿Dónde estoy?
ls                     # ¿Qué archivos hay aquí?
ls -la                 # Ver TODO (incluso archivos ocultos)
cd directorio          # Ir a un directorio
cd ..                  # Subir un nivel
cd ~                   # Ir a mi carpeta personal
```

## 📝 **Archivos Básicos** 
```bash
cat archivo.txt        # Ver contenido completo
head archivo.txt       # Ver primeras 10 líneas
tail archivo.txt       # Ver últimas 10 líneas
wc -l archivo.txt      # Contar líneas
grep "texto" archivo   # Buscar texto en archivo
```

## 🐳 **Docker para Big Data**
```bash
# Iniciar todo el ambiente
docker-compose up -d

# Ver qué está corriendo
docker-compose ps

# Ver logs si algo falla
docker-compose logs namenode
docker-compose logs spark-master

# Parar todo
docker-compose down

# Reiniciar un servicio específico
docker-compose restart namenode
```

## 🆘 **Comandos de Emergencia**
```bash
# Si algo se rompe completamente
cd 00-setup/scripts
./setup_bigdata_env.sh reset

# Ver si todo funciona
./setup_bigdata_env.sh status

# Limpiar espacio en disco
docker system prune -f
```

## ⚠️ **NO te preocupes por**
- Permisos complejos (chmod, chown)
- Editores de texto avanzados (vim, nano) 
- Procesos del sistema (ps, kill)
- Configuración de red

**✅ Todo eso está automatizado. Enfócate en Big Data!**