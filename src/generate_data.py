"""
Generate Data Module

This module generates a synthetic, highly realistic supply chain dataset encompassing
various product categories, inventory mechanics, supplier delays, and seasonal demand. 
"""

import os
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Tuple

import pandas as pd
import numpy as np

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def generate_supply_chain_data(num_records: int = 5000) -> None:
    """
    Generates synthetic supply chain tracking data and writes it to a CSV file.

    Parameters
    ----------
    num_records : int
        The number of sequential daily record transactions to mock.
        Defaults to 5000.

    Returns
    -------
    None
        The resulting pandas DataFrame is directly saved to `data/raw/supply_chain_data.csv`.
        
    Raises
    ------
    IOError
        If there is an issue saving the generated CSV file to the disk.
    """
    logger.info(f"Starting data generation for {num_records} records.")
    np.random.seed(42)
    
    categories: List[str] = ['Electronics', 'Clothing', 'Home & Kitchen', 'Sports', 'Beauty']
    products: Dict[str, List[str]] = {
        'Electronics': ['Laptop', 'Smartphone', 'Tablet', 'Headphones', 'Smartwatch'],
        'Clothing': ['T-Shirt', 'Jeans', 'Sneakers', 'Jacket', 'Sweater'],
        'Home & Kitchen': ['Blender', 'Microwave', 'Coffee Maker', 'Vacuum Cleaner', 'Air Purifier'],
        'Sports': ['Yoga Mat', 'Dumbbells', 'Tennis Racket', 'Basketball', 'Treadmill'],
        'Beauty': ['Moisturizer', 'Perfume', 'Lipstick', 'Shampoo', 'Sunscreen']
    }
    
    # Flatten products into a map of (Category, Product Name, Product ID)
    product_list: List[Tuple[str, str, str]] = []
    pid_counter: int = 1000
    for cat, prods in products.items():
        for prod in prods:
            product_list.append((cat, prod, f"PRD{pid_counter}"))
            pid_counter += 1
            
    # Dates spanning 2 years back
    start_date: datetime = datetime(2022, 1, 1)
    date_list: List[datetime] = [start_date + timedelta(days=x) for x in range(730)]
    
    suppliers: List[str] = [f"SUP{100+i}" for i in range(10)]
    regions: List[str] = ['North America', 'Europe', 'Asia', 'South America', 'Oceania']
    warehouses: List[str] = ['WH-A', 'WH-B', 'WH-C', 'WH-D']
    
    data: List[Dict] = []
    
    for _ in range(num_records):
        date = np.random.choice(date_list)
        cat, prod, pid = product_list[np.random.randint(0, len(product_list))]
        
        base_demand: int = np.random.randint(10, 100)
        month: int = pd.to_datetime(date).month
        
        # Inject realistic seasonality
        if cat == 'Electronics' and month in [11, 12]:
            base_demand = int(base_demand * 1.5)
        elif cat == 'Clothing' and month in [6, 7, 8] and prod == 'T-Shirt':
            base_demand = int(base_demand * 1.3)
        
        demand: int = max(0, int(np.random.normal(base_demand, 15)))
        inventory_level: int = np.random.randint(0, 500)
        reorder_point: int = np.random.randint(50, 150)
        lead_time: int = np.random.randint(3, 14) 
        
        if inventory_level == 0:
            stock_status = "Out of Stock"
        elif inventory_level < reorder_point:
            stock_status = "Low Stock"
        else:
            stock_status = "In Stock"
            
        order_quantity: int = np.random.randint(100, 300) if stock_status in ["Out of Stock", "Low Stock"] else 0
            
        data.append({
            'Date': date,
            'Product ID': pid,
            'Product Name': prod,
            'Category': cat,
            'Demand (Units Sold)': demand,
            'Inventory Level': inventory_level,
            'Reorder Point': reorder_point,
            'Lead Time (days)': lead_time,
            'Supplier ID': np.random.choice(suppliers),
            'Region': np.random.choice(regions),
            'Warehouse': np.random.choice(warehouses),
            'Stock Status': stock_status,
            'Order Quantity': order_quantity
        })
        
    df = pd.DataFrame(data)
    df = df.sort_values(by=['Date', 'Product ID']).reset_index(drop=True)
    
    # Dynamic secure absolute path mapping
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_dir = os.path.join(root_dir, 'data', 'raw')
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'supply_chain_data.csv')
    
    try:
        df.to_csv(output_path, index=False)
        logger.info(f"Successfully generated and structured {num_records} records.")
        logger.info(f"File saved to {output_path}")
    except IOError as e:
        logger.error(f"Failed to write CSV output: {str(e)}")
        raise

if __name__ == "__main__":
    generate_supply_chain_data(10000)
