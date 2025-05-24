#!/usr/bin/env python3
"""
🚌 GENERADOR DE DATOS DE TRANSPORTE REALISTA
Simula datos de transporte público de Lima para aprendizaje Big Data

Características:
- Datos realistas de rutas, distritos, horarios
- Patrones de demanda por hora del día
- Delays realistas basados en tráfico
- Generación continua para streaming
"""

import pandas as pd
import numpy as np
import json
import time
import os
from datetime import datetime, timedelta
from hdfs import InsecureClient
import random
from faker import Faker

fake = Faker('es_PE')  # Configurar para Perú

class TransportDataGenerator:
    def __init__(self):
        self.hdfs_client = None
        self.districts = [
            "Lima Centro", "Miraflores", "San Isidro", "Barranco", 
            "Surco", "San Borja", "La Molina", "Pueblo Libre",
            "Jesus Maria", "Magdalena", "San Miguel", "Callao",
            "Villa El Salvador", "Villa Maria", "Los Olivos"
        ]
        
        self.route_types = ["Metropolitano", "Corredor", "Regular", "Express"]
        self.companies = ["Protransporte", "Lima Bus", "Orion", "Etusa"]
        
        # Patrones realistas por hora
        self.demand_patterns = {
            6: 0.3, 7: 0.8, 8: 1.0, 9: 0.7, 10: 0.5,
            11: 0.4, 12: 0.6, 13: 0.8, 14: 0.6, 15: 0.5,
            16: 0.4, 17: 0.7, 18: 1.0, 19: 0.9, 20: 0.6,
            21: 0.4, 22: 0.3, 23: 0.2
        }
        
    def connect_hdfs(self):
        """Conectar a HDFS"""
        try:
            namenode_url = os.getenv('HDFS_NAMENODE', 'http://namenode:9870')
            self.hdfs_client = InsecureClient(namenode_url)
            print(f"✅ Conectado a HDFS: {namenode_url}")
            
            # Crear directorios base
            self.hdfs_client.makedirs('/transport_data/historical', permission=755)
            self.hdfs_client.makedirs('/transport_data/streaming', permission=755)
            
        except Exception as e:
            print(f"❌ Error conectando HDFS: {e}")
            return False
        return True    
    def generate_route_data(self):
        """Generar datos maestros de rutas"""
        routes = []
        total_routes = int(os.getenv('TOTAL_ROUTES', 50))
        
        for i in range(1, total_routes + 1):
            route = {
                'route_id': f'R{i:03d}',
                'route_name': f'Ruta {i} - {fake.street_name()}',
                'route_type': random.choice(self.route_types),
                'company': random.choice(self.companies),
                'origin_district': random.choice(self.districts),
                'destination_district': random.choice(self.districts),
                'distance_km': round(random.uniform(5.0, 25.0), 1),
                'average_duration_minutes': random.randint(20, 90),
                'fare_soles': round(random.uniform(1.50, 4.50), 2),
                'capacity_passengers': random.choice([40, 60, 80, 100, 120]),
                'operates_weekends': random.choice([True, False]),
                'peak_frequency_minutes': random.randint(3, 8),
                'off_peak_frequency_minutes': random.randint(8, 15)
            }
            routes.append(route)
        
        return routes
    
    def generate_trip_data(self, routes, date_str, hour):
        """Generar datos de viajes para una hora específica"""
        trips = []
        demand_factor = self.demand_patterns.get(hour, 0.3)
        
        for route in routes:
            # Número de viajes basado en demanda y frecuencia
            if 6 <= hour <= 22:  # Horario operativo
                frequency = route['peak_frequency_minutes'] if demand_factor > 0.6 else route['off_peak_frequency_minutes']
                trips_per_hour = 60 // frequency
                trips_per_hour = int(trips_per_hour * demand_factor)
            else:
                trips_per_hour = 0
            
            for trip_num in range(trips_per_hour):
                # Calcular tiempo del viaje
                minute = random.randint(0, 59)
                trip_time = f"{date_str} {hour:02d}:{minute:02d}:00"
                
                # Generar retraso realista
                base_delay = random.uniform(0, 3)  # Retraso base
                if 7 <= hour <= 9 or 17 <= hour <= 19:  # Horas pico
                    traffic_delay = random.uniform(0, 15)
                else:
                    traffic_delay = random.uniform(0, 5)
                
                total_delay = base_delay + traffic_delay
                
                # Ocupación basada en demanda
                max_capacity = route['capacity_passengers']
                occupancy_rate = random.uniform(0.3, 1.0) * demand_factor
                passengers = int(max_capacity * occupancy_rate)
                
                trip = {
                    'trip_id': f"T{date_str.replace('-','')}{hour:02d}{minute:02d}{trip_num:02d}",
                    'route_id': route['route_id'],
                    'date': date_str,
                    'scheduled_time': trip_time,
                    'actual_time': trip_time,  # Simplificado para este ejemplo
                    'delay_minutes': round(total_delay, 1),
                    'passengers_on_board': passengers,
                    'occupancy_rate': round(occupancy_rate, 2),
                    'fare_collected_soles': round(passengers * route['fare_soles'], 2),
                    'district_origin': route['origin_district'],
                    'district_destination': route['destination_district'],
                    'driver_id': f"D{random.randint(1000, 9999)}",
                    'bus_plate': fake.license_plate(),
                    'weather_condition': random.choice(['Sunny', 'Cloudy', 'Light Rain', 'Heavy Rain']),
                    'day_of_week': datetime.strptime(date_str, '%Y-%m-%d').strftime('%A')
                }
                
                trips.append(trip)
        
        return trips    
    def save_to_hdfs(self, data, file_path):
        """Guardar datos en HDFS"""
        try:
            json_data = json.dumps(data, indent=2, ensure_ascii=False)
            with self.hdfs_client.write(file_path, encoding='utf-8') as writer:
                writer.write(json_data)
            print(f"✅ Guardado: {file_path}")
            return True
        except Exception as e:
            print(f"❌ Error guardando {file_path}: {e}")
            return False
    
    def generate_historical_data(self, days=30):
        """Generar datos históricos para entrenar modelos"""
        print(f"🔄 Generando {days} días de datos históricos...")
        
        routes = self.generate_route_data()
        
        # Guardar datos maestros de rutas
        self.save_to_hdfs(routes, '/transport_data/master/routes.json')
        
        # Generar datos por día
        start_date = datetime.now() - timedelta(days=days)
        
        for day in range(days):
            current_date = start_date + timedelta(days=day)
            date_str = current_date.strftime('%Y-%m-%d')
            
            day_trips = []
            
            # Generar viajes por hora
            for hour in range(6, 23):  # Horario operativo 6AM-10PM
                hour_trips = self.generate_trip_data(routes, date_str, hour)
                day_trips.extend(hour_trips)
            
            # Guardar por día y particionado por distrito
            day_path = f'/transport_data/historical/date={date_str}'
            
            # Particionar por distrito de origen
            district_groups = {}
            for trip in day_trips:
                district = trip['district_origin'].replace(' ', '_')
                if district not in district_groups:
                    district_groups[district] = []
                district_groups[district].append(trip)
            
            for district, trips in district_groups.items():
                file_path = f'{day_path}/district={district}/trips_{date_str}_{district}.json'
                self.save_to_hdfs(trips, file_path)
        
        print(f"✅ Datos históricos generados: {days} días")
    
    def generate_streaming_data(self):
        """Generar datos en tiempo real para streaming"""
        print("🔄 Iniciando generación de datos en tiempo real...")
        
        routes = self.generate_route_data()
        interval = int(os.getenv('GENERATION_INTERVAL', 30))
        
        while True:
            try:
                current_time = datetime.now()
                date_str = current_time.strftime('%Y-%m-%d')
                hour = current_time.hour
                
                # Generar viajes para la hora actual
                trips = self.generate_trip_data(routes, date_str, hour)
                
                if trips:  # Solo si hay viajes en este horario
                    timestamp = current_time.strftime('%Y%m%d_%H%M%S')
                    file_path = f'/transport_data/streaming/trips_{timestamp}.json'
                    self.save_to_hdfs(trips, file_path)
                    print(f"📊 Generados {len(trips)} viajes para {current_time.strftime('%H:%M')}")
                
                time.sleep(interval)
                
            except KeyboardInterrupt:
                print("⏹️  Deteniendo generador...")
                break
            except Exception as e:
                print(f"❌ Error en streaming: {e}")
                time.sleep(5)

def main():
    """Función principal"""
    generator = TransportDataGenerator()
    
    print("🚌 GENERADOR DE DATOS DE TRANSPORTE")
    print("==================================")
    
    # Conectar a HDFS
    if not generator.connect_hdfs():
        print("❌ No se pudo conectar a HDFS. Saliendo...")
        return
    
    # Determinar modo de operación
    mode = os.getenv('GENERATION_MODE', 'both')
    
    if mode in ['historical', 'both']:
        # Generar datos históricos
        historical_days = int(os.getenv('HISTORICAL_DAYS', 30))
        generator.generate_historical_data(historical_days)
    
    if mode in ['streaming', 'both']:
        # Esperar un poco si acabamos de generar históricos
        if mode == 'both':
            print("⏳ Esperando 30 segundos antes de iniciar streaming...")
            time.sleep(30)
        
        # Generar datos en tiempo real
        generator.generate_streaming_data()

if __name__ == "__main__":
    main()