# Supply Chain & Inventory Analytics Platform

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/License-MIT-3DA65A?style=for-the-badge" alt="License">
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit">
  <img src="https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white" alt="scikit-learn">
  <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker">
</p>

> **Enterprise-grade supply chain analytics solution for demand forecasting and inventory optimization**

---

## 📋 Overview

This platform delivers an end-to-end data analytics solution designed to analyze demand patterns, optimize inventory levels, and improve supply chain efficiency. The complete pipeline ingests data, engineers features, trains forecasting models, and serves actionable insights through an interactive Streamlit dashboard.

### Key Capabilities

| Capability | Description |
|------------|-------------|
| **Data Generation** | Synthetic supply chain data with realistic seasonality, product categories, and supplier metrics |
| **ETL Pipeline** | Automated data cleaning, preprocessing, and feature engineering |
| **Demand Forecasting** | ML-based predictions using Linear Regression with lag features |
| **Interactive Dashboard** | Real-time inventory monitoring with risk alerts and forecasting |
| **SQL Analytics** | Pre-built queries for supply chain analysis |

---

## 🏗️ Architecture

```
SupplyChainAnalytics/
├── data/                      # Data storage
│   ├── raw/                   # Raw synthetic data
│   └── processed/             # Cleaned data and features
├── src/                       # Core modules
│   ├── generate_data.py       # Data generation engine
│   ├── preprocess.py          # ETL pipeline
│   └── forecasting.py         # ML forecasting module
├── dashboard/                 # Streamlit UI
│   └── app.py                 # Dashboard application
├── models/                    # Trained models
│   └── lr_demand_model.pkl    # Linear Regression model
├── notebooks/                 # Analysis notebooks
│   └── eda.py                 # EDA visualizations
├── sql/                       # SQL queries
│   └── analysis.sql          # Analytical queries
├── reports/                   # Generated reports
├── config.yaml                # Configuration management
├── Dockerfile                 # Container definition
└── docker-compose.yml         # Multi-container orchestration
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.9 or higher
- pip or poetry package manager
- Docker (optional, for containerized deployment)

### Installation

```bash
# Clone the repository
git clone https://github.com/logeshkannan19/Supply-Chain-Inventory-Analytics-for-Demand-Forecasting.git
cd Supply-Chain-Inventory-Analytics-for-Demand-Forecasting

# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate        # Linux / macOS
# venv\Scripts\activate         # Windows

# Install dependencies
pip install -r requirements.txt
```

### Running the Pipeline

```bash
# Step 1: Generate synthetic data
python src/generate_data.py

# Step 2: Preprocess and engineer features
python src/preprocess.py

# Step 3: Train forecasting model
python src/forecasting.py

# Step 4: Generate EDA visualizations
python notebooks/eda.py
```

### Launch Dashboard

```bash
streamlit run dashboard/app.py
```

Access the dashboard at: **`http://localhost:8501`**

---

## 📊 Tech Stack

| Category | Technology |
|----------|------------|
| **Language** | Python 3.9+ |
| **Data Processing** | Pandas, NumPy |
| **Visualization** | Matplotlib, Seaborn, Plotly |
| **Machine Learning** | scikit-learn, joblib |
| **Dashboard** | Streamlit |
| **Database** | PostgreSQL (via SQLAlchemy) |
| **Containerization** | Docker, Docker Compose |

---

## 📈 Key Metrics

| Metric | Target |
|--------|--------|
| Stock-Out Detection | Real-time monitoring |
| Forecast Accuracy | MAE < 90 units/week |
| Inventory Optimization | Turnover ratio tracking |

---

## ⚙️ Configuration

Customize the application by editing `config.yaml`:

- **Data Generation**: Number of records, date range, products, suppliers
- **Forecasting**: Model type, lag features, train-test split
- **Dashboard**: KPIs, charts, default filters
- **Database**: Connection settings (for production use)

---

## 🐳 Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up --build

# Access at http://localhost:8501
```

### Manual Docker Build

```bash
docker build -t supply-chain-analytics .
docker run -p 8501:8501 supply-chain-analytics
```

---

## 📂 Project Structure

| Directory | Purpose |
|-----------|---------|
| `src/` | Core data processing and ML modules |
| `dashboard/` | Streamlit web application |
| `models/` | Trained ML models |
| `notebooks/` | Exploratory data analysis |
| `sql/` | SQL analytical queries |
| `reports/` | Generated visualizations |
| `config.yaml` | Centralized configuration |

---

## 🤝 Contributing

Contributions are welcome! Please review our [Contributing Guidelines](CONTRIBUTING.md) for details on how to submit pull requests, report issues, and follow the code of conduct.

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 📋 Roadmap

For planned features and improvements, see the [Project Roadmap](ROADMAP.md).

---

## 🔐 Security

For security vulnerabilities, please review our [Security Policy](SECURITY.md).

---

<p align="center">
  <sub>Built with ❤️ by <a href="https://github.com/logeshkannan19">Logesh Kannan</a></sub>
</p>