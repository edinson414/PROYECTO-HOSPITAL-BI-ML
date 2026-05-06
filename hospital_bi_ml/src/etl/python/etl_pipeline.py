"""
ETL Pipeline: Extract from HospitalBigData → Transform → Load to DW_Hospital
Prepara datos limpios para Power BI importando desde SQL Server
"""

import os
import pandas as pd
import pyodbc
from datetime import datetime
from pathlib import Path
from loguru import logger

# Import config
from hospital_bi_ml.config import (
    DB_SERVER,
    DB_DRIVER,
    DB_USER,
    DB_PASSWORD,
    DB_TRANSACTIONAL,
    DB_DATAWAREHOUSE,
    PROCESSED_DATA_DIR,
)


class SQLServerConnection:
    """Manage connection to SQL Server databases."""

    def __init__(self, server: str, database: str, driver: str, user: str = "", password: str = ""):
        """
        Initialize SQL Server connection.
        
        Args:
            server: SQL Server instance name
            database: Database name
            driver: ODBC driver name
            user: Username (optional for Windows auth)
            password: Password (optional for Windows auth)
        """
        self.server = server
        self.database = database
        self.driver = driver
        self.user = user
        self.password = password
        self.connection = None

    def connect(self) -> bool:
        """
        Establish connection to SQL Server.
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if self.user and self.password:
                # SQL Server Authentication
                connection_string = (
                    f"Driver={self.driver};"
                    f"Server={self.server};"
                    f"Database={self.database};"
                    f"UID={self.user};"
                    f"PWD={self.password};"
                )
            else:
                # Windows Authentication
                connection_string = (
                    f"Driver={self.driver};"
                    f"Server={self.server};"
                    f"Database={self.database};"
                    f"Trusted_Connection=yes;"
                )

            self.connection = pyodbc.connect(connection_string)
            logger.success(f"Connected to {self.database} on {self.server}")
            return True
        except pyodbc.Error as e:
            logger.error(f"Connection failed: {e}")
            return False

    def query_to_dataframe(self, query: str) -> pd.DataFrame:
        """Execute SQL query and return as DataFrame."""
        try:
            df = pd.read_sql_query(query, self.connection)
            logger.info(f"Query executed successfully. Rows: {len(df)}")
            return df
        except Exception as e:
            logger.error(f"Query execution failed: {e}")
            return pd.DataFrame()

    def close(self):
        """Close database connection."""
        if self.connection:
            self.connection.close()
            logger.info("Connection closed")


class ETLPipeline:
    """Main ETL Pipeline for Hospital Data."""

    def __init__(self):
        """Initialize ETL pipeline."""
        self.conn_transactional = None
        self.conn_dw = None
        self.dataframes = {}

    def extract_from_transactional(self) -> bool:
        """
        Extract data from HospitalBigData (transactional database).
        
        Returns:
            bool: True if successful
        """
        logger.info("=" * 60)
        logger.info("STEP 1: EXTRACTING DATA FROM TRANSACTIONAL DATABASE")
        logger.info("=" * 60)

        self.conn_transactional = SQLServerConnection(
            server=DB_SERVER,
            database=DB_TRANSACTIONAL,
            driver=DB_DRIVER,
            user=DB_USER,
            password=DB_PASSWORD,
        )

        if not self.conn_transactional.connect():
            return False

        # Extract fact and dimension tables
        queries = {
            "pacientes": "SELECT * FROM Pacientes",
            "tipo_documento": "SELECT * FROM Tipo_De_Documento",
            "medicos": "SELECT * FROM Medicos",
            "especialidades": "SELECT * FROM Especialidades",
            "consultas": "SELECT * FROM Consultas",
            "recetas": "SELECT * FROM Recetas",
            "medicamentos": "SELECT * FROM Medicamentos",
            "historial_clinico": "SELECT * FROM Historial_Clinico",
            "diagnosticos": "SELECT * FROM Diagnosticos",
            "enfermedades": "SELECT * FROM Enfermedades",
            # Add more queries as needed
        }

        for table_name, query in queries.items():
            logger.info(f"Extracting {table_name}...")
            df = self.conn_transactional.query_to_dataframe(query)
            if not df.empty:
                self.dataframes[table_name] = df
                logger.success(f"✓ {table_name}: {len(df)} rows")
            else:
                logger.warning(f"⚠ {table_name}: No data extracted or table not found")

        return True

    def transform(self) -> bool:
        """
        Transform and clean data.
        Remove orphaned records, handle NULL values, create derived columns.
        
        Returns:
            bool: True if successful
        """
        logger.info("=" * 60)
        logger.info("STEP 2: TRANSFORMING DATA")
        logger.info("=" * 60)

        try:
            # Transform Pacientes
            if "pacientes" in self.dataframes:
                logger.info("Transforming Pacientes...")
                df_pacientes = self.dataframes["pacientes"]

                # Remove rows with missing critical data
                df_pacientes = df_pacientes.dropna(subset=["ID_paciente", "Nombres_paciente"])

                # Clean phone and email
                df_pacientes["telefono_paciente"] = df_pacientes["telefono_paciente"].fillna("Unknown")
                df_pacientes["email_paciente"] = df_pacientes["email_paciente"].fillna("Unknown")

                # Calculate age
                df_pacientes["fecha_nacimiento_paciente"] = pd.to_datetime(
                    df_pacientes["fecha_nacimiento_paciente"]
                )
                df_pacientes["edad"] = (
                    (datetime.now() - df_pacientes["fecha_nacimiento_paciente"]).dt.days // 365
                )

                self.dataframes["pacientes"] = df_pacientes
                logger.success(f"✓ Pacientes transformed: {len(df_pacientes)} rows")

            # Transform Consultas (merge with Pacientes and Medicos)
            if (
                "consultas" in self.dataframes
                and "pacientes" in self.dataframes
                and "medicos" in self.dataframes
            ):
                logger.info("Transforming Consultas...")
                df_consultas = self.dataframes["consultas"]
                df_pacientes = self.dataframes["pacientes"]
                df_medicos = self.dataframes["medicos"]

                # Merge with patients using ID_paciente_consulta
                df_consultas = df_consultas.merge(
                    df_pacientes[["ID_paciente", "Nombres_paciente", "edad"]],
                    left_on="ID_paciente_consulta",
                    right_on="ID_paciente",
                    how="inner",
                )

                # Merge with doctors using ID_medico_consulta
                df_consultas = df_consultas.merge(
                    df_medicos[["ID_medico", "nombre_medico"]],
                    left_on="ID_medico_consulta",
                    right_on="ID_medico",
                    how="inner",
                )

                self.dataframes["consultas"] = df_consultas
                logger.success(f"✓ Consultas transformed: {len(df_consultas)} rows")

            # Transform Recetas (clean data, no direct medicamento merge needed)
            # Medicamentos are linked via Detalle_Recetas table
            if "recetas" in self.dataframes:
                logger.info("Transforming Recetas...")
                df_recetas = self.dataframes["recetas"]
                df_recetas = df_recetas.dropna(subset=["ID_receta"])

                self.dataframes["recetas"] = df_recetas
                logger.success(f"✓ Recetas transformed: {len(df_recetas)} rows")

            logger.success("✓ All transformations completed")
            return True

        except Exception as e:
            logger.error(f"Transformation failed: {e}")
            return False

    def load_to_dw(self) -> bool:
        """
        Load transformed data to DW_Hospital.
        
        Returns:
            bool: True if successful
        """
        logger.info("=" * 60)
        logger.info("STEP 3: LOADING DATA TO DATA WAREHOUSE")
        logger.info("=" * 60)

        self.conn_dw = SQLServerConnection(
            server=DB_SERVER,
            database=DB_DATAWAREHOUSE,
            driver=DB_DRIVER,
            user=DB_USER,
            password=DB_PASSWORD,
        )

        if not self.conn_dw.connect():
            return False

        try:
            # Load Dim_Pacientes
            if "pacientes" in self.dataframes:
                logger.info("Loading Dim_Pacientes...")
                df_pacientes = self.dataframes["pacientes"][
                    ["Nombres_paciente", "apellidos_paciente", "fecha_nacimiento_paciente",
                     "genero_paciente", "telefono_paciente", "email_paciente", "edad"]
                ]
                
                # Delete existing data (simpler than TRUNCATE with foreign keys)
                cursor = self.conn_dw.connection.cursor()
                try:
                    cursor.execute("DELETE FROM Dim_Pacientes")
                    self.conn_dw.connection.commit()
                except Exception as e:
                    logger.warning(f"Could not delete existing Dim_Pacientes: {e}")
                    self.conn_dw.connection.rollback()

                # Insert new data
                for idx, row in df_pacientes.iterrows():
                    try:
                        cursor.execute(
                            """
                            INSERT INTO Dim_Pacientes 
                            (Nombres_paciente, apellidos_paciente, fecha_nacimiento_paciente, 
                             genero_paciente, telefono_paciente, email_paciente, edad)
                            VALUES (?, ?, ?, ?, ?, ?, ?)
                            """,
                            (
                                row["Nombres_paciente"],
                                row["apellidos_paciente"],
                                row["fecha_nacimiento_paciente"],
                                row["genero_paciente"],
                                row["telefono_paciente"],
                                row["email_paciente"],
                                int(row["edad"]),
                            ),
                        )
                    except Exception as e:
                        logger.warning(f"Could not insert row {idx}: {e}")
                        
                self.conn_dw.connection.commit()
                logger.success(f"✓ Dim_Pacientes loaded: {len(df_pacientes)} rows")

            logger.success("✓ Data warehouse load completed")
            return True

        except Exception as e:
            logger.error(f"Load to DW failed: {e}")
            return False

    def export_to_csv_for_powerbi(self):
        """
        Export cleaned data to CSV for Power BI import.
        
        Returns:
            Path: Path to exported CSV file
        """
        logger.info("=" * 60)
        logger.info("STEP 4: EXPORTING DATA FOR POWER BI")
        logger.info("=" * 60)

        try:
            # Create master table combining consultas, patients, and doctors
            if "consultas" in self.dataframes:
                master_df = self.dataframes["consultas"].copy()
                
                # Clean and prepare
                master_df = master_df.fillna("Unknown")
                
                # Export
                output_path = PROCESSED_DATA_DIR / "Data_Hospital_BI.csv"
                master_df.to_csv(output_path, index=False, encoding="utf-8-sig")
                
                logger.success(f"✓ Data exported to Power BI: {output_path}")
                return output_path
            else:
                logger.warning("⚠ Consultas data not found. Skipping Power BI export.")
                return None

        except Exception as e:
            logger.error(f"Power BI export failed: {e}")
            return None

    def run(self):
        """Execute complete ETL pipeline."""
        logger.info("\n" + "=" * 60)
        logger.info("🏥 HOSPITAL ETL PIPELINE STARTED")
        logger.info("=" * 60 + "\n")

        try:
            # Step 1: Extract
            if not self.extract_from_transactional():
                logger.error("❌ ETL Pipeline failed at Extract stage")
                return False

            # Step 2: Transform
            if not self.transform():
                logger.error("❌ ETL Pipeline failed at Transform stage")
                return False

            # Step 3: Load to DW
            if not self.load_to_dw():
                logger.warning("⚠ Load to DW failed, but continuing to export CSV")

            # Step 4: Export for Power BI
            self.export_to_csv_for_powerbi()

            logger.info("\n" + "=" * 60)
            logger.success("✓ ETL Pipeline completed successfully!")
            logger.info("=" * 60 + "\n")
            return True

        except Exception as e:
            logger.error(f"❌ ETL Pipeline failed with error: {e}")
            return False

        finally:
            # Cleanup
            if self.conn_transactional:
                self.conn_transactional.close()
            if self.conn_dw:
                self.conn_dw.close()


if __name__ == "__main__":
    pipeline = ETLPipeline()
    pipeline.run()
