# Configuración del Entorno Big Data

Este directorio contiene todos los scripts y configuraciones necesarias para configurar el entorno de desarrollo Big Data.

## Estructura del Directorio

```
00-setup/
├── scripts/
│   ├── windows/          # Scripts para Windows
│   │   ├── install_prerequisites.bat
│   │   └── quick_setup.bat
│   ├── mac/             # Scripts para Mac
│   │   ├── install_prerequisites.sh
│   │   └── quick_setup.sh
│   ├── linux/           # Scripts para Linux
│   │   └── quick_setup.sh
│   └── common/          # Scripts comunes
│       └── test_environment.py
├── docker/              # Configuraciones de Docker
│   └── docker-compose.yml
└── docs/               # Documentación
    └── troubleshooting.md
```

## Guía de Instalación

### Windows

1. **Instalación de Prerequisitos**:
   ```powershell
   cd scripts/windows
   .\install_prerequisites.bat
   ```
   Este script instalará:
   - Python 3.8
   - Java 8
   - Docker Desktop
   - Git
   - Visual Studio Build Tools
   - WSL2

2. **Configuración del Entorno**:
   ```powershell
   .\quick_setup.bat
   ```
   Este script:
   - Crea un entorno virtual
   - Instala dependencias
   - Configura Spark
   - Inicia los servicios Docker

### Mac

1. **Instalación de Prerequisitos**:
   ```bash
   cd scripts/mac
   chmod +x install_prerequisites.sh
   ./install_prerequisites.sh
   ```
   Este script instalará:
   - Homebrew (si no está instalado)
   - Python 3.8
   - Java 8
   - Docker Desktop
   - Git
   - VS Code y extensiones

2. **Configuración del Entorno**:
   ```bash
   chmod +x quick_setup.sh
   ./quick_setup.sh
   ```
   Este script:
   - Crea un entorno virtual
   - Instala dependencias
   - Configura Spark
   - Inicia los servicios Docker

### Linux

1. **Configuración del Entorno**:
   ```bash
   cd scripts/linux
   chmod +x quick_setup.sh
   ./quick_setup.sh
   ```

## Verificación del Entorno

Para verificar que todo está correctamente configurado:

```bash
cd scripts/common
python test_environment.py
```

## Servicios Disponibles

Después de la instalación, los siguientes servicios estarán disponibles:

- **Jupyter Notebook**: http://localhost:8888
- **Spark UI**: http://localhost:8080
- **HDFS UI**: http://localhost:9870
- **Kafka**: localhost:9092
- **Zookeeper**: localhost:2181

## Solución de Problemas

Si encuentras algún problema durante la instalación o configuración, consulta el archivo `docs/troubleshooting.md` para soluciones comunes.

## Requisitos del Sistema

- **Windows**:
  - Windows 10 Pro/Enterprise/Education (64-bit)
  - 8GB RAM mínimo (16GB recomendado)
  - 20GB espacio libre en disco
  - Procesador de 64 bits con soporte para virtualización

- **Mac**:
  - macOS 10.15 o superior
  - 8GB RAM mínimo (16GB recomendado)
  - 20GB espacio libre en disco
  - Procesador Intel o Apple Silicon

- **Linux**:
  - Ubuntu 20.04 LTS o superior
  - 8GB RAM mínimo (16GB recomendado)
  - 20GB espacio libre en disco
  - Docker y Docker Compose instalados

## Notas Importantes

1. Asegúrate de tener Docker Desktop corriendo antes de ejecutar los scripts
2. Los scripts deben ejecutarse con privilegios de administrador (excepto en Mac)
3. Se recomienda reiniciar el sistema después de la instalación
4. Mantén actualizado el archivo `requirements.txt` con las últimas versiones de las dependencias
5. En Mac, asegúrate de que Homebrew esté instalado y actualizado
6. En Linux, asegúrate de tener los permisos necesarios para ejecutar Docker sin sudo 