import pandas as pd
import numpy as np
import os

def preprocess_data():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    input_path = os.path.join(base_dir, 'data', 'raw', 'supply_chain_data.csv')
    
    if not os.path.exists(input_path):
        print(f"Error: {input_path} not found.")
        return
        
    print("Loading raw data...")
    df = pd.read_csv(input_path)
    
    # 1. Handle missing values & duplicates
    print("Cleaning data...")
    df = df.drop_duplicates()
    df = df.fillna(method='ffill') # Simple forward fill for any generated NaNs
    
    # 2. Date conversion & extraction
    df['Date'] = pd.to_datetime(df['Date'])
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month
    
    # 3. Create features
    # Inventory Turnover Ratio = Demand / Average Inventory (we use current for daily)
    # Adding small epsilon to avoid division by zero
    df['Inventory Turnover Ratio'] = df['Demand (Units Sold)'] / (df['Inventory Level'] + 1e-5)
    
    # Days of Inventory Remaining = Inventory Level / Average Daily Demand
    # If Demand is 0, we assume infinite (or put 999)
    df['Days of Inventory Remaining'] = np.where(
        df['Demand (Units Sold)'] > 0,
        df['Inventory Level'] / df['Demand (Units Sold)'],
        999
    )
    
    # Round metrics for readability
    df['Inventory Turnover Ratio'] = df['Inventory Turnover Ratio'].round(2)
    df['Days of Inventory Remaining'] = df['Days of Inventory Remaining'].round(2)
    
    # Save processed dataset
    output_dir = os.path.join(base_dir, 'data', 'processed')
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'cleaned_supply_chain_data.csv')
    
    df.to_csv(output_path, index=False)
    print(f"Preprocessing complete. Cleaned data saved to {output_path}")

if __name__ == "__main__":
    preprocess_data()
