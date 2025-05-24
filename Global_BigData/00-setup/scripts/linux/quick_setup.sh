#!/bin/bash
# Quick Setup Script for Big Data Transport Analysis Project

# Verificar prerequisitos
check_prerequisites() {
    echo "🔍 Verificando prerequisitos..."
    
    # Comprobar Python
    python_version=$(python3 --version 2>/dev/null)
    if [ $? -ne 0 ]; then
        echo "❌ Python no instalado. Por favor instala Python 3.8+"
        exit 1
    fi
    
    # Comprobar pip
    pip_version=$(pip3 --version 2>/dev/null)
    if [ $? -ne 0 ]; then
        echo "❌ pip no instalado. Por favor instala pip"
        exit 1
    fi
}    # Comprobar Java
    java_version=$(java -version 2>&1 | awk -F '"' '/version/ {print $2}')
    if [ $? -ne 0 ]; then
        echo "❌ Java no instalado. Requiere Java 8+"
        exit 1
    fi
}

# Crear entorno virtual
create_virtual_env() {
    echo "🚀 Creando entorno virtual..."
    python3 -m venv venv
    source venv/bin/activate
}

# Instalar dependencias
install_dependencies() {
    echo "📦 Instalando dependencias..."
    pip install --upgrade pip
    pip install -r requirements.txt
}# Configurar Spark
setup_spark() {
    echo "⚡ Configurando Spark..."
    # Descargar e instalar Spark
    wget https://downloads.apache.org/spark/spark-3.3.2/spark-3.3.2-bin-hadoop3.tgz
    tar -xzf spark-3.3.2-bin-hadoop3.tgz
    mv spark-3.3.2-bin-hadoop3 /opt/spark
    
    # Configurar variables de entorno
    echo "export SPARK_HOME=/opt/spark" >> ~/.bashrc
    echo "export PATH=$PATH:$SPARK_HOME/bin" >> ~/.bashrc
    source ~/.bashrc
}

# Validar instalación
validate_installation() {
    echo "🧪 Validando instalación..."
    spark-submit --version
    python3 test_environment.py
}

# Menú principal
main() {
    clear
    echo "🌐 Big Data Transport Analysis - Setup"
    
    check_prerequisites
    create_virtual_env
    install_dependencies
    setup_spark
    validate_installation
    
    echo "✅ Instalación completada exitosamente!"
}

# Ejecutar
main