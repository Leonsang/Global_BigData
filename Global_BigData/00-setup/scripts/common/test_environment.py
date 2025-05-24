import sys
import pyspark
import pandas
import numpy

def validate_python_version():
    """Validar versión de Python"""
    print("🐍 Validando versión de Python...")
    version = sys.version_info
    if version.major == 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor} - OK")
        return True
    else:
        print(f"❌ Versión de Python inválida: {version.major}.{version.minor}")
        return False

def validate_spark_installation():
    """Validar instalación de Spark"""
    print("⚡ Validando instalación de Spark...")
    try:
        print(f"Spark Version: {pyspark.__version__}")
        print("✅ Spark instalado correctamente")
        return True
    except Exception as e:
        print(f"❌ Error en instalación de Spark: {e}")
        return False

def validate_data_science_libraries():
    """Validar librerías de análisis de datos"""
    print("📊 Validando librerías de análisis...")
    libraries = [
        ("Pandas", pandas.__version__),
        ("NumPy", numpy.__version__)
    ]
    
    for name, version in libraries:
        print(f"{name} Version: {version}")
    
    print("✅ Librerías de análisis OK")
    return True

def main():
    """Validación general del entorno"""
    print("🌐 Validación de Entorno Big Data")
    
    checks = [
        validate_python_version(),
        validate_spark_installation(),
        validate_data_science_libraries()
    ]
    
    if all(checks):
        print("\n✨ Entorno validado exitosamente!")
        sys.exit(0)
    else:
        print("\n❌ Validación incompleta. Revise los errores.")
        sys.exit(1)

if __name__ == "__main__":
    main()