# Project Roadmap

This roadmap outlines the planned future capabilities and enhancements for the Supply Chain & Inventory Analytics system.

## Phase 1: Foundation (Current)
- [x] End-to-end data pipeline abstraction.
- [x] Synthetic data generation capturing robust seasonality.
- [x] Streamlit Executive Dashboard with filtering.
- [x] Baseline Statistical Forecasting (Linear Regression).

## Phase 2: System Upgrades
- [ ] **Database Integration**: Deprecate CSV file-saving in favor of SQLAlchemy connections pushing to PostgreSQL.
- [ ] **Advanced Forecasting**: Implement `Prophet` or `ARIMA` dedicated time-series forecasting. 
- [ ] **Cloud Deployment**: Package the system into a Docker image and provide templates for AWS Fargate/GCP Cloud Run deployment.

## Phase 3: Advanced Intelligence
- [ ] **Supplier Delay AI**: Implement classification models predicting the probability of supplier shipment delays based on geographic region and historical lead times.
- [ ] **Dynamic Pricing Alerts**: Suggest temporary pricing modifications to mitigate immediate Stock-Out risks.
- [ ] **Automated Reordering**: Generate email or webhook alerts (via Slack/Discord) autonomously when items hit critical threshold limits.
