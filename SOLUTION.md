# Airbnb Data Engineering Pipeline

## Descripción  
Pipeline ETL para extraer, transformar y cargar datos de listings y reviews de Airbnb en una base de datos MySQL, implementando buenas prácticas como manejo de nulos, validaciones, Changing tipo 2 y control de integridad referencial.

---

## Diseño Dimensional

### 1. Grano de la tabla de hechos  
La tabla de hechos `fact_reviews` tiene como grano la review individual, es decir, cada fila representa una revisión específica de un listing en una fecha determinada. Esto permite análisis detallados a nivel de review, incluyendo frecuencia y relación con listings.

### 2. Diseño de dimensiones  
La dimensión principal es `dim_listings`, que incluye atributos descriptivos relevantes de las propiedades como nombre, host, vecindario, precio y clasificación de precio. Esta dimensión soporta consultas agregadas por ubicación, rangos de precio y host, facilitando análisis estratégicos.

### 3. Manejo de dimensiones de cambio lento (SCD)  
Se implementa un Slowly Changing Dimension tipo 2 en `dim_listings` mediante la clave primaria compuesta `(id, start_date)` y los campos auxiliares `end_date` y `current_flag`. Este diseño permite mantener el historial de cambios en las propiedades con control de vigencia, facilitando análisis temporales y comparativos fiables.

---

## Estrategia de Indexación y Partición

- **Indexación**  
  - Índice primario en `(id, start_date)` para la tabla `dim_listings` que soporta consultas históricas.  
  - Índices en las claves foráneas, como `listing_id` en `fact_reviews`, para acelerar joins y filtros.  

- **Partición**  
  - Aunque aún no implementado por volumen, se recomienda particionar tablas como `fact_reviews` por rango de fechas (ej. año o mes) para mejorar rendimiento y manejo.  
  - Esta decisión depende del crecimiento futuro y patrones de consulta.

---

## Compensaciones y Alternativas Consideradas

- Se decidió usar SCD tipo 2 para no perder historial vs. SCD tipo 1 que sobreescribe datos.  
- Se priorizaron índices sobre partición inicial para mantener simplicidad y rendimiento aceptable con volúmenes actuales.

---

## Estructura del Proyecto

- `src/pipeline/extract.py`: funciones para cargar archivos CSV.  
- `src/pipeline/transform.py`: funciones para limpiar y transformar datos.  
- `src/pipeline/validate.py`: funciones para validaciones de calidad.  
- `src/pipeline/load.py`: funciones para cargar datos en MySQL.  
- `src/pipeline/orchestrator.py`: script principal que orquesta el pipeline.  
- `utils/db_connector.py`: conexión a la base de datos con variables de entorno.  
- `data/`: carpeta con archivos `listings.csv` y `reviews.csv`.  
- `logs/`: carpeta donde se guardan los logs de ejecución.  
- `output/`: carpeta donde se guarda el reporte de calidad y archivos de datos inválidos.

---

## Requisitos

- Python 3.8+  
- Librerías: pandas, pymysql, python-dotenv  
- Base de datos MySQL(preferible) configurada con las tablas adecuadas (ver script `db_schema.sql`)  
- Archivo `.env` con las credenciales de la base de datos

---

## Configuración

1. Crear y configurar el archivo `.env` con estas variables:

DB_HOST=localhost
DB_PORT=3306
DB_USER=tu_usuario
DB_PASSWORD=contraseña
DB_NAME=airbnb_db


2. Crear las tablas ejecutando el script SQL en la base de datos (`db_schema.sql`).

---

## Ejecución

Desde la terminal, en el directorio raíz del proyecto, ejecutar:

python src/pipeline/orchestrator.py


El pipeline realizará la extracción, transformación, validación y carga, guardando logs en `logs/pipeline_execution.log`.

---

## Ajustes Finales y Validaciones Avanzadas

El pipeline incluye:

- Manejo de filas con campos críticos nulos.  
- Validaciones estrictas de unicidad, tipos y presencia de columnas.  
- Validación de integridad referencial entre reviews y listings.  
- Reemplazo seguro de valores nulos en fechas para evitar errores en MySQL.  
- Filtrado de reviews sin `listing_id` válido antes de carga.  
- Clasificación de precios en rangos (`price_tier`).  
- Indicadores de actualidad en reviews (`is_recent`).

---

## Reporte de Calidad de Datos (data_quality_report.json)

Se genera un reporte JSON que almacena un resumen estructurado de la calidad de datos tras las validaciones del pipeline, con métricas como:

- Número de valores nulos en campos críticos.  
- Conteo de IDs duplicados.  
- Cantidad de registros con precios fuera de rango.  
- Número de reviews inválidos filtrados antes de la carga.

Este archivo se guarda automáticamente en la carpeta `output/` con el nombre `data_quality_report.json` para auditoría y seguimiento histórico.

Se implementó una función que convierte tipos no nativos (como `numpy.int64`) a tipos nativos Python antes de almacenar en JSON para evitar errores de serialización.


---

## Ejecución de pruebas unitarias

Para garantizar la calidad y correcto funcionamiento del pipeline, se incluyen pruebas unitarias automatizadas escrita con pytest.

### Pasos para pruebas:

1. Instalar pytest si no está instalado:

pip install pytest


2. Asegurarse de que pytest esté listado en `requirements.txt`.

3. Estructura de pruebas en carpeta `tests/` con archivos:

- `test_extract.py`  
- `test_transform.py`  
- `test_validate.py`  
- `test_load.py`


4. Ejecutar todas las pruebas desde la raíz del proyecto con:

pytest


5. Interpretar resultados:  
- Pruebas exitosas se muestran con puntos (“.`”).  
- Fallos se muestran con detalles para facilitar corrección.

---

## Orquestación y despliegue en Docker Compose (con Airflow)

Inicializa la base de Airflow:

1. Inicializar la base de datos de Airflow
Antes de iniciar Airflow, es necesario inicializar su base interna de metadatos. Para ello, ejecuta:

docker-compose run --rm airflow-init

2. Levantar los servicios principales
Con la base de datos inicializada, levanta simultáneamente los servicios de Airflow, MySQL y el pipeline con:

docker-compose up -d mysql-db airflow airflow-scheduler pipeline

Esto inicia el servidor web de Airflow, la base de datos MySQL y el contenedor que ejecuta el pipeline.

3. Acceder a la interfaz web de Airflow

Una vez levantados los servicios, abre tu navegador y visita:

http://localhost:8080/

Esta URL muestra el dashboard web de Airflow, donde podrás visualizar y administrar tus DAGs o flujos de trabajo.

---

## Posibles mejoras en ambientes prod de gran volumen

- Generar reportes periódicos de métricas de calidad.  
- Automatización del pipeline con Airflow o cron jobs.  
- Escalabilidad para nuevos datasets o columnas.

---

## Contacto  
Consulta y soporte: Jhon Caldas

