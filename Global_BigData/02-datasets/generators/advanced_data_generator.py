#!/usr/bin/env python3
"""
🚌 GENERADOR DE DATOS COMPLETO - 7 SESIONES
Genera datos para HDFS (batch) y Kafka (streaming)

Características expandidas:
- Datos históricos para HDFS (Sesiones 1-3)
- Streaming en tiempo real para Kafka (Sesión 4)
- Múltiples tipos de eventos (GPS, pagos, alertas)
- Patrones realistas de demanda y tráfico
"""

import json
import time
import os
import random
from datetime import datetime, timedelta
from hdfs import InsecureClient
from kafka import KafkaProducer
import pandas as pd
import numpy as np
from faker import Faker

fake = Faker('es_PE')

class AdvancedTransportDataGenerator:
    def __init__(self):
        self.hdfs_client = None
        self.kafka_producer = None
        
        # Configuración expandida
        self.districts = [
            "Lima Centro", "Miraflores", "San Isidro", "Barranco", 
            "Surco", "San Borja", "La Molina", "Pueblo Libre",
            "Jesus Maria", "Magdalena", "San Miguel", "Callao",
            "Villa El Salvador", "Villa Maria", "Los Olivos"
        ]
        
        self.route_types = ["Metropolitano", "Corredor", "Regular", "Express"]
        self.companies = ["Protransporte", "Lima Bus", "Orion", "Etusa", "Coaster"]
        
        # Patrones de demanda más realistas
        self.demand_patterns = {
            0: 0.1, 1: 0.05, 2: 0.05, 3: 0.05, 4: 0.1, 5: 0.2,
            6: 0.4, 7: 0.8, 8: 1.0, 9: 0.7, 10: 0.5, 11: 0.4,
            12: 0.6, 13: 0.8, 14: 0.6, 15: 0.5, 16: 0.4, 17: 0.7,
            18: 1.0, 19: 0.9, 20: 0.6, 21: 0.4, 22: 0.3, 23: 0.2
        }
        
        # Eventos para streaming
        self.event_types = ["trip_start", "trip_end", "gps_update", "payment", "alert"]
        
    def connect_services(self):
        """Conectar a HDFS y Kafka"""
        success = True
        
        # Conectar HDFS
        try:
            namenode_url = os.getenv('HDFS_NAMENODE', 'http://namenode:9870')
            self.hdfs_client = InsecureClient(namenode_url)
            print(f"✅ HDFS conectado: {namenode_url}")
            
            # Crear estructura completa de directorios
            directories = [
                '/transport_data/historical',
                '/transport_data/streaming', 
                '/transport_data/master',
                '/transport_data/weather',
                '/transport_data/processed'
            ]
            
            for directory in directories:
                self.hdfs_client.makedirs(directory, permission=755)
                
        except Exception as e:
            print(f"❌ Error conectando HDFS: {e}")
            success = False
            
        # Conectar Kafka
        try:
            bootstrap_servers = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 
                                        'kafka-1:29092,kafka-2:29093').split(',')
            
            self.kafka_producer = KafkaProducer(
                bootstrap_servers=bootstrap_servers,
                value_serializer=lambda v: json.dumps(v, ensure_ascii=False).encode('utf-8'),
                key_serializer=lambda k: str(k).encode('utf-8'),
                retries=5,
                batch_size=16384,
                linger_ms=100,
                buffer_memory=33554432
            )
            print(f"✅ Kafka conectado: {bootstrap_servers}")
            
        except Exception as e:
            print(f"❌ Error conectando Kafka: {e}")
            success = False
            
        return success