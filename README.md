# 📦 Supply Chain & Inventory Analytics for Demand Forecasting

An end-to-end data analytics solution designed to analyze demand patterns, optimize inventory levels, and improve supply chain efficiency. This complete pipeline ingests data, engineers features, trains forecasting models, and serves actionable insights to a Streamlit UI.

---

## 🔹 Project Overview
This repository contains a full project structure simulating a data scientist or supply chain analyst's workflow:
1. **Data Generation & Cleaning**: Mocks 10,000 rows of daily supply chain inventory/sales data, factoring in product seasonality. Cleanses and transforms these into standardized metric formats. 
2. **Exploratory Data Analysis**: Evaluates historic trends, inventory vs. demand dependencies, and overall KPIs.
3. **Machine Learning Forecasting**: Predicts future demand using Moving Average and Linear Regression, saving model weights.
4. **Interactive Dashboard**: A clean and reactive UI built in Streamlit for real-time inventory risk monitoring and decision making.
5. **SQL Integrations**: Pre-built SQL queries mapping to critical business questions.

---

## 🔹 Tech Stack
* **Python**: Pandas, NumPy
* **Visualization**: Matplotlib, Seaborn, Plotly (for Dashboard)
* **Delivery/UI**: Streamlit
* **Machine Learning**: Scikit-learn, joblib
* **Data Access**: Standard PostgreSQL analytics syntax files.

---

## 🔹 Project Structure
```text
SupplyChainAnalytics/
│
├── data/
│   ├── raw/                 # Generated synthetic raw data
│   └── processed/           # Cleaned data and feature variables
│
├── notebooks/
│   └── eda.py               # Exploratory Data Analysis script generating reports
│
├── sql/
│   └── analysis.sql         # Core SQL tracking queries
│
├── src/
│   ├── generate_data.py     # Script to generate random product datasets
│   ├── preprocess.py        # Cleaning missing values and feature engineering
│   └── forecasting.py       # Linear regression forecasting algorithm
│
├── dashboard/
│   └── app.py               # Streamlit application
│
├── models/
│   └── lr_demand_model.pkl  # Stored Linear Regression Model
│
├── reports/                 # Output charts (Heatmaps, Overviews)
│
├── requirements.txt         # Project Dependencies
└── README.md                # This document
```

---

## 🔹 Key Insights 
- **Stock-Out Awareness**: Tracking Stock-Outs per Day directly correlates with negative profitability. 
- **Forecast Validity**: Moving average and standard Linear lag regression demonstrated an active error MAE of < 90 units per week per product. This provides a measurable improvement in Reorder Point strategy compared to reactive restocks.
- **Turnover Optimization**: By tracking `Demand / Inventory Level`, operational teams can lower holding costs while keeping necessary demand items at safe thresholds.

---

## 🔹 How to Run

1. **Clone & Setup Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Generate and Process Data** (if not already done)
   ```bash
   python src/generate_data.py
   python src/preprocess.py
   ```

3. **Train Forecasting Model & Run EDA**
   ```bash
   python src/forecasting.py
   python notebooks/eda.py
   ```
   *(See the `reports/` folder for generated visualizations)*

4. **Launch Dashboard**
   ```bash
   streamlit run dashboard/app.py
   ```
   Navigate to `localhost:8501` to view your supply chain application!

---

## 🔹 Future Improvements
* Transition from CSV-based local persistence to an active Postgres/MySQL Database layer via SQLAlchemy.
* Incorporate advanced deep learning forecasting models (LSTMs, Prophet).
* Add detailed Supplier Lead Time delay analytics directly into the dashboard context. 
