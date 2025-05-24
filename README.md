# 🌐 Escuela Global - Proyecto Big Data

## 📋 Descripción
Este repositorio contiene el material y recursos para el curso de Big Data de Escuela Global. El proyecto está diseñado para proporcionar una experiencia práctica y realista con tecnologías Big Data, simulando problemas y herramientas de producción.

## 🚀 Comenzando

### Requisitos Previos
- Git instalado en tu sistema
- Cuenta de GitHub
- Docker Desktop (para las prácticas)
- Python 3.9 o superior

### Instalación

1. **Fork del Repositorio**
   - Ve a [https://github.com/Leonsang/Global_BigData](https://github.com/Leonsang/Global_BigData)
   - Haz clic en "Fork" en la esquina superior derecha

2. **Clonar tu Fork**
   ```bash
   git clone https://github.com/TU_USUARIO/Global_BigData.git
   cd Global_BigData
   ```

3. **Configurar el Repositorio**
   ```bash
   git remote add upstream https://github.com/Leonsang/Global_BigData.git
   ```

### Guía Detallada
Para una guía completa sobre cómo trabajar con este repositorio, consulta:
[Guía de Git para el Proyecto](Global_BigData/04-cheatsheets/git_workflow_guide.md)

## 📚 Estructura del Proyecto

```
Global_BigData/
├── 📁 00-setup/                    # Scripts de configuración
├── 📁 01-sessions/                 # Material por sesión
├── 📁 02-datasets/                 # Datos del proyecto
├── 📁 03-environments/             # Configuraciones ambiente
├── 📁 04-cheatsheets/              # Referencias rápidas
├── 📁 05-monitoring/               # Herramientas monitoreo
├── 📁 06-solutions/                # Soluciones ejercicios
└── 📁 07-presentations/            # Presentaciones del curso
```

## 🎯 Objetivos del Curso

- Aprender tecnologías Big Data en un ambiente realista
- Trabajar con datos reales de transporte público
- Simular problemas de producción
- Usar herramientas profesionales (Docker, HDFS, Spark, Kafka)
- Seguir una metodología hands-on (70% práctica, 30% teoría)

## 🛠️ Stack Tecnológico

- **Almacenamiento**: Hadoop HDFS 3.2.1
- **Procesamiento**: Apache Spark 3.4.0, Hadoop MapReduce 3.2.1
- **Event Streaming**: Apache Kafka 3.4.0
- **Orquestación**: Docker 20.10+, Docker Compose
- **Desarrollo**: Jupyter Lab, Python 3.9, Pandas/NumPy
- **Monitoreo**: Portainer, Hadoop Web UIs, Spark Web UI

## 📊 Datos del Proyecto

El proyecto utiliza datos realistas de transporte público de Lima:
- 30 días de datos históricos
- ~100,000 viajes
- 50 rutas diferentes
- 15 distritos de Lima
- Formato JSON particionado por fecha/distrito

## 🤝 Contribución

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📞 Soporte

Si tienes problemas o dudas:
1. Revisa la documentación en la carpeta `04-cheatsheets/`
2. Consulta los archivos de troubleshooting en `00-setup/docs/`
3. Pregunta en el canal de Discord del curso

## 📝 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

---

**¡Bienvenido al mundo del Big Data!** 🚀 