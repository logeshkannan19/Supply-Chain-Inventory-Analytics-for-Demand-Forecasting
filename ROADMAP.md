# Project Roadmap

This document outlines the planned development roadmap for the Supply Chain & Inventory Analytics project.

## Version History

| Version | Status | Description |
|---------|--------|-------------|
| 1.0.0 | ✅ Current | Baseline release with Linear Regression forecasting |

---

## Phase 1: Foundation (Completed ✅)

### v1.0.0 - Initial Release

- [x] Synthetic data generation with seasonality
- [x] ETL pipeline for data preprocessing
- [x] Linear Regression demand forecasting
- [x] Streamlit dashboard with filtering
- [x] SQL analysis queries
- [x] EDA visualizations

---

## Phase 2: Database Integration (Q2 2024)

### v1.1.0 - Database Support

- [ ] Replace CSV with PostgreSQL database
- [ ] Add SQLAlchemy ORM layer
- [ ] Implement connection pooling
- [ ] Add database migration scripts
- [ ] Connection string configuration via config.yaml

**Milestones:**
1. Design database schema
2. Create SQLAlchemy models
3. Migrate existing ETL to use database
4. Add connection health checks

---

## Phase 3: Advanced Forecasting (Q3 2024)

### v1.2.0 - Time Series Models

- [ ] Implement Facebook Prophet for demand forecasting
- [ ] Add ARIMA/SARIMA models
- [ ] Create model selection framework
- [ ] Add cross-validation for time series
- [ ] Compare model performance in dashboard

**Milestones:**
1. Integrate Prophet library
2. Create model training pipeline
3. Build model comparison UI
4. Add auto-selection of best model

---

## Phase 4: Cloud Deployment (Q4 2024)

### v1.3.0 - Production Ready

- [ ] Docker containerization
- [ ] Docker Compose for local development
- [ ] GitHub Actions CI/CD pipeline
- [ ] AWS/GCP deployment templates
- [ ] Kubernetes manifests

**Milestones:**
1. Optimize Docker image size
2. Add health check endpoints
3. Create deployment documentation
4. Setup monitoring and logging

---

## Phase 5: AI & Automation (2025)

### v2.0.0 - Intelligent Supply Chain

- [ ] Supplier delay prediction model
- [ ] Dynamic pricing suggestions
- [ ] Automated reorder alerts (Slack/Discord)
- [ ] Natural language queries
- [ ] Anomaly detection

**Milestones:**
1. Train classification models
2. Build notification system
3. Integrate LLM for queries
4. Add real-time alerts

---

## Feature Backlog

### High Priority

- [ ] Unit tests for all modules
- [ ] API wrapper for dashboard
- [ ] Export to Excel/PDF reports
- [ ] User authentication

### Medium Priority

- [ ] Multi-language support
- [ ] Dark mode theme
- [ ] Dashboard theming
- [ ] Email report scheduling

### Low Priority

- [ ] Mobile-responsive dashboard
- [ ] WebSocket for real-time updates
- [ ] Custom branding options
- [ ] Plugin system for extensions

---

## Technology Stack Evolution

| Component | Current | Future |
|-----------|---------|--------|
| Database | CSV | PostgreSQL |
| ML | scikit-learn | Prophet, XGBoost |
| Dashboard | Streamlit | React + FastAPI |
| Deployment | Manual | Kubernetes |

---

## Contributing to Roadmap

To propose new features:
1. Open an issue with the `feature-request` label
2. Provide use case and implementation ideas
3. Include mockups if applicable
4. Tag for appropriate milestone

---

## Notes

- Timeline is subject to change based on community feedback and resources
- Priority order may shift based on user requirements
- Major version bumps indicate breaking changes