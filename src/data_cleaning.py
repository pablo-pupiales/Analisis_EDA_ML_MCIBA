import pandas as pd
import os

def limpiar_y_unir_datos():
    print("Iniciando pipeline ETL...")
    
    # 1. Carga de datos (ajusta la ruta según desde dónde ejecutes el script)
    # Asumimos que ejecutas desde la raíz del proyecto
    cab_rides = pd.read_csv('data/raw/cab_rides.csv')
    weather = pd.read_csv('data/raw/weather.csv')
    
    print(f"Viajes iniciales: {len(cab_rides)} | Registros de clima iniciales: {len(weather)}")

    # ==========================================
    # 2. LIMPIEZA DE VIAJES (CAB RIDES)
    # ==========================================
    # Existen alrededor de 55,000 filas sin precio. Como queremos predecirlo, las eliminamos.
    cab_rides.dropna(subset=['price'], inplace=True)

    # El timestamp de los viajes está en milisegundos. Lo pasamos a formato fecha/hora legible
    cab_rides['datetime'] = pd.to_datetime(cab_rides['time_stamp'], unit='ms')

    # Extraemos características útiles para el análisis (Ingeniería de Características)
    cab_rides['date_hour'] = cab_rides['datetime'].dt.floor('H') # Redondea a la hora (ej: 14:35 -> 14:00)
    cab_rides['hour'] = cab_rides['datetime'].dt.hour
    cab_rides['day_of_week'] = cab_rides['datetime'].dt.dayofweek # 0=Lunes, 6=Domingo
    cab_rides['is_weekend'] = cab_rides['day_of_week'].apply(lambda x: 1 if x >= 5 else 0)

    # ==========================================
    # 3. LIMPIEZA DE CLIMA (WEATHER)
    # ==========================================
    # Si 'rain' es nulo, significa que no llovió, así que lo rellenamos con 0
    weather['rain'] = weather['rain'].fillna(0)

    # El timestamp del clima está en segundos.
    weather['datetime'] = pd.to_datetime(weather['time_stamp'], unit='s')
    weather['date_hour'] = weather['datetime'].dt.floor('H')

    # Puede haber múltiples registros de clima en una misma hora. Los promediamos para evitar duplicados en el merge.
    weather_grouped = weather.groupby(['location', 'date_hour']).agg({
        'temp': 'mean',
        'clouds': 'mean',
        'pressure': 'mean',
        'rain': 'mean',
        'humidity': 'mean',
        'wind': 'mean'
    }).reset_index()

    # ==========================================
    # 4. MERGE (UNIÓN DE DATASETS)
    # ==========================================
    # Unimos los viajes con el clima según el lugar de origen (source) y la hora
    merged_df = pd.merge(
        cab_rides, 
        weather_grouped, 
        left_on=['source', 'date_hour'], 
        right_on=['location', 'date_hour'], 
        how='inner'
    )
    
    # Eliminamos columnas redundantes
    merged_df.drop(columns=['time_stamp', 'id', 'location'], inplace=True)

    print(f"Dimensión después de la limpieza y merge: {merged_df.shape}")
    
    # 5. Guardar el dataset procesado
    # Asegurarnos de que la carpeta existe
    os.makedirs('data/processed', exist_ok=True)
    
    output_path = 'data/processed/uber_lyft_cleaned.csv'
    merged_df.to_csv(output_path, index=False)
    
    print(f"¡Éxito! Dataset limpio y listo para analizar guardado en: {output_path}")

if __name__ == "__main__":
    limpiar_y_unir_datos()