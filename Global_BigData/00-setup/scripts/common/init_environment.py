#!/usr/bin/env python3
"""
🌐 Big Data Transport Analysis - Inicialización del Entorno
Este script inicializa y verifica todo el entorno de Big Data
"""

import os
import sys
import json
import subprocess
import platform
from pathlib import Path

class EnvironmentManager:
    def __init__(self):
        self.root_dir = Path(__file__).parent.parent.parent.parent
        self.config = {
            "environments": {
                "development": {
                    "path": "03-environments/development",
                    "services": ["hdfs", "spark", "jupyter"],
                    "required_ports": [9870, 8080, 8888]
                },
                "practice-01": {
                    "path": "03-environments/practice-01",
                    "services": ["hdfs", "jupyter"],
                    "required_ports": [9870, 8888]
                },
                "practice-02": {
                    "path": "03-environments/practice-02",
                    "services": ["hdfs", "spark", "jupyter"],
                    "required_ports": [9870, 8080, 8888]
                },
                "practice-03": {
                    "path": "03-environments/practice-03",
                    "services": ["hdfs", "spark", "kafka", "jupyter"],
                    "required_ports": [9870, 8080, 9092, 8888]
                }
            }
        }

    def check_prerequisites(self):
        """Verifica los prerequisitos del sistema"""
        print("🔍 Verificando prerequisitos...")
        
        # Verificar Docker
        try:
            subprocess.run(["docker", "--version"], check=True, capture_output=True)
            print("✅ Docker instalado")
        except:
            print("❌ Docker no encontrado")
            return False

        # Verificar Docker Compose
        try:
            subprocess.run(["docker-compose", "--version"], check=True, capture_output=True)
            print("✅ Docker Compose instalado")
        except:
            print("❌ Docker Compose no encontrado")
            return False

        # Verificar Python
        if sys.version_info >= (3, 8):
            print("✅ Python 3.8+ instalado")
        else:
            print("❌ Se requiere Python 3.8+")
            return False

        return True

    def create_environment_structure(self):
        """Crea la estructura de directorios para los entornos"""
        print("📁 Creando estructura de entornos...")
        
        # Crear directorios para cada práctica
        for env_name in self.config["environments"]:
            env_path = self.root_dir / self.config["environments"][env_name]["path"]
            env_path.mkdir(parents=True, exist_ok=True)
            
            # Crear docker-compose.yml básico
            compose_path = env_path / "docker-compose.yml"
            if not compose_path.exists():
                self.create_basic_compose(compose_path, env_name)
            
            # Crear README.md
            readme_path = env_path / "README.md"
            if not readme_path.exists():
                self.create_readme(readme_path, env_name)

    def create_basic_compose(self, path, env_name):
        """Crea un docker-compose.yml básico según el entorno"""
        services = self.config["environments"][env_name]["services"]
        
        compose_content = f"""# 🐳 Docker Compose - {env_name}
# Configuración automática para el entorno de {env_name}

version: '3.8'

services:
"""
        
        if "hdfs" in services:
            compose_content += """
  # HDFS NameNode
  namenode:
    image: bde2020/hadoop-namenode:2.0.0-hadoop3.2.1-java8
    container_name: hdfs_namenode
    restart: unless-stopped
    ports:
      - "9870:9870"
    volumes:
      - namenode_data:/hadoop/dfs/name
    environment:
      - CLUSTER_NAME=bigdata_learning_cluster
    networks:
      - bigdata_network

  # HDFS DataNode
  datanode:
    image: bde2020/hadoop-datanode:2.0.0-hadoop3.2.1-java8
    container_name: hdfs_datanode
    restart: unless-stopped
    volumes:
      - datanode_data:/hadoop/dfs/data
    environment:
      SERVICE_PRECONDITION: "namenode:9870"
    depends_on:
      - namenode
    networks:
      - bigdata_network
"""

        if "spark" in services:
            compose_content += """
  # Spark Master
  spark-master:
    image: bde2020/spark-master:3.1.1-hadoop3.2
    container_name: spark_master
    restart: unless-stopped
    ports:
      - "8080:8080"
    environment:
      - INIT_DAEMON_STEP=setup_spark
    networks:
      - bigdata_network

  # Spark Worker
  spark-worker:
    image: bde2020/spark-worker:3.1.1-hadoop3.2
    container_name: spark_worker
    restart: unless-stopped
    environment:
      - SPARK_MASTER=spark://spark-master:7077
    depends_on:
      - spark-master
    networks:
      - bigdata_network
"""

        if "jupyter" in services:
            compose_content += """
  # Jupyter Notebook
  jupyter:
    image: jupyter/pyspark-notebook:spark-3.4.0
    container_name: jupyter_bigdata
    restart: unless-stopped
    ports:
      - "8888:8888"
    volumes:
      - ../01-sessions:/home/jovyan/sessions
      - ../02-datasets:/home/jovyan/datasets
    networks:
      - bigdata_network
"""

        compose_content += """
networks:
  bigdata_network:
    driver: bridge

volumes:
  namenode_data:
  datanode_data:
"""

        with open(path, 'w') as f:
            f.write(compose_content)

    def create_readme(self, path, env_name):
        """Crea un README.md básico para el entorno"""
        services = self.config["environments"][env_name]["services"]
        ports = self.config["environments"][env_name]["required_ports"]
        
        readme_content = f"""# Entorno de {env_name}

## Descripción
Este entorno está configurado para la práctica de Big Data.

## Servicios Disponibles
"""
        
        for service in services:
            readme_content += f"- {service.upper()}\n"
        
        readme_content += f"""
## Puertos
"""
        
        for port in ports:
            readme_content += f"- {port}\n"
        
        readme_content += """
## Uso
1. Iniciar el entorno:
   ```bash
   docker-compose up -d
   ```

2. Verificar servicios:
   ```bash
   docker-compose ps
   ```

3. Detener el entorno:
   ```bash
   docker-compose down
   ```
"""

        with open(path, 'w') as f:
            f.write(readme_content)

    def verify_environment(self, env_name):
        """Verifica que un entorno específico esté funcionando correctamente"""
        if env_name not in self.config["environments"]:
            print(f"❌ Entorno {env_name} no encontrado")
            return False

        env_path = self.root_dir / self.config["environments"][env_name]["path"]
        if not env_path.exists():
            print(f"❌ Directorio del entorno {env_name} no encontrado")
            return False

        # Verificar docker-compose.yml
        compose_path = env_path / "docker-compose.yml"
        if not compose_path.exists():
            print(f"❌ docker-compose.yml no encontrado en {env_name}")
            return False

        return True

def main():
    manager = EnvironmentManager()
    
    if not manager.check_prerequisites():
        print("❌ Prerequisitos no cumplidos")
        sys.exit(1)
    
    manager.create_environment_structure()
    
    # Verificar cada entorno
    for env_name in manager.config["environments"]:
        if manager.verify_environment(env_name):
            print(f"✅ Entorno {env_name} verificado correctamente")
        else:
            print(f"❌ Problemas con el entorno {env_name}")

if __name__ == "__main__":
    main() 