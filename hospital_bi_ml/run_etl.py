#!/usr/bin/env python
"""
Hospital ETL Pipeline Runner
Simple wrapper to run ETL from project root
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
# Ensure both project root and its parent are on sys.path so imports like
# `src.*` and `hospital_bi_ml.*` resolve correctly when running from VS Code.
sys.path.insert(0, str(project_root.parent))
sys.path.insert(0, str(project_root))

from src.etl.python.etl_pipeline import ETLPipeline
from loguru import logger


def main():
    """Run ETL pipeline."""
    pipeline = ETLPipeline()
    success = pipeline.run()
    
    if success:
        print("\n✓ ETL Pipeline completed successfully!")
        print(f"✓ CSV file ready for Power BI at: data/processed/Data_Hospital_BI.csv")
        return 0
    else:
        print("\n✗ ETL Pipeline failed!")
        return 1


if __name__ == "__main__":
    sys.exit(main())
