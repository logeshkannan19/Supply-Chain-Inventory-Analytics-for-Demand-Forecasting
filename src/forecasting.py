"""
Forecasting Module

Trains a Linear Regression model on aggregated weekly supply chain demand DataFrames
to predict future item needs and inform automated Reorder Point strategies. 
"""

import os
import logging
from typing import Optional, Tuple

import pandas as pd
import numpy as np
import joblib

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def train_forecast_models() -> None:
    """
    Ingests cleaned records, maps historical Moving Average lag variables (L1, L2, L3),
    evaluates a Scikit-Learn LinearRegressor, and outputs 4 constraints:
      - Trained .pkl Model weights
      - Computed Forecast CSV for dashboard loading

    Returns
    -------
    None
        Prints MAE execution variables directly to the terminal logger.
        
    Raises
    ------
    FileNotFoundError
        When processed dependencies are missing preventing dataframe loads.
    """
    logger.info("Initializing demand forecasting script.")
    base_dir: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path: str = os.path.join(base_dir, 'data', 'processed', 'cleaned_supply_chain_data.csv')
    model_dir: str = os.path.join(base_dir, 'models')
    
    os.makedirs(model_dir, exist_ok=True)
    
    if not os.path.exists(data_path):
        logger.error(f"Processed dataset empty/missing at {data_path}.")
        raise FileNotFoundError("Missing prerequisite: cleaned_supply_chain_data.csv")
        
    logger.info("Loading preprocessed analytical metrics...")
    df: pd.DataFrame = pd.read_csv(data_path)
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Aggregate demand weekly per product ID
    logger.info("Aggregating transactional volume into a sequential Weekly Demand DataFrame.")
    weekly_data = df.groupby([pd.Grouper(key='Date', freq='W-MON'), 'Product ID']).agg({
        'Demand (Units Sold)': 'sum'
    }).reset_index()
    
    weekly_data.rename(columns={'Demand (Units Sold)': 'Weekly_Demand'}, inplace=True)
    weekly_data = weekly_data.sort_values(by=['Product ID', 'Date'])
    
    # Feature Engineering (Lag Sequence Creation)
    weekly_data['Lag_1'] = weekly_data.groupby('Product ID')['Weekly_Demand'].shift(1)
    weekly_data['Lag_2'] = weekly_data.groupby('Product ID')['Weekly_Demand'].shift(2)
    weekly_data['Lag_3'] = weekly_data.groupby('Product ID')['Weekly_Demand'].shift(3)
    
    # Baseline Output (Standard Simple Moving Average)
    weekly_data['MA_Forecast'] = weekly_data[['Lag_1', 'Lag_2', 'Lag_3']].mean(axis=1)
    
    ml_data: pd.DataFrame = weekly_data.dropna().copy()
    
    X = ml_data[['Lag_1', 'Lag_2', 'Lag_3']]
    y = ml_data['Weekly_Demand']
    
    # 90-10 Temporal Train-Test Validation Split
    split_idx: int = int(len(ml_data) * 0.9)
    train_data: pd.DataFrame = ml_data.iloc[:split_idx]
    test_data: pd.DataFrame = ml_data.iloc[split_idx:]
    
    X_train = train_data[['Lag_1', 'Lag_2', 'Lag_3']]
    y_train = train_data['Weekly_Demand']
    
    X_test = test_data[['Lag_1', 'Lag_2', 'Lag_3']]
    y_test = test_data['Weekly_Demand']
    
    logger.info("Training secondary predictive LinearRegression mapping...")
    lr_model = LinearRegression()
    lr_model.fit(X_train, y_train)
    
    test_data = test_data.copy()
    test_data['LR_Forecast'] = lr_model.predict(X_test)
    
    # Evaluation Logic
    ma_mae: float = mean_absolute_error(test_data['Weekly_Demand'], test_data['MA_Forecast'])
    lr_mae: float = mean_absolute_error(test_data['Weekly_Demand'], test_data['LR_Forecast'])
    
    logger.info(f"EVALUATION: Baseline Moving Average MAE: {ma_mae:.2f}")
    logger.info(f"EVALUATION: Linear Regression MAE: {lr_mae:.2f}")
    
    # Save Model 
    model_path: str = os.path.join(model_dir, 'lr_demand_model.pkl')
    try:
        joblib.dump(lr_model, model_path)
        logger.info(f"Model successfully saved to {model_path}")
    except IOError as e:
        logger.error(f"Failed to save joblib pickle: {e}")
    
    # Next Cycle Extraction
    logger.info("Computing active forecast variables for nearest future timeframe...")
    latest_data = weekly_data.groupby('Product ID').last().reset_index()
    X_future = latest_data[['Weekly_Demand', 'Lag_1', 'Lag_2']].copy()
    
    # Shift labels backward one unit mapped cleanly for forward prediction
    X_future.rename(columns={'Weekly_Demand': 'Lag_1', 'Lag_1': 'Lag_2', 'Lag_2': 'Lag_3'}, inplace=True)
    
    future_forecast = lr_model.predict(X_future[['Lag_1', 'Lag_2', 'Lag_3']])
    
    forecast_df = pd.DataFrame({
        'Product ID': latest_data['Product ID'],
        'Forecasted_Demand_Next_Week': np.round(future_forecast, 0)
    })
    
    output_path: str = os.path.join(base_dir, 'data', 'processed', 'forecast_outputs.csv')
    try:
        forecast_df.to_csv(output_path, index=False)
        logger.info(f"Exported final future metric inferences directly to {output_path}")
    except IOError as e:
        logger.error(f"Failed exporting future inferences: {e}")

if __name__ == "__main__":
    train_forecast_models()
