@echo off
setlocal enabledelayedexpansion

echo 🌐 Big Data Transport Analysis - Setup
echo =====================================
echo.

:: Verificar si se está ejecutando como administrador
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️  Este script requiere privilegios de administrador
    echo 💡 Por favor, ejecuta como administrador
    pause
    exit /b 1
)

:: Verificar Docker
echo 🔍 Verificando Docker...
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker no instalado
    echo 💡 Por favor, instala Docker Desktop desde https://www.docker.com/products/docker-desktop
    pause
    exit /b 1
)

:: Verificar Docker Desktop está corriendo
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker Desktop no está corriendo
    echo 💡 Por favor, inicia Docker Desktop y vuelve a intentar
    pause
    exit /b 1
)

:: Verificar Python
echo 🔍 Verificando Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python no instalado
    echo 💡 Por favor, instala Python 3.8+ desde https://www.python.org/downloads/
    pause
    exit /b 1
)

:: Verificar versión de Python
for /f "tokens=2" %%I in ('python --version 2^>^&1') do set PYTHON_VERSION=%%I
for /f "tokens=1 delims=." %%I in ("!PYTHON_VERSION!") do set PYTHON_MAJOR=%%I
for /f "tokens=2 delims=." %%I in ("!PYTHON_VERSION!") do set PYTHON_MINOR=%%I

if !PYTHON_MAJOR! LSS 3 (
    echo ❌ Se requiere Python 3.8 o superior
    echo 💡 Versión actual: !PYTHON_VERSION!
    pause
    exit /b 1
)
if !PYTHON_MAJOR! EQU 3 if !PYTHON_MINOR! LSS 8 (
    echo ❌ Se requiere Python 3.8 o superior
    echo 💡 Versión actual: !PYTHON_VERSION!
    pause
    exit /b 1
)

:: Verificar pip
echo 🔍 Verificando pip...
python -m pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ pip no instalado
    echo 💡 Por favor, instala pip
    pause
    exit /b 1
)

:: Verificar Java
echo 🔍 Verificando Java...
java -version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Java no instalado
    echo 💡 Por favor, instala Java 8+ desde https://adoptium.net/
    pause
    exit /b 1
)

:: Crear directorios necesarios
echo 📁 Creando estructura de directorios...
if not exist "hdfs" mkdir hdfs
if not exist "hdfs\namenode" mkdir hdfs\namenode
if not exist "hdfs\datanode1" mkdir hdfs\datanode1
if not exist "hdfs\datanode2" mkdir hdfs\datanode2
if not exist "spark\logs" mkdir spark\logs

:: Crear entorno virtual
echo 🚀 Creando entorno virtual...
if exist "venv" (
    echo ⚠️  El entorno virtual ya existe
    echo 💡 Eliminando entorno virtual existente...
    rmdir /s /q venv
)
python -m venv venv
call venv\Scripts\activate.bat

:: Instalar dependencias
echo 📦 Instalando dependencias...
python -m pip install --upgrade pip
pip install -r requirements.txt

:: Configurar Spark
echo ⚡ Configurando Spark...
if not exist "C:\opt" mkdir C:\opt
cd C:\opt

:: Descargar Spark si no existe
if not exist "spark-3.3.2-bin-hadoop3" (
    echo 📥 Descargando Spark...
    powershell -Command "Invoke-WebRequest -Uri 'https://downloads.apache.org/spark/spark-3.3.2/spark-3.3.2-bin-hadoop3.tgz' -OutFile 'spark-3.3.2-bin-hadoop3.tgz'"
    echo 📦 Extrayendo Spark...
    powershell -Command "tar -xzf spark-3.3.2-bin-hadoop3.tgz"
)

:: Configurar variables de entorno
echo 🔧 Configurando variables de entorno...
setx SPARK_HOME "C:\opt\spark-3.3.2-bin-hadoop3"
setx PATH "%PATH%;%SPARK_HOME%\bin"

:: Volver al directorio original
cd /d %~dp0

:: Iniciar servicios Docker
echo 🐳 Iniciando servicios Docker...
docker-compose down
docker-compose up -d

:: Esperar a que los servicios estén listos
echo ⏳ Esperando a que los servicios estén listos...
timeout /t 30 /nobreak

:: Validar instalación
echo 🧪 Validando instalación...
python test_environment.py

echo.
echo ✅ Instalación completada exitosamente!
echo.
echo 📝 Notas importantes:
echo 1. Reinicia tu terminal para que los cambios surtan efecto
echo 2. Accede a las interfaces web:
echo    - Jupyter: http://localhost:8888
echo    - Spark UI: http://localhost:8080
echo    - HDFS UI: http://localhost:9870
echo 3. Verifica el estado de los servicios:
echo    docker-compose ps
echo.
echo 🚀 ¡Listo para comenzar con Big Data!
echo.

pause 