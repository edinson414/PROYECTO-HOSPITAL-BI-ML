# hospital_bi_ml

<a target="_blank" href="https://cookiecutter-data-science.drivendata.org/">
    <img src="https://img.shields.io/badge/CCDS-Project%20template-328F97?logo=cookiecutter" />
</a>

Proyecto End-to-End de BI y Machine Learning para análisis hospitalario y predicción de inasistencias.

## Configuración del Entorno Virtual / Virtual Environment Setup

### Requisitos previos / Prerequisites
- Python 3.10

### Pasos / Steps

1. **Crear el entorno virtual** (desde la carpeta `hospital_bi_ml/`):
   ```bash
   make create_environment
   ```
   Esto crea una carpeta `.venv` con el entorno aislado.

2. **Activar el entorno virtual**:
   - Linux / macOS:
     ```bash
     source .venv/bin/activate
     ```
   - Windows:
     ```bat
     .venv\Scripts\activate
     ```

3. **Instalar las dependencias**:
   ```bash
   make requirements
   ```

4. **Configurar variables de entorno** (opcional):
   ```bash
   cp .env.example .env
   # Edita .env con tus valores
   ```

5. **Desactivar el entorno** cuando termines:
   ```bash
   deactivate
   ```

## Project Organization

```
├── LICENSE            <- Open-source license if one is chosen
├── Makefile           <- Makefile with convenience commands like `make data` or `make train`
├── README.md          <- The top-level README for developers using this project.
├── data
│   ├── external       <- Data from third party sources.
│   ├── interim        <- Intermediate data that has been transformed.
│   ├── processed      <- The final, canonical data sets for modeling.
│   └── raw            <- The original, immutable data dump.
│
├── docs               <- A default mkdocs project; see www.mkdocs.org for details
│
├── models             <- Trained and serialized models, model predictions, or model summaries
│
├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
│                         the creator's initials, and a short `-` delimited description, e.g.
│                         `1.0-jqp-initial-data-exploration`.
│
├── pyproject.toml     <- Project configuration file with package metadata for 
│                         hospital_bi_ml and configuration for tools like black
│
├── references         <- Data dictionaries, manuals, and all other explanatory materials.
│
├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
│   └── figures        <- Generated graphics and figures to be used in reporting
│
├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
│                         generated with `pip freeze > requirements.txt`
│
├── setup.cfg          <- Configuration file for flake8
│
└── hospital_bi_ml   <- Source code for use in this project.
    │
    ├── __init__.py             <- Makes hospital_bi_ml a Python module
    │
    ├── config.py               <- Store useful variables and configuration
    │
    ├── dataset.py              <- Scripts to download or generate data
    │
    ├── features.py             <- Code to create features for modeling
    │
    ├── modeling                
    │   ├── __init__.py 
    │   ├── predict.py          <- Code to run model inference with trained models          
    │   └── train.py            <- Code to train models
    │
    └── plots.py                <- Code to create visualizations
```

--------

