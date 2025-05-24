#!/bin/bash

echo "🌐 Big Data Transport Analysis - Configuración Rápida (Mac)"
echo "======================================================"
echo

# Verificar si se está ejecutando como root
if [ "$EUID" -eq 0 ]; then
    echo "⚠️  No ejecutes este script como root"
    echo "💡 Ejecuta el script sin sudo"
    exit 1
fi

# Verificar Docker
echo "🔍 Verificando Docker..."
if ! command -v docker &> /dev/null; then
    echo "❌ Docker no instalado"
    echo "💡 Por favor, instala Docker Desktop desde https://www.docker.com/products/docker-desktop"
    exit 1
fi

# Verificar si Docker está corriendo
if ! docker info &> /dev/null; then
    echo "❌ Docker Desktop no está corriendo"
    echo "💡 Por favor, inicia Docker Desktop y vuelve a intentar"
    exit 1
fi

# Verificar Python
echo "🔍 Verificando Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python no instalado"
    echo "💡 Por favor, instala Python 3.8+"
    exit 1
fi

# Verificar versión de Python
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 8 ]); then
    echo "❌ Se requiere Python 3.8 o superior"
    echo "💡 Versión actual: $PYTHON_VERSION"
    exit 1
fi

# Verificar pip
echo "🔍 Verificando pip..."
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip no instalado"
    echo "💡 Por favor, instala pip"
    exit 1
fi

# Verificar Java
echo "🔍 Verificando Java..."
if ! command -v java &> /dev/null; then
    echo "❌ Java no instalado"
    echo "💡 Por favor, instala Java 8+"
    exit 1
fi

# Crear directorios necesarios
echo "📁 Creando estructura de directorios..."
mkdir -p hdfs/namenode hdfs/datanode1 hdfs/datanode2 spark/logs

# Crear entorno virtual
echo "🚀 Creando entorno virtual..."
if [ -d "venv" ]; then
    echo "⚠️  El entorno virtual ya existe"
    echo "💡 Eliminando entorno virtual existente..."
    rm -rf venv
fi
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
echo "📦 Instalando dependencias..."
pip3 install --upgrade pip
pip3 install -r requirements.txt

# Configurar Spark
echo "⚡ Configurando Spark..."
if [ ! -d "/opt/spark-3.3.2-bin-hadoop3" ]; then
    echo "📥 Descargando Spark..."
    curl -O https://downloads.apache.org/spark/spark-3.3.2/spark-3.3.2-bin-hadoop3.tgz
    echo "📦 Extrayendo Spark..."
    sudo tar -xzf spark-3.3.2-bin-hadoop3.tgz -C /opt
    sudo ln -s /opt/spark-3.3.2-bin-hadoop3 /opt/spark
fi

# Configurar variables de entorno
echo "🔧 Configurando variables de entorno..."
echo 'export SPARK_HOME=/opt/spark' >> ~/.zshrc
echo 'export PATH=$PATH:$SPARK_HOME/bin' >> ~/.zshrc
source ~/.zshrc

# Iniciar servicios Docker
echo "🐳 Iniciando servicios Docker..."
docker-compose down
docker-compose up -d

# Esperar a que los servicios estén listos
echo "⏳ Esperando a que los servicios estén listos..."
sleep 30

# Validar instalación
echo "🧪 Validando instalación..."
python3 test_environment.py

echo
echo "✅ Instalación completada exitosamente!"
echo
echo "📝 Notas importantes:"
echo "1. Reinicia tu terminal para que los cambios surtan efecto"
echo "2. Accede a las interfaces web:"
echo "   - Jupyter: http://localhost:8888"
echo "   - Spark UI: http://localhost:8080"
echo "   - HDFS UI: http://localhost:9870"
echo "3. Verifica el estado de los servicios:"
echo "   docker-compose ps"
echo
echo "🚀 ¡Listo para comenzar con Big Data!"
echo

read -p "Presiona Enter para continuar..." 