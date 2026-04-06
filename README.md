<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&height=300&section=header&text=Supply%20Chain%20Analytics&fontSize=80&animation=fadeIn&fontAlignY=35" width="100%"/>
</p>

<div align="center">

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-3DA65A?style=for-the-badge)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)

**Enterprise-grade supply chain analytics platform for demand forecasting and inventory optimization**

[📚 Documentation](https://github.com/logeshkannan19/Supply-Chain-Inventory-Analytics-for-Demand-Forecasting/wiki) •
[🚀 Quick Start](#-getting-started) •
[🐳 Docker](#-docker-deployment) •
[🤝 Contribute](CONTRIBUTING.md) •
[📄 License](LICENSE)

</div>

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Key Features](#key-features)
3. [Architecture](#architecture)
4. [Getting Started](#getting-started)
5. [Tech Stack](#tech-stack)
6. [Configuration](#configuration)
7. [Docker Deployment](#docker-deployment)
8. [Project Structure](#project-structure)
9. [Roadmap](#roadmap)
10. [Contributing](#contributing)
11. [License](#license)

---

## Overview

Supply Chain & Inventory Analytics is a comprehensive, end-to-end data analytics solution designed to transform raw supply chain data into actionable business insights. Built with enterprise-grade practices, this platform enables organizations to:

- **Analyze demand patterns** across product categories, regions, and time periods
- **Optimize inventory levels** through data-driven forecasting and risk analysis
- **Improve supply chain efficiency** with real-time monitoring and alerts
- **Make informed decisions** with interactive visualizations and KPIs

### Why This Platform?

| Traditional Approach | Our Platform |
|---------------------|---------------|
| Manual data entry & spreadsheets | Automated ETL pipeline |
| Reactive inventory management | Proactive demand forecasting |
| Static reports | Interactive real-time dashboard |
| Siloed data analysis | Integrated analytics workflow |

---

## Key Features

### 🔄 Data Pipeline

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Generate  │───▶│   Clean     │───▶│   Feature   │───▶│   Export    │
│   Raw Data  │    │   & Dedupe  │    │   Engineer │    │   to CSV    │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
```

- **Synthetic Data Generation**: Realistic supply chain data with seasonality patterns
- **Automated ETL**: Data cleaning, deduplication, and transformation
- **Feature Engineering**: Inventory turnover ratio, days of stock remaining

### 🤖 Machine Learning

- **Linear Regression** with 3-period lag features
- **Moving Average** baseline comparison
- **Model Serialization** via joblib for reproducibility
- **Weekly Demand Forecasting** with MAE < 90 units

### 📊 Interactive Dashboard

| Component | Description |
|-----------|-------------|
| **Executive KPIs** | Total demand, inventory levels, stock-out rate, turnover |
| **Trend Charts** | Demand vs inventory over time |
| **Risk Analysis** | Low inventory alerts with risk levels |
| **Forecasts** | Next week demand predictions |
| **Filters** | Category, region, warehouse, date range |

### 🛢️ SQL Analytics

Pre-built analytical queries for:
- Product & category demand analysis
- Monthly trend aggregation
- Warehouse inventory tracking
- Stock-out frequency analysis
- Supplier performance metrics

---

## Architecture

### High-Level System Design

```
┌────────────────────────────────────────────────────────────────────────────┐
│                              PRESENTATION LAYER                             │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                    Streamlit Dashboard                               │  │
│  │   ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐      │  │
│  │   │ KPIs    │ │ Charts  │ │ Tables  │ │ Filters │ │ Alerts  │      │  │
│  │   └─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘      │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────────────────┘
                                       │
                                       ▼
┌────────────────────────────────────────────────────────────────────────────┐
│                              APPLICATION LAYER                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │   Generate   │  │  Preprocess  │  │  Forecast    │  │     EDA     │   │
│  │    Data      │  │    (ETL)    │  │    (ML)      │  │  (Analysis) │   │
│  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘   │
└────────────────────────────────────────────────────────────────────────────┘
                                       │
                                       ▼
┌────────────────────────────────────────────────────────────────────────────┐
│                                DATA LAYER                                  │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐      │
│  │   Raw CSV   │  │  Processed  │  │   Models    │  │   Reports   │      │
│  │  (data/raw) │  │     CSV     │  │  (*.pkl)    │  │   (*.png)   │      │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘      │
└────────────────────────────────────────────────────────────────────────────┘
```

### Component Flow

```
                    ┌──────────────────┐
                    │   config.yaml   │
                    └────────┬─────────┘
                             │
         ┌───────────────────┼───────────────────┐
         │                   │                   │
         ▼                   ▼                   ▼
┌────────────────┐  ┌────────────────┐  ┌────────────────┐
│ Data Generator │  │  Preprocessor │  │   Forecaster  │
│                │  │                │  │                │
│ • Products     │  │ • Clean       │  │ • Lag Features │
│ • Suppliers    │  │ • Dedupe      │  │ • Train Model  │
│ • Seasonality  │  │ • Engineer    │  │ • Evaluate     │
│ • Lead Times   │  │ • KPIs        │  │ • Predict      │
└───────┬────────┘  └───────┬────────┘  └───────┬────────┘
        │                   │                   │
        ▼                   ▼                   ▼
   data/raw/          data/processed/        models/
   supply_chain      cleaned_supply_        lr_demand
   _data.csv         chain_data.csv        _model.pkl
                                              │
                                              ▼
                                    data/processed/
                                    forecast_outputs.csv
```

---

## Getting Started

### Prerequisites

| Requirement | Version | Notes |
|-------------|---------|-------|
| Python | 3.9+ | Required |
| pip | Latest | Package manager |
| Docker | 20.10+ | Optional |

### Local Installation

```bash
# 1. Clone the repository
git clone https://github.com/logeshkannan19/Supply-Chain-Inventory-Analytics-for-Demand-Forecasting.git
cd Supply-Chain-Inventory-Analytics-for-Demand-Forecasting

# 2. Create virtual environment
python -m venv venv

# 3. Activate environment
source venv/bin/activate        # Linux/macOS
venv\Scripts\activate          # Windows

# 4. Install dependencies
pip install -r requirements.txt
```

### Run the Pipeline

```bash
# Generate synthetic data (10,000 records)
python src/generate_data.py

# Preprocess and engineer features
python src/preprocess.py

# Train ML model and generate forecasts
python src/forecasting.py

# Generate EDA visualizations
python notebooks/eda.py
```

### Launch Dashboard

```bash
streamlit run dashboard/app.py
```

🌐 **Open http://localhost:8501 in your browser**

---

## Tech Stack

### Core Technologies

| Layer | Technology | Purpose |
|-------|------------|---------|
| **Language** | Python 3.9+ | Primary development language |
| **Data Processing** | Pandas, NumPy | Data manipulation & numerical computing |
| **Visualization** | Matplotlib, Seaborn, Plotly | Charts and dashboards |
| **Machine Learning** | scikit-learn, joblib | Demand forecasting |
| **Dashboard** | Streamlit | Interactive web UI |
| **Configuration** | PyYAML | Centralized settings |
| **Containerization** | Docker, Docker Compose | Deployment |

### Development Tools

| Tool | Purpose |
|------|---------|
| Git | Version control |
| GitHub Actions | CI/CD pipeline |
| Black | Code formatting |
| Flake8 | Linting |
| MyPy | Type checking |

---

## Configuration

Customize the platform via `config.yaml`:

### Data Generation

```yaml
data:
  generation:
    num_records: 10000
    start_date: "2022-01-01"
    days_span: 730
    random_seed: 42
```

### Forecasting

```yaml
forecasting:
  model_type: linear_regression
  lags: [1, 2, 3]
  train_test_split: 0.9
```

### Dashboard

```yaml
dashboard:
  title: "Supply Chain Analytics"
  layout: "wide"
  kpis:
    - total_demand
    - current_inventory
    - stock_out_rate
```

---

## Docker Deployment

### Using Docker Compose (Recommended)

```bash
# Build and start containers
docker-compose up --build

# Access dashboard
open http://localhost:8501
```

### Manual Docker Build

```bash
# Build image
docker build -t supply-chain-analytics .

# Run container
docker run -p 8501:8501 supply-chain-analytics
```

### Docker Compose with PostgreSQL

```yaml
# Uncomment in docker-compose.yml
services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: supply_chain
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: admin
    volumes:
      - db_data:/var/lib/postgresql/data
```

---

## Project Structure

```
SupplyChainAnalytics/
│
├── 📂 src/                          # Core modules
│   ├── generate_data.py             # Data generation
│   ├── preprocess.py                # ETL pipeline
│   └── forecasting.py               # ML forecasting
│
├── 📂 dashboard/                    # Streamlit UI
│   └── app.py                       # Dashboard application
│
├── 📂 models/                       # Trained models
│   └── lr_demand_model.pkl          # Linear Regression
│
├── 📂 data/                         # Data storage
│   ├── raw/                         # Raw data
│   └── processed/                   # Clean data + forecasts
│
├── 📂 notebooks/                    # Analysis
│   └── eda.py                       # EDA visualizations
│
├── 📂 sql/                          # SQL queries
│   └── analysis.sql                 # Analytical queries
│
├── 📂 reports/                      # Generated reports
│
├── 📂 .github/workflows/            # CI/CD
│   └── ci.yml                       # GitHub Actions
│
├── 📄 config.yaml                   # Configuration
├── 📄 Dockerfile                    # Container build
├── 📄 docker-compose.yml             # Container orchestration
├── 📄 pyproject.toml                # Package metadata
└── 📄 requirements.txt              # Dependencies
```

---

## Roadmap

### Completed (v1.0.0)

- ✅ Synthetic data generation with seasonality
- ✅ ETL pipeline with feature engineering
- ✅ Linear Regression demand forecasting
- ✅ Interactive Streamlit dashboard
- ✅ Docker containerization
- ✅ GitHub Actions CI/CD

### Upcoming Features

| Version | Features |
|---------|----------|
| **v1.1.0** | PostgreSQL integration, SQLAlchemy ORM |
| **v1.2.0** | Prophet/ARIMA forecasting, model comparison |
| **v2.0.0** | Supplier delay prediction, automated alerts |

See [ROADMAP.md](ROADMAP.md) for detailed milestones.

---

## Contributing

We welcome contributions! Please read our [Contributing Guidelines](CONTRIBUTING.md) for:

- Code of conduct
- Development setup
- Coding standards
- Pull request process

### Quick Contribution Steps

```bash
# 1. Fork the repository
# 2. Create feature branch
git checkout -b feature/your-feature

# 3. Make changes and test
python src/generate_data.py
python src/preprocess.py
python src/forecasting.py

# 4. Commit and push
git commit -m "feat: add new feature"
git push origin feature/your-feature

# 5. Create Pull Request
```

---

## License

This project is licensed under the **MIT License** - see [LICENSE](LICENSE) for details.

---

## Support

- 📖 [Documentation](https://github.com/logeshkannan19/Supply-Chain-Inventory-Analytics-for-Demand-Forecasting/wiki)
- 🐛 [Issue Tracker](https://github.com/logeshkannan19/Supply-Chain-Inventory-Analytics-for-Demand-Forecasting/issues)
- 💬 [Discussions](https://github.com/logeshkannan19/Supply-Chain-Inventory-Analytics-for-Demand-Forecasting/discussions)

---

<p align="center">
  <sub>Built with ❤️ by <a href="https://github.com/logeshkannan19">Logesh Kannan</a></sub>
</p>

<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&height=100&section=footer" width="100%"/>
</p>