# Architecture Overview

This document outlines the architectural design and data flow of the **Supply Chain & Inventory Analytics** project. The project is designed sequentially to handle data generation, pre-processing, modeling, and interactive visualization. 

## System Components

### 1. Data Engineering (`src/generate_data.py`, `src/preprocess.py`)
- **Data Generator**: A synthetic data generator simulating realistic business operations, supplier lead times, reorder thresholds, and demand seasonality.
- **Preprocessor**: Implements data cleaning and transformation logic, generating KPI metrics like `Inventory Turnover Ratio`. This layer essentially acts as a localized ETL (Extract, Transform, Load) pipeline outputting flat analytical records.

### 2. Analytical & Statistical Layer (`sql/analysis.sql`, `notebooks/eda.py`)
- **SQL Analysis**: Contains parameterized SQL queries demonstrating direct aggregations and reporting logic agnostic of the database dialect. 
- **Exploratory Data Analysis (EDA)**: Python-based analysis scripts running Pandas aggregations and rendering Seaborn/Matplotlib correlation heatmaps and trend analyses over time.

### 3. Machine Learning Forecasting (`src/forecasting.py`)
- **Demand Model**: Features an engineering pipeline transforming historical demand data into lag features (L1, L2, L3). 
- **Algorithms**: Evaluates baseline Moving Average accuracy vs. a Scikit-Learn `LinearRegression` algorithm.
- **Output Hook**: Serializes the best-performing model (`lr_demand_model.pkl`) and exports near-term future demand CSVs to the local datastore.

### 4. Presentation Layer (`dashboard/app.py`)
- **Streamlit Web Application**: An interactive visualization dashboard serving as the user interface. It consumes the `cleaned_supply_chain_data.csv` and the ML forecast outputs, displaying risk alerts, top-product summaries, and real-time inventory levels.

## Data Flow Diagram
```text
[Raw Generation Script] -> [data/raw/*.csv] -> [Pre-Processor Script] -> [data/processed/cleaned_data.csv]
                                                                                   |
                                                                                   +--> [SQL Queries / EDA Generation] -> [reports/]
                                                                                   |
                                                                                   +--> [Forecasting Model Training] -> [models/] / [forecasts.csv]
                                                                                                      |
                                                                                                      v
                                                                                           [Streamlit Dashboard]
```

## Technology Choices
- **Pandas / NumPy**: Chosen for their robust, in-memory vectorized data transformation capabilities.
- **Scikit-Learn**: Industry-standard ML framework. Picked linear regression as a highly interpretable baseline for sequential structural lags securely handling univariate time-series data.
- **Streamlit**: Selected for its rapid prototyping speed bridging Python logic directly into full-feature React-based frontends without requiring API construction.
