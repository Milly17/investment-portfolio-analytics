# Investment Portfolio Performance Analytics

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## 📊 Project Overview

This project provides a comprehensive analysis of investment portfolio performance across different market conditions. It helps investors optimize their asset allocation strategies based on risk profiles and changing economic environments.

### 🔍 Problem Statement

Investors struggle to understand how different asset allocation strategies perform across various market conditions, leading to suboptimal investment decisions. This project analyzes historical performance data to identify optimal portfolio allocations for different risk profiles and market environments, providing actionable insights for investment strategy optimization.

## 🚀 Features

- **Data Integration Pipeline**: Collects and merges financial data from Yahoo Finance, FRED, World Bank, and Fama-French datasets
- **Market Regime Classification**: Identifies different market environments (bull, bear, recovery, high volatility)
- **Portfolio Construction Models**:
  - Equal-weight and market-cap-weight allocations
  - Markowitz mean-variance optimization
  - Risk parity implementation
  - Factor-based portfolio construction
- **Performance Analytics**:
  - Risk-adjusted return metrics (Sharpe, Sortino, Calmar ratios)
  - Drawdown analysis and recovery periods
  - Factor attribution
  - Correlation analysis across market regimes
- **Interactive Visualizations**:
  - Efficient frontier plots
  - Performance comparison dashboards
  - Risk decomposition charts
  - Factor exposure heatmaps

## 🛠️ Technology Stack

- **Core**: Python, Pandas, NumPy
- **Data Sources**: yfinance, fredapi, wbdata
- **Optimization**: scipy, cvxpy
- **Statistical Analysis**: statsmodels, scikit-learn
- **Visualization**: Matplotlib, Seaborn, Plotly
- **Interactive Dashboard**: Streamlit
- **Testing**: pytest

## 🔧 Installation & Usage

### Prerequisites

- Python 3.8+
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/your-username/investment-portfolio-analytics.git
cd investment-portfolio-analytics

# Set up a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Running the Analysis

```bash
# Run data collection
python src/data/collect_data.py

# Execute the portfolio analysis
python src/models/run_analysis.py

# Launch the interactive dashboard
streamlit run dashboard/app.py
```

## 📋 Project Structure

```
investment-portfolio-analytics/
├── data/
│   ├── raw/                # Original data from APIs
│   ├── processed/          # Cleaned and aligned data
│   └── external/           # External reference data (benchmarks)
├── notebooks/              # Exploratory Jupyter notebooks
│   ├── 01_data_exploration.ipynb
│   ├── 02_feature_engineering.ipynb
│   ├── 03_baseline_models.ipynb
│   └── 04_advanced_models.ipynb
├── src/                    # Source code
│   ├── data/               # Data collection and processing
│   ├── features/           # Feature engineering
│   ├── models/             # Portfolio construction models
│   └── visualization/      # Visualization modules
├── tests/                  # Unit tests
├── results/                # Generated analysis outputs
├── dashboard/              # Interactive Streamlit dashboard
├── docs/                   # Documentation and methodology
│   └── images/             # Diagrams and visual aids
├── requirements.txt        # Project dependencies
├── setup.py                # Make package installable
└── README.md               # Project description
```

## 📝 Methodology

### Data Collection & Preparation

The project collects data from multiple financial sources and implements a robust preparation pipeline:

1. **Data Retrieval**: API connections to Yahoo Finance, FRED, and World Bank with appropriate error handling
2. **Time Series Alignment**: Resampling and alignment of different data frequencies
3. **Missing Value Treatment**: Forward-fill for market data, appropriate interpolation for economic indicators
4. **Feature Engineering**: Calculation of returns, volatility, drawdowns, and technical indicators
5. **Regime Classification**: Implementation of market regime identification based on economic indicators

### Portfolio Construction

Multiple portfolio construction methodologies are implemented and compared:

1. **Baseline Models**:
   - Equal-weight allocation
   - Market-cap-weighted allocation
   - Traditional 60/40 stocks/bonds allocation

2. **Advanced Models**:
   - Mean-variance optimization with constraints
   - Risk parity implementation
   - Factor-based portfolio construction
   - Regime-dependent allocation strategies

### Performance Evaluation

Comprehensive performance metrics are calculated across different market regimes:

1. **Return Metrics**: Total return, annualized return, period returns
2. **Risk Metrics**: Volatility, downside deviation, maximum drawdown, VaR, CVaR
3. **Risk-Adjusted Metrics**: Sharpe ratio, Sortino ratio, Calmar ratio, information ratio
4. **Scenario Analysis**: Performance during historical stress periods

## 🔮 Business Impact

This analysis provides tangible benefits for various stakeholders:

- **For Wealth Management Firms**: Potential for 15-20% improvement in risk-adjusted returns through optimized allocations
- **For Individual Investors**: Reduction in maximum drawdown during market corrections by 10-15%
- **For Financial Advisors**: Data-driven allocation strategies that can improve client outcomes and satisfaction
- **Cost Efficiency**: Quantified potential fee savings through optimized passive vs. active allocations

## 📋 Future Work

- Implementation of machine learning models for regime prediction
- Addition of alternative asset classes (real estate, commodities, private equity)
- Portfolio optimization with ESG constraints
- Tax-aware portfolio construction
- Monte Carlo simulations for retirement planning

## 👤 Author

**Your Name** - Data & AI Consultant  
[LinkedIn](https://www.linkedin.com/in/michaelmiller1710/) | [Email](mailto:michaelmiller1710@gmail.com)

## 🤝 Acknowledgements

- Financial data provided by Yahoo Finance, FRED, and World Bank
- Factor data courtesy of the Fama-French Data Library
