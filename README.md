# Supply Chain & Inventory Analytics Platform

<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=0:302b63,100:24243e&height=200&section=header&text=Supply%20Chain%20Analytics&fontSize=60&animation=fadeIn&fontAlignY=35" width="100%"/>
</p>

<div align="center">

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-3DA65A?style=for-the-badge)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)

**Enterprise-grade supply chain analytics platform for demand forecasting and inventory optimization**

[📚 Documentation](ARCHITECTURE.md) · [🚀 Quick Start](#getting-started) · [🐳 Docker](#docker-deployment) · [🤝 Contribute](CONTRIBUTING.md) · [📄 License](LICENSE)

</div>

---

## Overview

An end-to-end data analytics solution that transforms raw supply chain data into actionable business insights through machine learning forecasting and interactive visualization. Built with enterprise-grade practices for production-ready deployment.

### Why This Platform?

| Traditional Approach | Our Platform |
|---------------------|--------------|
| Manual spreadsheets | Automated ETL pipeline |
| Reactive inventory | Proactive ML forecasting |
| Static reports | Real-time Streamlit dashboard |
| Siloed analysis | Integrated analytics workflow |

---

## Key Features

| Feature | Description |
|---------|-------------|
| **Data Pipeline** | Synthetic data generation with seasonality, automated ETL, feature engineering |
| **ML Forecasting** | Linear Regression with lag features, model serialization, MAE < 90 units |
| **Interactive Dashboard** | KPIs, trend charts, risk alerts, demand forecasts, dynamic filtering |
| **SQL Analytics** | Pre-built queries for demand analysis, stock-out tracking, supplier metrics |
| **Docker Ready** | Production containerization with Docker Compose |
| **CI/CD** | Automated GitHub Actions workflow |

---

## Architecture

```
┌────────────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER                         │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │              Streamlit Dashboard (Port 8501)            │ │
│  │   KPIs │ Charts │ Risk Alerts │ Forecasts │ Filters     │ │
│  └──────────────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌────────────────────────────────────────────────────────────────┐
│                     APPLICATION LAYER                         │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐     │
│  │ Generate │  │Preprocess│  │ Forecast │  │   EDA    │     │
│  │  Data    │  │  (ETL)   │  │   (ML)   │  │          │     │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘     │
└────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌────────────────────────────────────────────────────────────────┐
│                       DATA LAYER                               │
│  ┌────────┐  ┌──────────┐  ┌────────┐  ┌────────┐           │
│  │  Raw   │  │Processed│  │ Models │  │Reports │           │
│  │  CSV   │  │   CSV   │  │ (*.pkl)│  │ (*.png)│           │
│  └────────┘  └──────────┘  └────────┘  └────────┘           │
└────────────────────────────────────────────────────────────────┘
```

### Data Flow

```
config.yaml → generate_data.py → data/raw/
                                     ↓
                               preprocess.py → data/processed/
                                     ↓                    ↓
                               forecasting.py → models/    notebooks/eda.py
                                     ↓                    ↓
                               forecast_outputs.csv    reports/
                                     ↓
                               dashboard/app.py
```

---

## Getting Started

### Prerequisites

| Requirement | Version |
|-------------|---------|
| Python | 3.9+ |
| pip | Latest |
| Docker | 20.10+ (optional) |

### Installation

```bash
# Clone repository
git clone https://github.com/logeshkannan19/Supply-Chain-Inventory-Analytics-for-Demand-Forecasting.git
cd Supply-Chain-Inventory-Analytics-for-Demand-Forecasting

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt
```

### Run Pipeline

```bash
# Generate synthetic data
python src/generate_data.py

# Preprocess and engineer features
python src/preprocess.py

# Train model and generate forecasts
python src/forecasting.py

# Generate EDA visualizations
python notebooks/eda.py
```

### Launch Dashboard

```bash
streamlit run dashboard/app.py
```

🌐 **Open http://localhost:8501**

---

## Tech Stack

| Category | Technology |
|----------|------------|
| Language | Python 3.9+ |
| Data Processing | Pandas, NumPy |
| Visualization | Plotly, Matplotlib, Seaborn |
| Machine Learning | scikit-learn, joblib |
| Dashboard | Streamlit |
| Configuration | PyYAML |
| Containerization | Docker, Docker Compose |
| CI/CD | GitHub Actions |

---

## Configuration

Edit `config.yaml` to customize:

```yaml
data:
  generation:
    num_records: 10000
    start_date: "2022-01-01"
    random_seed: 42

forecasting:
  model_type: linear_regression
  lags: [1, 2, 3]
  train_test_split: 0.9

dashboard:
  title: "Supply Chain Analytics"
  layout: "wide"
```

---

## Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up --build

# Access at http://localhost:8501
```

### Manual Build

```bash
docker build -t supply-chain-analytics .
docker run -p 8501:8501 supply-chain-analytics
```

---

## Project Structure

```
SupplyChainAnalytics/
├── src/                    # Core modules
│   ├── generate_data.py    # Data generation
│   ├── preprocess.py       # ETL pipeline
│   └── forecasting.py      # ML forecasting
├── dashboard/              # Streamlit UI
│   └── app.py              # Dashboard
├── models/                 # Trained models
│   └── lr_demand_model.pkl
├── data/                   # Data storage
│   ├── raw/               # Raw data
│   └── processed/         # Clean data
├── notebooks/             # EDA scripts
├── sql/                   # SQL queries
├── reports/               # Generated charts
├── .github/workflows/     # CI/CD
├── config.yaml            # Configuration
├── Dockerfile             # Container build
└── docker-compose.yml     # Orchestration
```

---

## Roadmap

### v1.0.0 (Current)
- ✅ Synthetic data generation
- ✅ ETL pipeline
- ✅ Linear Regression forecasting
- ✅ Streamlit dashboard
- ✅ Docker support
- ✅ CI/CD pipeline

### Upcoming
| Version | Features |
|---------|----------|
| v1.1.0 | PostgreSQL, SQLAlchemy |
| v1.2.0 | Prophet, ARIMA |
| v2.0.0 | Supplier prediction, alerts |

---

## Contributing

Contributions welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

```bash
# Fork, create branch, make changes, submit PR
git checkout -b feature/your-feature
```

---

## License

MIT License - see [LICENSE](LICENSE)

---

## Support

- 📖 [Documentation](ARCHITECTURE.md)
- 🐛 [Issues](https://github.com/logeshkannan19/Supply-Chain-Inventory-Analytics-for-Demand-Forecasting/issues)
- 💬 [Discussions](https://github.com/logeshkannan19/Supply-Chain-Inventory-Analytics-for-Demand-Forecasting/discussions)

---

<p align="center">
  <sub>Built with ❤️ by <a href="https://github.com/logeshkannan19">Logesh Kannan</a></sub>
</p>