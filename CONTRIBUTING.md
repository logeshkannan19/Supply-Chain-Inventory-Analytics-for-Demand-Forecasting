# Contributing to Supply Chain Analytics

Thank you for your interest in contributing to this project!

## Code of Conduct

Please be respectful and professional in all interactions. We follow the [Contributor Covenant](https://www.contributor-covenant.org/) code of conduct.

## How to Contribute

### 1. Reporting Issues

- Check if the issue already exists in the issue tracker
- Create a detailed issue with:
  - Clear title and description
  - Steps to reproduce (if applicable)
  - Expected vs actual behavior
  - Screenshots or error messages

### 2. Feature Requests

- Open an issue with the `enhancement` label
- Describe the feature and its use case
- Provide any mockups or examples if possible

### 3. Pull Requests

#### Process

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make your changes following the style guide
4. Add tests if applicable
5. Commit with clear, descriptive messages
6. Push to your fork and create a Pull Request

#### Branch Naming

- `feature/` - New features
- `fix/` - Bug fixes
- `refactor/` - Code refactoring
- `docs/` - Documentation updates

#### Commit Messages

Use clear, descriptive commit messages:
- `feat: add Prophet forecasting model`
- `fix: resolve stock risk calculation bug`
- `docs: update API documentation`

### 4. Development Setup

```bash
# Clone and setup
git clone https://github.com/logeshkannan19/Supply-Chain-Inventory-Analytics-for-Demand-Forecasting.git
cd Supply-Chain-Inventory-Analytics-for-Demand-Forecasting

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the pipeline
python src/generate_data.py
python src/preprocess.py
python src/forecasting.py

# Launch dashboard
streamlit run dashboard/app.py
```

### 5. Coding Standards

- **Python**: Follow PEP 8
- **Type Hints**: Use type annotations for function parameters and return types
- **Docstrings**: Use Google-style docstrings for all public functions
- **Testing**: Add unit tests for new features

#### Example Docstring

```python
def calculate_turnover_ratio(demand: int, inventory: int) -> float:
    """Calculate inventory turnover ratio.

    Args:
        demand: Total units sold
        inventory: Current inventory level

    Returns:
        Turnover ratio as a float

    Raises:
        ValueError: If inventory is zero or negative
    """
    if inventory <= 0:
        raise ValueError("Inventory must be positive")
    return demand / inventory
```

### 6. Project Structure

```
SupplyChainAnalytics/
├── src/              # Core modules
├── dashboard/        # Streamlit UI
├── notebooks/        # EDA scripts
├── models/           # Trained models
├── data/             # Data files
├── reports/          # Generated reports
└── sql/              # SQL queries
```

### 7. Testing

Run tests before submitting a PR:

```bash
# Run all scripts to ensure they work
python src/generate_data.py
python src/preprocess.py
python src/forecasting.py

# Run linting
flake8 src/
black --check src/
```

### 8. Review Process

- All PRs require at least one review
- Address feedback promptly
- Ensure CI passes before merging

## Questions?

If you have questions, feel free to open a discussion or reach out to the maintainers.

## Recognition

Contributors will be recognized in the README and project's contributors page.