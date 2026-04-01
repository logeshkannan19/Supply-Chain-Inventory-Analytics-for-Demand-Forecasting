import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

def generate_supply_chain_data(num_records=5000):
    np.random.seed(42)
    
    # Products and Categories
    categories = ['Electronics', 'Clothing', 'Home & Kitchen', 'Sports', 'Beauty']
    products = {
        'Electronics': ['Laptop', 'Smartphone', 'Tablet', 'Headphones', 'Smartwatch'],
        'Clothing': ['T-Shirt', 'Jeans', 'Sneakers', 'Jacket', 'Sweater'],
        'Home & Kitchen': ['Blender', 'Microwave', 'Coffee Maker', 'Vacuum Cleaner', 'Air Purifier'],
        'Sports': ['Yoga Mat', 'Dumbbells', 'Tennis Racket', 'Basketball', 'Treadmill'],
        'Beauty': ['Moisturizer', 'Perfume', 'Lipstick', 'Shampoo', 'Sunscreen']
    }
    
    # Flatten products into a list of (Category, Product Name, Product ID)
    product_list = []
    pid_counter = 1000
    for cat, prods in products.items():
        for prod in prods:
            product_list.append((cat, prod, f"PRD{pid_counter}"))
            pid_counter += 1
            
    # Dates spanning 2 years
    start_date = datetime(2022, 1, 1)
    date_list = [start_date + timedelta(days=x) for x in range(730)]
    
    # Other dimensional attributes
    suppliers = [f"SUP{100+i}" for i in range(10)]
    regions = ['North America', 'Europe', 'Asia', 'South America', 'Oceania']
    warehouses = ['WH-A', 'WH-B', 'WH-C', 'WH-D']
    
    data = []
    
    # Generate sequential data simulating daily operations
    # To make demand realistic, we apply some seasonality and trend based on category
    for i in range(num_records):
        date = np.random.choice(date_list)
        cat, prod, pid = product_list[np.random.randint(0, len(product_list))]
        
        # Base demand and variations
        base_demand = np.random.randint(10, 100)
        
        # Seasonality: Electronics higher in Q4, Clothing varies by month
        month = pd.to_datetime(date).month
        if cat == 'Electronics' and month in [11, 12]:
            base_demand = int(base_demand * 1.5)
        elif cat == 'Clothing' and month in [6, 7, 8]: # Summer
            if prod in ['T-Shirt']:
                base_demand = int(base_demand * 1.3)
        
        demand = max(0, int(np.random.normal(base_demand, 15)))
        
        # Inventory mechanics
        inventory_level = np.random.randint(0, 500)
        reorder_point = np.random.randint(50, 150)
        lead_time = np.random.randint(3, 14) # days
        supplier_id = np.random.choice(suppliers)
        region = np.random.choice(regions)
        warehouse = np.random.choice(warehouses)
        
        # Stock Status based on inventory vs demand
        if inventory_level == 0:
            stock_status = "Out of Stock"
        elif inventory_level < reorder_point:
            stock_status = "Low Stock"
        else:
            stock_status = "In Stock"
            
        # Order quantity (replenishment)
        if stock_status in ["Out of Stock", "Low Stock"]:
            order_quantity = np.random.randint(100, 300)
        else:
            order_quantity = 0
            
        data.append({
            'Date': date,
            'Product ID': pid,
            'Product Name': prod,
            'Category': cat,
            'Demand (Units Sold)': demand,
            'Inventory Level': inventory_level,
            'Reorder Point': reorder_point,
            'Lead Time (days)': lead_time,
            'Supplier ID': supplier_id,
            'Region': region,
            'Warehouse': warehouse,
            'Stock Status': stock_status,
            'Order Quantity': order_quantity
        })
        
    df = pd.DataFrame(data)
    # Sort by date
    df = df.sort_values(by=['Date', 'Product ID']).reset_index(drop=True)
    
    # Save to CSV
    output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'raw')
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'supply_chain_data.csv')
    df.to_csv(output_path, index=False)
    print(f"Generated {num_records} records of supply chain data.")
    print(f"Saved to {output_path}")

if __name__ == "__main__":
    generate_supply_chain_data(10000)
