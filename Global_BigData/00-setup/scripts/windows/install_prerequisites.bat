@echo off
setlocal enabledelayedexpansion

echo 🌐 Big Data Transport Analysis - Instalación de Prerequisitos
echo ============================================================
echo.
echo 📋 Guía de Instalación:
echo ----------------------
echo 1. Este script instalará todos los componentes necesarios para el proyecto
echo 2. Se requiere conexión a internet estable
echo 3. El proceso puede tomar entre 30-60 minutos
echo 4. Se recomienda cerrar todas las aplicaciones antes de comenzar
echo 5. Se necesitarán varios reinicios durante el proceso
echo.
echo ⚠️  IMPORTANTE: Antes de continuar:
echo - Asegúrate de tener al menos 20GB de espacio libre en disco
echo - Tener una conexión a internet estable
echo - Cerrar todas las aplicaciones en ejecución
echo - Tener permisos de administrador
echo.
echo ¿Deseas continuar con la instalación? (S/N)
set /p CONTINUAR=

if /i not "%CONTINUAR%"=="S" (
    echo.
    echo ❌ Instalación cancelada por el usuario
    pause
    exit /b 1
)

echo.
echo 🚀 Iniciando instalación...
echo.

:: Verificar si se está ejecutando como administrador
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️  Este script requiere privilegios de administrador
    echo 💡 Por favor, ejecuta como administrador
    pause
    exit /b 1
)

:: Verificar espacio en disco
echo 🔍 Verificando espacio en disco...
for /f "tokens=3" %%a in ('dir /-c 2^>nul ^| find "bytes free"') do set FREE_SPACE=%%a
set /a FREE_SPACE_GB=%FREE_SPACE:~0,-9%
if %FREE_SPACE_GB% LSS 20 (
    echo ⚠️  Espacio insuficiente en disco
    echo 💡 Se requieren al menos 20GB de espacio libre
    echo 💡 Espacio actual: %FREE_SPACE_GB%GB
    pause
    exit /b 1
)

:: Verificar conexión a internet
echo 🔍 Verificando conexión a internet...
ping -n 1 google.com >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️  No hay conexión a internet
    echo 💡 Por favor, verifica tu conexión e intenta nuevamente
    pause
    exit /b 1
)

:: Verificar si Chocolatey está instalado
echo 🔍 Verificando Chocolatey...
where choco >nul 2>&1
if %errorlevel% neq 0 (
    echo 📦 Instalando Chocolatey...
    echo 💡 Esto puede tomar unos minutos...
    powershell -Command "Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))"
    set "PATH=%PATH%;%ALLUSERSPROFILE%\chocolatey\bin"
    echo ✅ Chocolatey instalado correctamente
)

:: Instalar Python
echo 🔍 Verificando Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 📦 Instalando Python 3.8.10...
    echo 💡 Esto puede tomar unos minutos...
    choco install python --version=3.8.10 -y
    set "PATH=%PATH%;%LOCALAPPDATA%\Programs\Python\Python38\Scripts"
    echo ✅ Python instalado correctamente
)

:: Instalar Java
echo 🔍 Verificando Java...
java -version >nul 2>&1
if %errorlevel% neq 0 (
    echo 📦 Instalando Java 8...
    echo 💡 Esto puede tomar unos minutos...
    choco install adoptopenjdk8 -y
    echo ✅ Java instalado correctamente
)

:: Instalar Git
echo 🔍 Verificando Git...
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 📦 Instalando Git...
    echo 💡 Esto puede tomar unos minutos...
    choco install git -y
    echo ✅ Git instalado correctamente
)

:: Instalar Docker Desktop
echo 🔍 Verificando Docker...
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 📦 Instalando Docker Desktop...
    echo 💡 Esto puede tomar varios minutos...
    choco install docker-desktop -y
    echo.
    echo ⚠️  IMPORTANTE: Después de la instalación:
    echo 1. Reinicia tu computadora
    echo 2. Inicia Docker Desktop
    echo 3. Acepta los términos de servicio
    echo 4. Espera a que Docker Desktop esté completamente iniciado
    echo 5. Verifica que Docker Desktop esté corriendo en la bandeja del sistema
    echo.
    echo 💡 Docker Desktop es necesario para ejecutar los contenedores
    echo 💡 Si tienes problemas, consulta la documentación oficial:
    echo 💡 https://docs.docker.com/desktop/windows/install/
    echo.
    pause
)

