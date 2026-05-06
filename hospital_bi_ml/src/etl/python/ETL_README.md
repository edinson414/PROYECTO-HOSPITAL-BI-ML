# ETL Pipeline - Hospital BI ML

## Descripción

Este documento resume cómo funciona el ETL en Python que toma datos de la base transaccional de SQL Server, los limpia, los carga en el Data Warehouse y genera el CSV listo para Power BI.

## Arquitectura

```text
Hospital (OLTP) → ETL en Python → DW_Hospital (Star Schema) → Power BI
  - Pacientes       - Extracción      - Dim_Pacientes        - Importar CSV
  - Médicos         - Transformación  - Dim_Médicos
  - Consultas       - Carga           - Dim_Diagnósticos
  - Recetas         - Exportación     - Fact_Consultas
```

## Configuración

### 1. Configurar el archivo `.env`

Edita el archivo `.env` de la raíz del proyecto con tus datos de SQL Server:

```env
DB_SERVER=EDINSON\EDINSONMSSS19PC
DB_DRIVER=ODBC Driver 17 for SQL Server
DB_USER=
DB_PASSWORD=
DB_TRANSACTIONAL=Hospital
DB_DATAWAREHOUSE=DW_Hospital
ENVIRONMENT=development
```

Si usas autenticación de Windows, deja `DB_USER` y `DB_PASSWORD` vacíos.

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

## Uso

### Verificar conexión a SQL Server

Antes de ejecutar el ETL, confirma que la conexión funciona:

```bash
python src/etl/python/test_connection.py
```

Salida esperada:

```text
✓ Connected successfully to Hospital
✓ Connected successfully to DW_Hospital
✓ ALL TESTS PASSED - Ready to run ETL pipeline!
```

### Ejecutar el ETL completo

```bash
python run_etl.py
```

El proceso hace lo siguiente:

1. Extrae tablas de `Hospital`.
2. Limpia y transforma los datos.
3. Carga dimensiones y hechos en `DW_Hospital`.
4. Exporta `data/processed/Data_Hospital_BI.csv`.

## Detalle de pasos

### 1. Extracción

- Se conecta a `Hospital`.
- Extrae tablas como Pacientes, Médicos, Consultas, Recetas y Medicamentos.

### 2. Transformación

- Pacientes: elimina nulos críticos, limpia teléfono y correo, calcula edad.
- Consultas: cruza con Pacientes y Médicos.
- Recetas: valida y limpia los datos relacionados.

### 3. Carga

- Inserta datos en las dimensiones del Data Warehouse.
- Si una tabla no permite `TRUNCATE`, usa `DELETE` como alternativa.

### 4. Exportación para Power BI

- Construye la tabla maestra final.
- La exporta con codificación UTF-8.
- El archivo final queda en `data/processed/Data_Hospital_BI.csv`.

## Integración con Power BI

1. Abre Power BI Desktop.
2. Selecciona Obtener datos > Texto/CSV.
3. Elige `data/processed/Data_Hospital_BI.csv`.
4. Carga el archivo.

## Solución de problemas

### Error: falta `pyodbc`

```bash
pip install pyodbc
```

### Error: no conecta a SQL Server

- Verifica que SQL Server esté ejecutándose.
- Confirma el servidor `EDINSON\EDINSONMSSS19PC`.
- Revisa el archivo `.env`.

### Error: la tabla no existe

- Ejecuta primero `data/raw/HOSPITAL BIG DATA.sql`.
- Luego ejecuta los scripts de `data/raw/Insert/`.

### Verificar datos extraídos

```bash
python -c "
from src.etl.python.etl_pipeline import ETLPipeline

pipeline = ETLPipeline()
pipeline.extract_from_transactional()
print(pipeline.dataframes['pacientes'].head())
"
```

## Siguientes pasos

- Configurar `.env`.
- Ejecutar `test_connection.py`.
- Ejecutar `run_etl.py`.
- Importar `Data_Hospital_BI.csv` en Power BI.
- Crear el dashboard final.
