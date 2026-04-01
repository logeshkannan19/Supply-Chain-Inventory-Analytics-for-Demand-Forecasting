import pandas as pd
import numpy as np
import os
import joblib
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error

def train_forecast_models():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_dir, 'data', 'processed', 'cleaned_supply_chain_data.csv')
    model_dir = os.path.join(base_dir, 'models')
    
    os.makedirs(model_dir, exist_ok=True)
    
    print("Loading data for forecasting...")
    df = pd.read_csv(data_path)
    df['Date'] = pd.to_datetime(df['Date'])
    
    # We will aggregate demand weekly per product
    # To keep it simple, let's forecast the total overall weekly demand as an example,
    # and also a generic model that takes product-level weekly history.
    
    print("Preparing aggregated weekly demand...")
    weekly_data = df.groupby([pd.Grouper(key='Date', freq='W-MON'), 'Product ID']).agg({
        'Demand (Units Sold)': 'sum'
    }).reset_index()
    
    weekly_data.rename(columns={'Demand (Units Sold)': 'Weekly_Demand'}, inplace=True)
    weekly_data = weekly_data.sort_values(by=['Product ID', 'Date'])
    
    # Create Moving Average (lag-based features)
    # We create Lag_1, Lag_2, Lag_3 weeks of demand to predict the current week
    weekly_data['Lag_1'] = weekly_data.groupby('Product ID')['Weekly_Demand'].shift(1)
    weekly_data['Lag_2'] = weekly_data.groupby('Product ID')['Weekly_Demand'].shift(2)
    weekly_data['Lag_3'] = weekly_data.groupby('Product ID')['Weekly_Demand'].shift(3)
    
    # Moving average (Baseline) prediction: Average of last 3 weeks
    weekly_data['MA_Forecast'] = weekly_data[['Lag_1', 'Lag_2', 'Lag_3']].mean(axis=1)
    
    # Drop NaNs for ML
    ml_data = weekly_data.dropna().copy()
    
    X = ml_data[['Lag_1', 'Lag_2', 'Lag_3']]
    y = ml_data['Weekly_Demand']
    
    # Train-test split (Temporal)
    # Last 10% of time as test
    split_idx = int(len(ml_data) * 0.9)
    train_data = ml_data.iloc[:split_idx]
    test_data = ml_data.iloc[split_idx:]
    
    X_train, y_train = train_data[['Lag_1', 'Lag_2', 'Lag_3']], train_data['Weekly_Demand']
    X_test, y_test = test_data[['Lag_1', 'Lag_2', 'Lag_3']], test_data['Weekly_Demand']
    
    print("Training Linear Regression model...")
    lr_model = LinearRegression()
    lr_model.fit(X_train, y_train)
    
    # Predict
    test_data = test_data.copy()
    test_data['LR_Forecast'] = lr_model.predict(X_test)
    
    # Evaluation
    ma_mae = mean_absolute_error(test_data['Weekly_Demand'], test_data['MA_Forecast'])
    lr_mae = mean_absolute_error(test_data['Weekly_Demand'], test_data['LR_Forecast'])
    
    print(f"Moving Average MAE: {ma_mae:.2f}")
    print(f"Linear Regression MAE: {lr_mae:.2f}")
    
    # Save Model
    model_path = os.path.join(model_dir, 'lr_demand_model.pkl')
    joblib.dump(lr_model, model_path)
    print(f"Model saved to {model_path}")
    
    # Save a forecast outputs file to display in dashboard
    # We'll compute future forecast for all products for the next 1 week
    latest_data = weekly_data.groupby('Product ID').last().reset_index()
    X_future = latest_data[['Weekly_Demand', 'Lag_1', 'Lag_2']] # This becomes lag1, lag2, lag3 for next week
    X_future.rename(columns={'Weekly_Demand': 'Lag_1', 'Lag_1': 'Lag_2', 'Lag_2': 'Lag_3'}, inplace=True)
    
    future_forecast = lr_model.predict(X_future[['Lag_1', 'Lag_2', 'Lag_3']])
    
    forecast_df = pd.DataFrame({
        'Product ID': latest_data['Product ID'],
        'Forecasted_Demand_Next_Week': np.round(future_forecast, 0)
    })
    
    output_path = os.path.join(base_dir, 'data', 'processed', 'forecast_outputs.csv')
    forecast_df.to_csv(output_path, index=False)
    print(f"Next week forecasts saved to {output_path}")

if __name__ == "__main__":
    train_forecast_models()
