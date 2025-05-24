#!/usr/bin/env python3
"""
🌐 Big Data Transport Analysis - Gestor de Entornos
Este script permite gestionar los diferentes entornos de práctica
"""

import os
import sys
import json
import subprocess
from pathlib import Path

class EnvironmentController:
    def __init__(self):
        self.root_dir = Path(__file__).parent.parent.parent.parent
        self.environments_dir = self.root_dir / "03-environments"
        self.current_env = None

    def list_environments(self):
        """Lista todos los entornos disponibles"""
        print("📋 Entornos disponibles:")
        for env_dir in self.environments_dir.iterdir():
            if env_dir.is_dir():
                print(f"- {env_dir.name}")

    def start_environment(self, env_name):
        """Inicia un entorno específico"""
        env_path = self.environments_dir / env_name
        if not env_path.exists():
            print(f"❌ Entorno {env_name} no encontrado")
            return False

        print(f"🚀 Iniciando entorno {env_name}...")
        try:
            subprocess.run(["docker-compose", "up", "-d"], 
                         cwd=env_path, 
                         check=True)
            print(f"✅ Entorno {env_name} iniciado correctamente")
            self.current_env = env_name
            return True
        except subprocess.CalledProcessError:
            print(f"❌ Error al iniciar el entorno {env_name}")
            return False

    def stop_environment(self, env_name):
        """Detiene un entorno específico"""
        env_path = self.environments_dir / env_name
        if not env_path.exists():
            print(f"❌ Entorno {env_name} no encontrado")
            return False

        print(f"🛑 Deteniendo entorno {env_name}...")
        try:
            subprocess.run(["docker-compose", "down"], 
                         cwd=env_path, 
                         check=True)
            print(f"✅ Entorno {env_name} detenido correctamente")
            if self.current_env == env_name:
                self.current_env = None
            return True
        except subprocess.CalledProcessError:
            print(f"❌ Error al detener el entorno {env_name}")
            return False

    def check_environment_status(self, env_name):
        """Verifica el estado de un entorno"""
        env_path = self.environments_dir / env_name
        if not env_path.exists():
            print(f"❌ Entorno {env_name} no encontrado")
            return False

        print(f"🔍 Verificando estado del entorno {env_name}...")
        try:
            result = subprocess.run(["docker-compose", "ps"], 
                                  cwd=env_path, 
                                  capture_output=True, 
                                  text=True)
            print(result.stdout)
            return True
        except subprocess.CalledProcessError:
            print(f"❌ Error al verificar el estado del entorno {env_name}")
            return False

    def switch_environment(self, new_env):
        """Cambia de un entorno a otro"""
        if self.current_env:
            self.stop_environment(self.current_env)
        
        return self.start_environment(new_env)

def print_help():
    """Muestra la ayuda del script"""
    print("""
🌐 Gestor de Entornos Big Data

Uso:
  python manage_environments.py [comando] [entorno]

Comandos disponibles:
  list                    Lista todos los entornos disponibles
  start [entorno]         Inicia un entorno específico
  stop [entorno]          Detiene un entorno específico
  status [entorno]        Muestra el estado de un entorno
  switch [entorno]        Cambia a otro entorno
  help                    Muestra esta ayuda

Ejemplos:
  python manage_environments.py list
  python manage_environments.py start practice-01
  python manage_environments.py status development
  python manage_environments.py switch practice-02
""")

def main():
    controller = EnvironmentController()
    
    if len(sys.argv) < 2:
        print_help()
        return

    command = sys.argv[1].lower()
    
    if command == "list":
        controller.list_environments()
    
    elif command == "start":
        if len(sys.argv) < 3:
            print("❌ Debes especificar un entorno")
            return
        controller.start_environment(sys.argv[2])
    
    elif command == "stop":
        if len(sys.argv) < 3:
            print("❌ Debes especificar un entorno")
            return
        controller.stop_environment(sys.argv[2])
    
    elif command == "status":
        if len(sys.argv) < 3:
            print("❌ Debes especificar un entorno")
            return
        controller.check_environment_status(sys.argv[2])
    
    elif command == "switch":
        if len(sys.argv) < 3:
            print("❌ Debes especificar un entorno")
            return
        controller.switch_environment(sys.argv[2])
    
    elif command == "help":
        print_help()
    
    else:
        print("❌ Comando no reconocido")
        print_help()

if __name__ == "__main__":
    main() 