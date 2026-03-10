
## Estructura del Proyecto
data/raw/: Dataset original.

data/processed/: Dataset tras la limpieza.

notebooks/: Archivos .ipynb para el EDA.

src/: Scripts .py para limpieza y funciones modulares

## Análisis EDA 

# Predicción de Tarifas y Análisis de Transporte Urbano (Uber vs Lyft)

## Propósito del Proyecto
Este proyecto tiene como objetivo analizar y predecir el comportamiento de las tarifas de servicios de transporte compartido (Uber y Lyft) en la ciudad de Boston. A través de un enfoque de ingeniería de datos y Machine Learning, buscamos entender cómo factores externos (como el clima, la hora del día y la distancia) impactan dinámicamente en el precio final para el usuario.

## Selección de Datasets y Fuentes Externas
Para dotar al análisis de un valor real y profundo, no nos limitamos a un solo origen de datos. Se integraron dos datasets:
1. **Cab Rides Dataset (Kaggle):** Contiene el historial de viajes, tipos de servicio, origen, destino y precio.
2. **Weather Dataset (Externo/Adicional):** Historial climático por hora en los distintos barrios de la ciudad (temperatura, lluvia, viento).
*Justificación:* La integración del clima permite descubrir patrones de demanda inelástica (ej. cómo reacciona el precio ante la lluvia), aportando un valor analítico superior al de evaluar los viajes de forma aislada.

## Procesamiento de Datos (Pipeline ETL)
El dataset original requirió un tratamiento riguroso antes de su análisis:
1. **Limpieza de Nulos:** Se eliminaron registros sin precio (`NaN`) en el dataset de viajes, ya que esta es nuestra variable objetivo ($y$). Se imputaron valores de `0` en la columna de lluvia cuando no había precipitaciones.
2. **Transformación Temporal:** Se convirtieron los *timestamps* de formato Unix a objetos `datetime` manejables en Pandas, extrayendo características clave como la hora del día y el día de la semana.
3. **Merge (Unión):** Se unieron los datos de viajes y clima utilizando como llaves el `source` (origen del viaje) y la `hora` redondeada, creando un único dataset consolidado de cientos de miles de registros.

## Análisis Exploratorio de Datos (EDA) y Visualización
Se generaron visualizaciones estéticamente atractivas y funcionales utilizando diversas librerías:
* **Seaborn & Matplotlib:** Para entender la distribución de precios entre compañías y la matriz de correlación numérica.
* **Plotly:** Para gráficos interactivos de dispersión que permiten explorar la relación Precio vs Distancia por tipo de servicio.
* **Folium:** Se mapearon manualmente las coordenadas de los barrios de Boston para generar un **Mapa de Calor Geográfico**, revelando visualmente los focos de mayor demanda de transporte en la ciudad.


## Principales Hallazgos del análisis 


## Análisis de Precios (Uber vs Lyft)
-El diagrama de caja muestra que Lyft presenta una mediana de precios ligeramente superior a la de Uber y una mayor variabilidad en sus tarifas. Ambos servicios presentan valores atípicos con precios elevados.En general, Uber tiende a mantener una distribución de precios más concentrada.

## Matriz de Correlación (Impacto del clima y distancia)
-El análisis de correlación muestra que la distancia tiene la relación más fuerte con el precio del viaje (0.35), seguida del multiplicador de tarifa dinámica (0.24). Las demás variables como temperatura, lluvia y hora presentan correlaciones muy bajas, indicando que tienen una influencia limitada en el precio de los viajes dentro del conjunto de datos analizado.

## Relación Distancia vs Precio (Interactivo por Tipo de Servicio)

El gráfico muestra que el precio del viaje aumenta conforme crece la distancia recorrida. Sin embargo, el precio también varía dependiendo del tipo de servicio seleccionado, siendo los servicios premium los que presentan tarifas más elevadas. Además, la presencia de varios precios para distancias similares indica que factores adicionales como la demanda o la tarifa dinámica influyen en el costo final del viaje.

-----------------------------------------------------------------------------------------------------------------------------------------------

## Modelado Predictivo (Machine Learning)
Se implementó un modelo de Machine Learning utilizando `scikit-learn` para predecir la tarifa del viaje:
* **Algoritmo:** `Random Forest Regressor` (integrado dentro de un `Pipeline` para manejar automáticamente las variables categóricas con `OneHotEncoder`).
* **Features:** Distancia, Multiplicador de tarifa (Surge), Hora, Temperatura y Tipo de Servicio.
* **Rendimiento:** El modelo logró predecir con alta precisión el costo del viaje, demostrando que la distancia y el nivel del servicio son los predictores más fuertes.

## Principales Hallazgos
1. **Efecto Base y Premium:** Existe una clara segmentación de precios. Los servicios compartidos mantienen precios estables sin importar tanto la distancia, mientras que los servicios "Lux" o "Black" tienen una pendiente de costo por milla mucho más agresiva.
2. **Impacto Geográfico:** Zonas como *Financial District* y *Back Bay* concentran la mayor densidad de peticiones, lo que las convierte en áreas clave para la ubicación estratégica de conductores.
3. **Poder Predictivo:** El modelo confirma que, a pesar de la percepción de precios de estas apps, la tarifa sigue una estructura matemática altamente modelable si se tienen en cuenta el clima y la distancia.
