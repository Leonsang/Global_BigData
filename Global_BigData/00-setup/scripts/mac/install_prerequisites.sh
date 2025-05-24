#!/bin/bash

echo "🌐 Big Data Transport Analysis - Instalación de Prerequisitos (Mac)"
echo "============================================================"
echo

# Verificar si Homebrew está instalado
echo "🔍 Verificando Homebrew..."
if ! command -v brew &> /dev/null; then
    echo "📦 Instalando Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    echo "✅ Homebrew instalado correctamente"
fi

# Verificar Python
echo "🔍 Verificando Python..."
if ! command -v python3 &> /dev/null; then
    echo "📦 Instalando Python 3.8..."
    brew install python@3.8
    echo "✅ Python instalado correctamente"
fi

# Verificar Java
echo "🔍 Verificando Java..."
if ! command -v java &> /dev/null; then
    echo "📦 Instalando Java 8..."
    brew tap adoptopenjdk/openjdk
    brew install --cask adoptopenjdk8
    echo "✅ Java instalado correctamente"
fi

# Verificar Git
echo "🔍 Verificando Git..."
if ! command -v git &> /dev/null; then
    echo "📦 Instalando Git..."
    brew install git
    echo "✅ Git instalado correctamente"
fi

# Verificar Docker
echo "🔍 Verificando Docker..."
if ! command -v docker &> /dev/null; then
    echo "📦 Instalando Docker Desktop..."
    brew install --cask docker
    echo
    echo "⚠️  IMPORTANTE: Después de la instalación:"
    echo "1. Abre Docker Desktop desde tus aplicaciones"
    echo "2. Acepta los términos de servicio"
    echo "3. Espera a que Docker Desktop esté completamente iniciado"
    echo
    echo "💡 Docker Desktop es necesario para ejecutar los contenedores"
    echo "💡 Si tienes problemas, consulta la documentación oficial:"
    echo "💡 https://docs.docker.com/desktop/mac/install/"
    echo
    read -p "Presiona Enter cuando hayas completado estos pasos..."
fi

# Verificar VS Code
echo "🔍 Verificando VS Code..."
if ! command -v code &> /dev/null; then
    echo "📦 Instalando VS Code..."
    brew install --cask visual-studio-code
    echo "✅ VS Code instalado correctamente"
fi

# Instalar extensiones de VS Code
if command -v code &> /dev/null; then
    echo "📦 Instalando extensiones de VS Code..."
    echo "💡 Instalando extensiones para Python..."
    code --install-extension ms-python.python
    echo "💡 Instalando extensiones para Docker..."
    code --install-extension ms-azuretools.vscode-docker
    echo "💡 Instalando extensiones para Jupyter..."
    code --install-extension ms-toolsai.jupyter
    echo "💡 Instalando extensiones para Java..."
    code --install-extension redhat.java
    echo "✅ Extensiones de VS Code instaladas correctamente"
fi

# Crear archivo de requisitos si no existe
if [ ! -f "requirements.txt" ]; then
    echo "📝 Creando archivo requirements.txt..."
    cat > requirements.txt << EOL
numpy==1.21.0
pandas==1.3.0
pyspark==3.3.2
jupyter==1.0.0
kafka-python==2.0.2
python-dotenv==0.19.0
requests==2.26.0
matplotlib==3.4.3
seaborn==0.11.2
scikit-learn==0.24.2
EOL
    echo "✅ Archivo requirements.txt creado correctamente"
fi

echo
echo "✅ Instalación de prerequisitos completada!"
echo
echo "📝 Pasos siguientes:"
echo "1. Reinicia tu terminal"
echo "2. Ejecuta quick_setup.sh"
echo
echo "🔍 Verificación post-instalación:"
echo "1. Abre una nueva terminal"
echo "2. Verifica que Docker Desktop esté corriendo"
echo "3. Ejecuta 'docker --version' para confirmar la instalación"
echo "4. Ejecuta 'python3 --version' para confirmar Python 3.8"
echo "5. Ejecuta 'java -version' para confirmar Java 8"
echo
echo "💡 Recursos útiles:"
echo "- Documentación de Docker: https://docs.docker.com/"
echo "- Documentación de Python: https://docs.python.org/3/"
echo "- Documentación de Spark: https://spark.apache.org/docs/latest/"
echo "- Documentación de Kafka: https://kafka.apache.org/documentation/"
echo
echo "🚀 ¡Listo para comenzar con la configuración del entorno!"
echo

read -p "Presiona Enter para continuar..." 