"""
Preprocess Module

Loads raw supply chain analytical data, handles missing records, enforces date indices,
and computes higher-order features for BI visualization (Inventory Turnover).
"""

import os
import logging
from typing import Optional

import pandas as pd
import numpy as np

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def preprocess_data() -> None:
    """
    Ingests 'supply_chain_data.csv', scrubs duplicates / nulls, and builds KPIs.

    Returns
    -------
    None
        Processed records are saved directly to `data/processed/cleaned_supply_chain_data.csv`.

    Raises
    ------
    FileNotFoundError
        If the primary raw dataset is missing from the data directory.
    Exception
        Any generalized pandas transformation exception during data grooming.
    """
    base_dir: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    input_path: str = os.path.join(base_dir, 'data', 'raw', 'supply_chain_data.csv')
    
    if not os.path.exists(input_path):
        logger.error(f"Input file not found at {input_path}. Please run generate_data.py first.")
        raise FileNotFoundError(f"Missing raw data: {input_path}")
        
    logger.info("Loading raw data into DataFrame.")
    try:
        df: pd.DataFrame = pd.read_csv(input_path)
    except Exception as e:
        logger.error(f"Failed to load CSV: {e}")
        raise
    
    # Data Cleaning Phase
    logger.info("De-duplicating and scrubbing NaN values.")
    initial_len = len(df)
    df = df.drop_duplicates()
    df = df.ffill() 
    logger.debug(f"Removed {initial_len - len(df)} duplicate records.")
    
    # Feature Engineering (Date)
    df['Date'] = pd.to_datetime(df['Date'])
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month
    
    # Feature Engineering (KPIs)
    logger.info("Computing secondary financial KPIs (Turnover Ratio, etc.)")
    # Inventory Turnover Ratio = Demand / Average Inventory
    # Add an epsilon value to prevent division by zero in math logic
    df['Inventory Turnover Ratio'] = df['Demand (Units Sold)'] / (df['Inventory Level'] + 1e-5)
    
    # Days of Inventory Remaining = Inventory Level / Average Daily Demand
    df['Days of Inventory Remaining'] = np.where(
        df['Demand (Units Sold)'] > 0,
        df['Inventory Level'] / df['Demand (Units Sold)'],
        999.0
    )
    
    # Final cleanup
    df['Inventory Turnover Ratio'] = df['Inventory Turnover Ratio'].round(2)
    df['Days of Inventory Remaining'] = df['Days of Inventory Remaining'].round(2)
    
    # Export Phase
    output_dir: str = os.path.join(base_dir, 'data', 'processed')
    os.makedirs(output_dir, exist_ok=True)
    output_path: str = os.path.join(output_dir, 'cleaned_supply_chain_data.csv')
    
    try:
        df.to_csv(output_path, index=False)
        logger.info(f"Preprocessing fully completed. Saved to {output_path}")
    except IOError as e:
        logger.error(f"Error saving processed data: {e}")
        raise

if __name__ == "__main__":
    preprocess_data()
