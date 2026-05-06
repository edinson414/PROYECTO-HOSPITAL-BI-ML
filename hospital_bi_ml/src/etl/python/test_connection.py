"""
Test script to verify SQL Server connection.
Run this first to ensure connectivity before running the full ETL pipeline.
"""

import os
import sys
from pathlib import Path

# Compute project root (hospital_bi_ml) and ensure both it and its parent are on sys.path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root.parent))
sys.path.insert(0, str(project_root))

import pyodbc
from loguru import logger
from hospital_bi_ml.config import (
    DB_SERVER,
    DB_DRIVER,
    DB_USER,
    DB_PASSWORD,
    DB_TRANSACTIONAL,
    DB_DATAWAREHOUSE,
)


def test_connection(server: str, database: str, driver: str, user: str = "", password: str = ""):
    """Test connection to SQL Server database."""
    try:
        if user and password:
            # SQL Server Authentication
            connection_string = (
                f"Driver={driver};"
                f"Server={server};"
                f"Database={database};"
                f"UID={user};"
                f"PWD={password};"
            )
        else:
            # Windows Authentication
            connection_string = (
                f"Driver={driver};"
                f"Server={server};"
                f"Database={database};"
                f"Trusted_Connection=yes;"
            )

        logger.info(f"Attempting connection to {database} on {server}...")
        connection = pyodbc.connect(connection_string)
        
        # Test query
        cursor = connection.cursor()
        cursor.execute("SELECT @@version as version")
        version = cursor.fetchone()[0]
        
        logger.success(f"✓ Connected successfully to {database}")
        logger.info(f"SQL Server Version: {version}")
        
        # List tables
        cursor.execute(
            "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE'"
        )
        tables = [row[0] for row in cursor.fetchall()]
        logger.info(f"Tables found: {', '.join(tables) if tables else 'No tables'}")
        
        connection.close()
        return True
        
    except pyodbc.Error as e:
        logger.error(f"✗ Connection failed: {e}")
        return False


if __name__ == "__main__":
    logger.info("=" * 70)
    logger.info("SQL SERVER CONNECTION TEST")
    logger.info("=" * 70)
    
    # Test transactional database
    logger.info(f"\n[1/2] Testing TRANSACTIONAL DATABASE: {DB_TRANSACTIONAL}")
    transactional_ok = test_connection(
        server=DB_SERVER,
        database=DB_TRANSACTIONAL,
        driver=DB_DRIVER,
        user=DB_USER,
        password=DB_PASSWORD,
    )
    
    # Test data warehouse
    logger.info(f"\n[2/2] Testing DATA WAREHOUSE: {DB_DATAWAREHOUSE}")
    dw_ok = test_connection(
        server=DB_SERVER,
        database=DB_DATAWAREHOUSE,
        driver=DB_DRIVER,
        user=DB_USER,
        password=DB_PASSWORD,
    )
    
    # Summary
    logger.info("\n" + "=" * 70)
    if transactional_ok and dw_ok:
        logger.success("✓ ALL TESTS PASSED - Ready to run ETL pipeline!")
    else:
        logger.error("✗ TESTS FAILED - Check your SQL Server configuration")
        if not transactional_ok:
            logger.error(f"  - Cannot connect to {DB_TRANSACTIONAL}")
        if not dw_ok:
            logger.error(f"  - Cannot connect to {DB_DATAWAREHOUSE}")
    logger.info("=" * 70)
