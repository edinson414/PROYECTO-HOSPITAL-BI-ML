# Hospital BI ML

Proyecto end-to-end de Business Intelligence y Machine Learning para analisis hospitalario, con un ETL en Python que prepara datos para Power BI y un modelo de estrella en SQL Server.

## Tabla de Contenidos

- [Descripcion](#descripcion)
- [Configuracion del Entorno](#configuracion-del-entorno)
- [Pipeline ETL](#pipeline-etl)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Uso](#uso)
- [Solucion de Problemas](#solucion-de-problemas)
- [Recursos Adicionales](#recursos-adicionales)
- [Autor](#autor)
- [Licencia](#licencia)

## Descripcion

Este proyecto extrae datos desde la base transaccional `Hospital`, los transforma con Python, los carga en `DW_Hospital` y exporta un CSV listo para Power BI.

- Extrae pacientes, medicos, consultas, recetas y tablas relacionadas.
- Limpia valores nulos y calcula campos derivados como la edad.
- Carga dimensiones y hechos en el Data Warehouse.
- Genera `data/processed/Data_Hospital_BI.csv` para analisis en Power BI.

## Configuracion del Entorno

### Requisitos previos

- Python 3.10 o superior.
- SQL Server 2019 o superior.
- ODBC Driver 17 for SQL Server.
- Archivo `.env` en la raiz del proyecto.

### Variables de entorno

```env
DB_SERVER=EDINSON\EDINSONMSSS19PC
DB_DRIVER=ODBC Driver 17 for SQL Server
DB_USER=
DB_PASSWORD=
DB_TRANSACTIONAL=Hospital
DB_DATAWAREHOUSE=DW_Hospital
ENVIRONMENT=development
```

### Instalacion

```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Pipeline ETL

### Flujo general

```text
Hospital (OLTP) -> ETL en Python -> DW_Hospital -> Power BI
```

### Verificar conexion

```bash
python src/etl/python/test_connection.py
```

### Ejecutar el ETL completo

```bash
python run_etl.py
```

El proceso realiza estas etapas:

1. Extrae datos desde `Hospital`.
2. Transforma y limpia la informacion.
3. Carga el modelo de estrella en `DW_Hospital`.
4. Exporta el archivo `data/processed/Data_Hospital_BI.csv`.

## Estructura del Proyecto

La estructura del proyecto sigue el estandar de ciencia de datos:

```text
hospital_bi_ml/
├── LICENSE                     <- Licencia de codigo abierto
├── Makefile                    <- Comandos utiles como `make data` o `make train`
├── README.md                   <- Este archivo, guia para desarrolladores
├── pyproject.toml              <- Configuracion del proyecto y metadatos
├── requirements.txt            <- Dependencias de Python
├── setup.cfg                   <- Configuracion para flake8
├── .env                        <- Variables de entorno (no subir a Git)
│
├── data                        <- Datos en todas las etapas del proyecto
│   ├── raw/                    <- Datos originales e inmutables
│   │   ├── HOSPITAL BIG DATA.sql
│   │   └── Insert/             <- Scripts para insertar datos
│   ├── interim/                <- Datos intermedios transformados
│   ├── processed/              <- Datos finales listos para modelado
│   │   └── Data_Hospital_BI.csv
│   └── external/               <- Datos de terceros
│
├── docs                        <- Documentacion del proyecto (mkdocs)
│   ├── mkdocs.yml
│   └── docs/
│       ├── index.md
│       └── getting-started.md
│
├── models                      <- Modelos entrenados, predicciones, resumenes
│
├── notebooks                   <- Jupyter notebooks para exploracion
│                                 (Convencion: numero-iniciales-descripcion)
│
├── references                  <- Diccionarios de datos, manuales, materiales
│
├── reports                     <- Analisis generado (HTML, PDF, LaTeX)
│   └── figures/                <- Graficos y figuras para reportes
│
├── run_etl.py                  <- Punto de entrada principal del pipeline
│
└── src                         <- Codigo fuente principal del proyecto
    │
    ├── __init__.py             <- Hace de hospital_bi_ml un modulo de Python
    ├── config.py               <- Variables y configuracion centralizada
    ├── dataset.py              <- Scripts para descargar o generar datos
    ├── features.py             <- Codigo para crear features para modelado
    ├── plots.py                <- Codigo para crear visualizaciones
    │
    ├── etl/                    <- Pipeline ETL del proyecto
    │   ├── __init__.py
    │   └── python/
    │       ├── __init__.py
    │       ├── etl_pipeline.py <- Clase principal del ETL
    │       ├── test_connection.py <- Verifica conexion a SQL Server
    │       └── ETL_README.md   <- Documentacion especifica del ETL
    │
    └── modeling/               <- Modelos de Machine Learning
        ├── __init__.py
        ├── train.py            <- Codigo para entrenar modelos
        └── predict.py          <- Codigo para inferencia con modelos
```

### Proposito de cada directorio

**`data/`**: Almacena datos en diferentes etapas:

- `raw/`: Scripts SQL originales para crear esquema e insertar datos.
- `interim/`: Datos transformados pero aun no listos para uso final.
- `processed/`: Datos finales y limpios, exportados a CSV para Power BI.
- `external/`: Datos de fuentes externas si es necesario.

**`src/`**: Codigo principal del proyecto:

- `config.py`: Centralizacion de variables y configuracion de bases de datos.
- `dataset.py`: Utilidades para preparacion de datos.
- `features.py`: Ingenieria de features para modelos ML.
- `plots.py`: Funciones para visualizaciones.
- `etl/`: Pipeline ETL con extraccion, transformacion y carga.
- `modeling/`: Entrenamientohe inferencia de modelos.

**`docs/`**: Documentacion del proyecto en formato mkdocs.

**`notebooks/`**: Jupyter notebooks para exploracion interactiva de datos.

**`models/`**: Modelos entrenados y serializados.

**`reports/`**: Reportes generados y figuras.

**`references/`**: Diccionarios de datos y documentacion externa.

### Archivos importantes

- `run_etl.py`: Ejecuta el pipeline ETL completo. Punto de entrada principal.
- `requirements.txt`: Lista de dependencias Python. Generar con `pip freeze > requirements.txt`.
- `.env`: Configuracion sensible (servidor, usuario, contraseña). Nunca subir a Git.
- `pyproject.toml`: Metadatos del proyecto y configuracion de herramientas.
- `setup.cfg`: Configuracion para linters como flake8.

### Uso de la estructura

Para trabajar en este proyecto:

1. **Crear datos**: Ejecuta scripts en `data/raw/` para inicializar las bases de datos.
2. **Ejecutar ETL**: Corre `python run_etl.py` desde la raiz del proyecto.
3. **Explorar datos**: Abre notebooks en `notebooks/` para EDA y analisis.
4. **Entrenar modelos**: Usa `src/modeling/train.py` para ML.
5. **Generar reportes**: Crea visualizaciones en `reports/figures/`.

## Uso

### Importar en Power BI

1. Abre Power BI Desktop.
2. Selecciona Obtener datos > Texto/CSV.
3. Elige `data/processed/Data_Hospital_BI.csv`.
4. Carga el archivo.

### Desarrollo local

```bash
python run_etl.py
python src/etl/python/test_connection.py
```

## Solucion de Problemas

### Error: falta pyodbc

```bash
pip install pyodbc
```

### Error: no conecta a SQL Server

- Verifica que SQL Server este ejecutandose.
- Confirma el servidor `EDINSON\EDINSONMSSS19PC`.
- Revisa el archivo `.env`.

### Error: no existe la tabla

- Ejecuta primero `data/raw/HOSPITAL BIG DATA.sql`.
- Luego ejecuta los scripts de `data/raw/Insert/`.

## Recursos Adicionales

- [Documentacion de SQL Server](https://learn.microsoft.com/sql/sql-server/)
- [Documentacion de pandas](https://pandas.pydata.org/docs/)
- [Documentacion de Power BI](https://learn.microsoft.com/power-bi/)

## Autor

Edinson Saldarriaga

## Licencia

Ver archivo [LICENSE](LICENSE) para mas detalles.
