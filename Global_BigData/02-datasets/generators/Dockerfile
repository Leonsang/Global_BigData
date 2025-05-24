# Dockerfile para Generador de Datos de Transporte
FROM python:3.9-slim

WORKDIR /app

# Instalar dependencias
RUN pip install --no-cache-dir \
    pandas \
    numpy \
    requests \
    hdfs[avro,kerberos] \
    python-dateutil \
    faker

# Copiar script generador
COPY transport_data_generator.py .
COPY generate_schemas.py .

# Variables de ambiente
ENV HDFS_NAMENODE=hdfs://namenode:9000
ENV GENERATION_INTERVAL=30
ENV TOTAL_ROUTES=50
ENV DISTRICTS=15

# Ejecutar generador
CMD ["python", "transport_data_generator.py"]