:: Instalar Visual Studio Build Tools
echo 🔍 Verificando Visual Studio Build Tools...
if not exist "C:\Program Files (x86)\Microsoft Visual Studio\2019\BuildTools" (
    echo 📦 Instalando Visual Studio Build Tools...
    echo 💡 Esto puede tomar varios minutos...
    choco install visualstudio2019buildtools -y
    choco install visualstudio2019-workload-vctools -y
    echo ✅ Visual Studio Build Tools instalado correctamente
)

:: Instalar WSL2 (Windows Subsystem for Linux)
echo 🔍 Verificando WSL2...
wsl --status >nul 2>&1
if %errorlevel% neq 0 (
    echo 📦 Instalando WSL2...
    echo 💡 Esto puede tomar varios minutos...
    wsl --install
    echo.
    echo ⚠️  IMPORTANTE: Después de la instalación:
    echo 1. Reinicia tu computadora
    echo 2. Configura tu usuario y contraseña de WSL
    echo 3. Verifica que WSL2 esté funcionando con el comando 'wsl --status'
    echo.
    echo 💡 WSL2 es necesario para algunas funcionalidades de Docker
    echo 💡 Si tienes problemas, consulta la documentación oficial:
    echo 💡 https://docs.microsoft.com/windows/wsl/install
    echo.
    pause
)

:: Instalar extensiones de VS Code recomendadas
echo 🔍 Verificando VS Code...
code --version >nul 2>&1
if %errorlevel% equ 0 (
    echo 📦 Instalando extensiones de VS Code...
    echo 💡 Instalando extensiones para Python...
    code --install-extension ms-python.python
    echo 💡 Instalando extensiones para Docker...
    code --install-extension ms-azuretools.vscode-docker
    echo 💡 Instalando extensiones para Jupyter...
    code --install-extension ms-toolsai.jupyter
    echo 💡 Instalando extensiones para Java...
    code --install-extension redhat.java
    echo ✅ Extensiones de VS Code instaladas correctamente
)

:: Crear archivo de requisitos si no existe
if not exist "requirements.txt" (
    echo 📝 Creando archivo requirements.txt...
    (
        echo numpy==1.21.0
        echo pandas==1.3.0
        echo pyspark==3.3.2
        echo jupyter==1.0.0
        echo kafka-python==2.0.2
        echo python-dotenv==0.19.0
        echo requests==2.26.0
        echo matplotlib==3.4.3
        echo seaborn==0.11.2
        echo scikit-learn==0.24.2
    ) > requirements.txt
    echo ✅ Archivo requirements.txt creado correctamente
)

echo.
echo ✅ Instalación de prerequisitos completada!
echo.
echo 📝 Pasos siguientes:
echo 1. Reinicia tu computadora
echo 2. Después de reiniciar, ejecuta quick_setup.bat como administrador
echo.
echo 🔍 Verificación post-instalación:
echo 1. Abre una nueva terminal como administrador
echo 2. Verifica que Docker Desktop esté corriendo
echo 3. Ejecuta 'docker --version' para confirmar la instalación
echo 4. Ejecuta 'python --version' para confirmar Python 3.8
echo 5. Ejecuta 'java -version' para confirmar Java 8
echo.
echo 💡 Recursos útiles:
echo - Documentación de Docker: https://docs.docker.com/
echo - Documentación de Python: https://docs.python.org/3/
echo - Documentación de Spark: https://spark.apache.org/docs/latest/
echo - Documentación de Kafka: https://kafka.apache.org/documentation/
echo.
echo 🚀 ¡Listo para comenzar con la configuración del entorno!
echo.

pause 