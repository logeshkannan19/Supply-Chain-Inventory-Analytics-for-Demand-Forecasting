# Architecture Documentation

> Comprehensive technical documentation for the Supply Chain & Inventory Analytics Platform

---

## Table of Contents

1. [System Overview](#system-overview)
2. [Architecture Layers](#architecture-layers)
3. [Component Design](#component-design)
4. [Data Architecture](#data-architecture)
5. [ML Pipeline Architecture](#ml-pipeline-architecture)
6. [Application Architecture](#application-architecture)
7. [Infrastructure Architecture](#infrastructure-architecture)
8. [Security Architecture](#security-architecture)

---

## System Overview

The Supply Chain & Inventory Analytics Platform is a modular, batch-oriented analytics system designed to transform raw supply chain data into actionable business insights through machine learning forecasting and interactive visualization.

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           PRESENTATION LAYER                               │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                    Streamlit Dashboard (Port 8501)                  │   │
│  │  • KPI Metrics  • Risk Alerts  • Forecast Display  • Filtering       │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           APPLICATION LAYER                                │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │
│  │ Data Generator│  │ Preprocessor │  │ Forecaster   │  │   EDA Tool   │    │
│  │  (generate)   │  │  (preprocess)│  │ (forecasting)│  │   (eda.py)  │    │
│  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘    │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                             DATA LAYER                                      │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐                 │
│  │  Raw Data CSV  │  │ Processed Data │  │  ML Models &   │                 │
│  │  (data/raw/)   │  │  (data/proc/)  │  │  Forecasts     │                 │
│  └────────────────┘  └────────────────┘  └────────────────┘                 │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Design Principles

| Principle | Implementation |
|-----------|----------------|
| **Modularity** | Each component is self-contained with clear interfaces |
| **Extensibility** | Configurable via YAML, easy to add new models |
| **Reproducibility** | Fixed random seeds, versioned data outputs |
| **Observability** | Structured logging throughout pipeline |

---

## Architecture Layers

### Layer 1: Data Engineering

**Responsibility**: Generate, ingest, clean, and transform raw supply chain data

**Components**:
- `src/generate_data.py` - Synthetic data generation
- `src/preprocess.py` - ETL pipeline

**Input**: Configuration (products, suppliers, date ranges)
**Output**: Cleaned CSV with engineered features

```
┌────────────────────────────────────────────────────────────────┐
│                   DATA ENGINEERING LAYER                       │
│                                                                │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐      │
│  │   Config     │───▶│   Generator  │───▶│    Raw CSV   │      │
│  │  (config.yaml)   │  (generate)  │    │  (data/raw/) │      │
│  └──────────────┘    └──────────────┘    └──────────────┘      │
│                            │                                   │
│                            ▼                                   │
│                     ┌──────────────┐    ┌──────────────┐      │
│                     │ Preprocessor │───▶│  Clean CSV   │      │
│                     │ (preprocess) │    │(data/proc/) │      │
│                     └──────────────┘    └──────────────┘      │
│                            │                                   │
│                            ▼                                   │
│                     ┌──────────────┐                          │
│                     │   Features   │                          │
│                     │ • Turnover   │                          │
│                     │ • Days Left  │                          │
│                     └──────────────┘                          │
└────────────────────────────────────────────────────────────────┘
```

### Layer 2: Machine Learning

**Responsibility**: Train and evaluate demand forecasting models

**Components**:
- `src/forecasting.py` - Model training and prediction
- `models/` - Serialized model artifacts

**Input**: Processed historical demand data
**Output**: Trained model + forecast predictions

### Layer 3: Analytics & Reporting

**Responsibility**: Generate business insights and visualizations

**Components**:
- `notebooks/eda.py` - Statistical analysis
- `sql/analysis.sql` - Database queries
- `reports/` - Generated charts

### Layer 4: Presentation

**Responsibility**: Interactive user interface

**Components**:
- `dashboard/app.py` - Streamlit application

---

## Component Design

### 1. Data Generator (`src/generate_data.py`)

**Purpose**: Generate realistic synthetic supply chain data

**Class Diagram**:
```
┌─────────────────────────────────────────────────────────┐
│                 DataGenerator                            │
├─────────────────────────────────────────────────────────┤
│ - categories: List[str]                                  │
│ - products: Dict[str, List[str]]                        │
│ - suppliers: List[str]                                   │
│ - regions: List[str]                                    │
│ - warehouses: List[str]                                  │
├─────────────────────────────────────────────────────────┤
│ + generate_supply_chain_data(num_records) → None         │
│ - _generate_products() → List[Tuple]                    │
│ - _generate_demand(date, category, product) → int       │
│ - _calculate_stock_status(inventory, reorder) → str    │
│ - _save_to_csv(df) → None                               │
└─────────────────────────────────────────────────────────┘
```

**Responsibilities**:
1. Define product taxonomy (categories → products)
2. Generate temporal data with seasonality patterns
3. Calculate derived fields (stock status, order quantity)
4. Persist to CSV with proper schema

**Configuration**:
```yaml
data:
  generation:
    num_records: 10000
    start_date: "2022-01-01"
    days_span: 730
    random_seed: 42
  products:
    Electronics: [Laptop, Smartphone, ...]
    Clothing: [T-Shirt, Jeans, ...]
```

### 2. Preprocessor (`src/preprocess.py`)

**Purpose**: Clean, validate, and engineer features from raw data

**ETL Pipeline**:
```
┌─────────────────────────────────────────────────────────────────┐
│                      ETL PIPELINE                               │
│                                                                 │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐      │
│  │  EXTRACT│───▶│ TRANSFORM│───▶│VALIDATE │───▶│  LOAD   │      │
│  │         │    │         │    │         │    │         │      │
│  │ Load    │    │ Clean   │    │ Schema  │    │ Export  │      │
│  │ CSV     │    │ Dedupe  │    │ Check   │    │ CSV     │      │
│  └─────────┘    │ Feature │    └─────────┘    └─────────┘      │
│                  │ Engineer│                                    │
│                  └─────────┘                                    │
└─────────────────────────────────────────────────────────────────┘
```

**Feature Engineering**:
| Feature | Formula | Description |
|---------|---------|-------------|
| `Inventory Turnover Ratio` | `Demand / (Inventory + ε)` | Measures inventory efficiency |
| `Days of Inventory Remaining` | `Inventory / Demand` | Days until stock-out |
| `Year` | `Date.dt.year` | Temporal extraction |
| `Month` | `Date.dt.month` | Seasonality detection |

### 3. Forecaster (`src/forecasting.py`)

**Purpose**: Train ML models and generate demand predictions

**Pipeline**:
```
┌─────────────────────────────────────────────────────────────────┐
│                    FORECASTING PIPELINE                         │
│                                                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │   AGGREGATE│─▶│   FEATURE   │─▶│    TRAIN    │             │
│  │             │  │   ENGINEER  │  │             │             │
│  │ Weekly      │  │ Lag features│  │ Linear      │             │
│  │ demand      │  │ L1, L2, L3  │  │ Regression  │             │
│  └─────────────┘  └─────────────┘  └──────┬──────┘             │
│                                           │                     │
│  ┌─────────────┐  ┌─────────────┐         │                    │
│  │   EVALUATE  │◀─│   PREDICT   │◀────────┘                    │
│  │             │  │             │                               │
│  │ MAE/RMSE    │  │ Next week   │                               │
│  │ comparison  │  │ forecasts   │                               │
│  └─────────────┘  └─────────────┘                               │
└─────────────────────────────────────────────────────────────────┘
```

**Model Details**:
- **Algorithm**: Linear Regression with lag features
- **Features**: 3-period lag variables (L1, L2, L3)
- **Train/Test Split**: 90/10 temporal split
- **Evaluation**: MAE (Mean Absolute Error)
- **Output**: Serialized model (.pkl) + forecast CSV

### 4. Dashboard (`dashboard/app.py`)

**Purpose**: Interactive visualization and business intelligence

**Page Structure**:
```
┌─────────────────────────────────────────────────────────────────┐
│  HEADER: Supply Chain & Inventory Analytics                    │
├─────────────────────────────────────────────────────────────────┤
│  SIDEBAR                    │  MAIN CONTENT                    │
│  ─────────                  │  ──────────────                   │
│  • Category filter          │  ┌─────────┬─────────┐           │
│  • Region filter           │  │ KPI 1   │ KPI 2   │           │
│  • Warehouse filter        │  ├─────────┼─────────┤           │
│  • Date range              │  │ KPI 3   │ KPI 4   │           │
│  • Quick stats             │  └─────────┴─────────┘           │
│                            │                                    │
│                            │  ┌──────────┬──────────┐          │
│                            │  │ Chart 1  │ Chart 2  │          │
│                            │  └──────────┴──────────┘          │
│                            │                                    │
│                            │  ┌────────────────────────┐        │
│                            │  │  Risk Analysis Table  │        │
│                            │  └────────────────────────┘        │
│                            │                                    │
│                            │  ┌────────────────────────┐        │
│                            │  │  Forecast Section     │        │
│                            │  └────────────────────────┘        │
└─────────────────────────────────────────────────────────────────┘
```

---

## Data Architecture

### Data Schema

**Raw Data (`data/raw/supply_chain_data.csv`)**:
| Column | Type | Description |
|--------|------|-------------|
| Date | datetime | Transaction date |
| Product ID | string | Unique product identifier |
| Product Name | string | Human-readable name |
| Category | string | Product category |
| Demand (Units Sold) | integer | Units sold |
| Inventory Level | integer | Current stock |
| Reorder Point | integer | Threshold for reorder |
| Lead Time (days) | integer | Supplier lead time |
| Supplier ID | string | Supplier identifier |
| Region | string | Sales region |
| Warehouse | string | Warehouse location |
| Stock Status | string | In Stock/Low Stock/Out of Stock |
| Order Quantity | integer | Order size |

**Processed Data (`data/processed/cleaned_supply_chain_data.csv`)**:
| Column | Type | Description |
|--------|------|-------------|
| [All raw columns] | ... | ... |
| Year | integer | Extracted year |
| Month | integer | Extracted month |
| Inventory Turnover Ratio | float | Engineered feature |
| Days of Inventory Remaining | float | Engineered feature |

**Forecast Output (`data/processed/forecast_outputs.csv`)**:
| Column | Type | Description |
|--------|------|-------------|
| Product ID | string | Product identifier |
| Forecasted_Demand_Next_Week | integer | Predicted demand |

### Data Flow

```
                    ┌─────────────────┐
                    │   YAML Config   │
                    └────────┬────────┘
                             │
         ┌───────────────────┼───────────────────┐
         │                   │                   │
         ▼                   ▼                   ▼
┌─────────────┐    ┌─────────────────┐    ┌─────────────┐
│  Generator  │    │  Preprocessor   │    │  Forecaster │
│              │    │                 │    │             │
│ Output:      │───▶│ Input: Raw CSV  │───▶│ Input:      │
│ Raw CSV      │    │ Output: Clean   │    │ Clean CSV   │
└─────────────┘    └─────────────────┘    └──────┬──────┘
                                                 │
                              ┌──────────────────┼──────────────────┐
                              │                  │                  │
                              ▼                  ▼                  ▼
                     ┌─────────────┐   ┌─────────────────┐  ┌──────────┐
                     │  EDA Tool   │   │  Model (pkl)    │  │ Forecast │
                     │             │   │                  │  │ CSV      │
                     │ Reports/    │   │ Serialized       │  │ Next     │
                     │ *.png       │   │ LinearRegression │  │ Week     │
                     └─────────────┘   └─────────────────┘  └────┬─────┘
                                                                  │
                                                                  ▼
                                                          ┌─────────────┐
                                                          │  Dashboard  │
                                                          │             │
                                                          │ UI Display  │
                                                          └─────────────┘
```

---

## ML Pipeline Architecture

### Feature Engineering

```
┌─────────────────────────────────────────────────────────────────┐
│                    FEATURE ENGINEERING                          │
│                                                                 │
│  Raw Demand Data                                                │
│       │                                                         │
│       ▼                                                         │
│  ┌─────────────────┐                                            │
│  │   Resample to   │  Weekly aggregation by Product ID        │
│  │   Weekly        │                                            │
│  └────────┬────────┘                                            │
│           │                                                     │
│           ▼                                                     │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐      │
│  │   Create Lags   │  │   Moving Avg    │  │   Target    │      │
│  │                 │  │                 │  │             │      │
│  │  Lag_1 = t-1    │  │  MA = avg(lags) │  │  Y = Demand │      │
│  │  Lag_2 = t-2    │  │                 │  │             │      │
│  │  Lag_3 = t-3    │  │                 │  │             │      │
│  └─────────────────┘  └─────────────────┘  └─────────────┘      │
│           │                   │                   │              │
│           └───────────────────┴───────────────────┘              │
│                             │                                     │
│                             ▼                                     │
│                     ┌──────────────┐                             │
│                     │ Feature Matrix│                             │
│                     │ [L1, L2, L3] │                             │
│                     └──────────────┘                             │
└─────────────────────────────────────────────────────────────────┘
```

### Model Training

```
┌─────────────────────────────────────────────────────────────────┐
│                     MODEL TRAINING                              │
│                                                                 │
│  Feature Matrix (X)          Target Vector (y)                 │
│  ┌─────────────────────┐      ┌─────────────────┐              │
│  │ L1    L2    L3     │      │ Weekly_Demand    │              │
│  ├─────────────────────┤      ├─────────────────┤              │
│  │ 120   115   110    │      │ 125              │              │
│  │ 125   120   115    │      │ 130              │              │
│  │ ...   ...   ...    │      │ ...              │              │
│  └─────────────────────┘      └─────────────────┘              │
│           │                           │                         │
│           └─────────────┬─────────────┘                         │
│                         ▼                                        │
│              ┌─────────────────────┐                            │
│              │  Linear Regression   │                            │
│              │                      │                            │
│              │  y = β₀ + β₁L₁       │                            │
│              │       + β₂L₂ + β₃L₃  │                            │
│              │                      │                            │
│              └──────────┬────────────┘                            │
│                         │                                         │
│          ┌──────────────┼──────────────┐                          │
│          ▼              ▼              ▼                          │
│   ┌────────────┐  ┌────────────┐  ┌────────────┐                │
│   │  Weights   │  │  Metrics  │  │  Serialize │                │
│   │            │  │           │  │            │                │
│   │ β₀, β₁...  │  │ MAE, RMSE │  │  .pkl file │                │
│   └────────────┘  └────────────┘  └────────────┘                │
└─────────────────────────────────────────────────────────────────┘
```

### Prediction

```
┌─────────────────────────────────────────────────────────────────┐
│                     PREDICTION PHASE                            │
│                                                                 │
│  Latest Week's Data                                             │
│       │                                                         │
│       ▼                                                         │
│  ┌─────────────────────────────────────────┐                   │
│  │        Create Forecast Features         │                   │
│  │                                         │                   │
│  │  Current: Demand = 125                   │                   │
│  │  Lag_1 = Previous Demand (120)          │                   │
│  │  Lag_2 = 2 weeks ago (115)              │                   │
│  │  Lag_3 = 3 weeks ago (110)               │                   │
│  └────────────────────┬────────────────────┘                    │
│                       │                                          │
│                       ▼                                          │
│              ┌─────────────────────┐                            │
│              │  Load Model (.pkl)  │                            │
│              └──────────┬──────────┘                            │
│                         │                                        │
│                         ▼                                        │
│              ┌─────────────────────┐                            │
│              │   Predict (predict) │                            │
│              │                      │                            │
│              │  y = 125.4           │                            │
│              │                      │                            │
│              └──────────┬──────────┘                            │
│                         │                                        │
│                         ▼                                        │
│              ┌─────────────────────┐                            │
│              │  Output: Next Week   │                            │
│              │  Forecast = 125      │                            │
│              └─────────────────────┘                            │
└─────────────────────────────────────────────────────────────────┘
```

---

## Application Architecture

### Streamlit Application Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    STREAMLIT APP FLOW                           │
│                                                                 │
│  ┌──────────────┐                                               │
│  │  Page Config │  set_page_config()                           │
│  │  CSS Injects │  Custom styling                              │
│  └──────┬───────┘                                               │
│         │                                                        │
│         ▼                                                        │
│  ┌──────────────┐                                               │
│  │  Load Data   │  @st.cache_data decorator                    │
│  │               │  - cleaned_supply_chain_data.csv            │
│  │               │  - forecast_outputs.csv                     │
│  └──────┬───────┘                                               │
│         │                                                        │
│         ▼                                                        │
│  ┌──────────────┐                                               │
│  │   Sidebar    │  Filter widgets                              │
│  │               │  - Category, Region, Warehouse               │
│  │               │  - Date range                               │
│  └──────┬───────┘                                               │
│         │                                                        │
│         ▼                                                        │
│  ┌──────────────┐                                               │
│  │ Apply Filters│  Pandas boolean masking                       │
│  └──────┬───────┘                                               │
│         │                                                        │
│         ▼                                                        │
│  ┌──────────────┐                                               │
│  │  Calculate   │  KPI computation                              │
│  │  KPIs        │  - Total demand, inventory, stock-out rate   │
│  └──────┬───────┘                                               │
│         │                                                        │
│         ▼                                                        │
│  ┌──────────────────────────────────────────┐                  │
│  │         Render Components                │                  │
│  │                                          │                  │
│  │  ┌──────────┐ ┌──────────┐              │                  │
│  │  │ Metrics  │ │ Charts   │              │                  │
│  │  │ (st.metric)│(plotly)  │              │                  │
│  │  └──────────┘ └──────────┘              │                  │
│  │  ┌──────────────────────────────┐     │                  │
│  │  │  Risk Analysis Table          │     │                  │
│  │  │  (st.dataframe)               │     │                  │
│  │  └──────────────────────────────┘     │                  │
│  │  ┌──────────────────────────────┐     │                  │
│  │  │  Forecast Display            │     │                  │
│  │  │  (st.dataframe + chart)      │     │                  │
│  │  └──────────────────────────────┘     │                  │
│  └──────────────────────────────────────────┘                  │
└─────────────────────────────────────────────────────────────────┘
```

### Module Interactions

```
┌─────────────────────────────────────────────────────────────────┐
│                    MODULE INTERACTIONS                          │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                     dashboard/app.py                     │  │
│  │                         │                                 │  │
│  │                     loads data                            │  │
│  │                         ▼                                 │  │
│  │  ┌─────────────────────────────────────────────────────┐│  │
│  │  │                    Streamlit UI                      ││  │
│  │  │   ┌─────────┐  ┌─────────┐  ┌─────────┐             ││  │
│  │  │   │ Filters │─▶│ KPIs    │─▶│ Charts  │             ││  │
│  │  │   └─────────┘  └─────────┘  └─────────┘             ││  │
│  │  └─────────────────────────────────────────────────────┘│  │
│  └──────────────────────────────────────────────────────────┘  │
│                             │                                    │
│         ┌───────────────────┼───────────────────┐              │
│         │                   │                   │              │
│         ▼                   ▼                   ▼              │
│  ┌────────────┐    ┌────────────────┐    ┌────────────┐        │
│  │  EDA Tool  │    │ Forecast CSV  │    │  ML Model │        │
│  │ (notebooks)│    │ (data/proc/)  │    │ (models/)  │        │
│  └────────────┘    └────────────────┘    └────────────┘        │
│        │                   │                   │              │
│        │                   │                   │              │
│        └───────────────────┴───────────────────┘              │
│                             │                                    │
│                             ▼                                    │
│                   ┌─────────────────┐                            │
│                   │  Python Scripts │                            │
│                   │  (src/)         │                            │
│                   └─────────────────┘                            │
└─────────────────────────────────────────────────────────────────┘
```

---

## Infrastructure Architecture

### Docker Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    DOCKER ARCHITECTURE                          │
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │                    Docker Host                            │ │
│  │                                                            │ │
│  │  ┌─────────────────────────────────────────────────────┐ │ │
│  │  │               supply-chain-analytics Container     │ │ │
│  │  │                                                     │ │ │
│  │  │  ┌─────────────────────────────────────────────┐   │ │ │
│  │  │  │              Streamlit App                  │   │ │ │
│  │  │  │              (Port 8501)                   │   │ │ │
│  │  │  └─────────────────────────────────────────────┘   │ │ │
│  │  │                      │                              │ │ │
│  │  │  ┌───────────────────┼───────────────────────┐     │ │ │
│  │  │  │                   │                       │     │ │ │
│  │  │  ▼                   ▼                       ▼     │ │ │
│  │  │ ┌─────┐         ┌──────┐           ┌────────┐   │ │ │
│  │  │ │ data│         │models│           │ reports │   │ │ │
│  │  │ │volume│        │volume│           │ volume  │   │ │ │
│  │  │ └─────┘         └──────┘           └────────┘   │ │ │
│  │  └─────────────────────────────────────────────────────┘ │ │
│  └───────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

### Docker Compose Architecture

```yaml
# docker-compose.yml structure
services:
  app:
    build: .
    ports:
      - "8501:8501"
    volumes:
      - ./data:/app/data
      - ./models:/app/models
      - ./reports:/app/reports
```

### Kubernetes Architecture (Future)

```
┌─────────────────────────────────────────────────────────────────┐
│               KUBERNETES ARCHITECTURE (PROPOSED)                │
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                     Kubernetes Cluster                    │  │
│  │                                                            │  │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐          │  │
│  │  │   Ingress  │  │  Service   │  │ ConfigMap  │          │  │
│  │  │  (NGINX)   │  │ (ClusterIP)│  │ (config)   │          │  │
│  │  └─────┬──────┘  └─────┬──────┘  └────────────┘          │  │
│  │        │               │                                  │  │
│  │        ▼               ▼                                  │  │
│  │  ┌─────────────────────────────────────────────────────┐  │  │
│  │  │                    Deployment                        │  │  │
│  │  │  ┌──────────────────────────────────────────────┐   │  │  │
│  │  │  │              Pod (supply-chain-app)         │   │  │  │
│  │  │  │  ┌────────────────────────────────────────┐  │   │  │  │
│  │  │  │  │  Container: supply-chain-analytics     │  │   │  │  │
│  │  │  │  │  - Streamlit App                       │  │   │  │  │
│  │  │  │  │  - Python Scripts                      │  │   │  │  │
│  │  │  │  └────────────────────────────────────────┘  │   │  │  │
│  │  │  └──────────────────────────────────────────────┘   │  │  │
│  │  │                                                      │  │  │
│  │  │  ┌──────────────────────────────────────────────┐   │  │  │
│  │  │  │              PVC (Persistent Volume)         │   │  │  │
│  │  │  │  - data/  - models/  - reports/              │   │  │  │
│  │  │  └──────────────────────────────────────────────┘   │  │  │
│  │  └─────────────────────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Security Architecture

### Application Security

```
┌─────────────────────────────────────────────────────────────────┐
│                   SECURITY ARCHITECTURE                         │
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                    Input Validation                        │  │
│  │                                                           │  │
│  │  • File existence checks before read                     │  │
│  │  • Date range validation                                  │  │
│  │  • Category/Region whitelist filtering                    │  │
│  │  • Numeric bounds checking                                │  │
│  └───────────────────────────────────────────────────────────┘  │
│                              │                                   │
│                              ▼                                   │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                   Data Protection                         │  │
│  │                                                           │  │
│  │  • .gitignore for sensitive files                         │  │
│  │  • .env.example for secrets                               │  │
│  │  • No credentials in source code                          │  │
│  │  • .dockerignore for build optimization                   │  │
│  └───────────────────────────────────────────────────────────┘  │
│                              │                                   │
│                              ▼                                   │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                   Dependencies                             │  │
│  │                                                           │  │
│  │  • Version pinning in requirements.txt                    │  │
│  │  • Regular security updates recommended                  │  │
│  │  • Minimal base image (python:3.9-slim)                   │  │
│  └───────────────────────────────────────────────────────────┘  │
```

### Environment Configuration

```yaml
# config.yaml - Non-sensitive configuration
database:
  type: sqlite
  path: "data/supply_chain.db"

# .env - Sensitive (not committed)
# DATABASE_URL=postgresql://user:pass@host:5432/db
# API_KEY=your-secret-key
```

---

## Version Compatibility Matrix

| Component | Version | Notes |
|-----------|---------|-------|
| Python | 3.9+ | Minimum 3.9 required |
| pandas | >=2.0.0 | Data manipulation |
| numpy | >=1.24.0 | Numerical computing |
| scikit-learn | >=1.3.0 | ML framework |
| streamlit | >=1.28.0 | Dashboard UI |
| plotly | >=5.18.0 | Charts |
| pyyaml | >=6.0 | Config parsing |

---

## Performance Considerations

| Aspect | Current | Optimization |
|--------|---------|--------------|
| Data Loading | CSV on-demand | @st.cache_data |
| Model Loading | Lazy load | Cached at startup |
| Large Datasets | Pandas | Consider Dask/Spark |
| Dashboard | Single instance | Consider Gunicorn |

---

## Error Handling

| Component | Strategy |
|-----------|----------|
| Data Generation | Graceful fallback, logging |
| Preprocessing | File existence check + informative error |
| Forecasting | Try-except around model load |
| Dashboard | st.warning for missing data |

---

## Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| "Data not found" | Run: `python src/generate_data.py && python src/preprocess.py` |
| "Model not found" | Run: `python src/forecasting.py` |
| Port 8501 in use | Change port: `streamlit run app.py --server.port 8502` |
| Import errors | Install requirements: `pip install -r requirements.txt` |

---

*Last Updated: April 2026*
*Version: 1.0.0*
*Maintainer: Logesh Kannan*