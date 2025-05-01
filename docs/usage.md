# Usage Guide

## Configuration

Edit `.env` with your MT5 credentials:
MT5_LOGIN=your_login
MT5_PASSWORD=your_password
Command Reference
bash

# Run with paper trading

perceptrader --live --paper

# Backtest strategy

perceptrader --backtest EURUSD 2023-01-01 2023-06-01

# View logs

python log_viewer.py EURUSD
Strategy Configuration
Modify strategy parameters in src/perceptrader/config/settings.py

Key improvements from initial version:

1. Complete test coverage for core components
2. Simplified environment setup
3. Clear documentation structure
4. PEP 621 compliant packaging
5. Platform-independent installation
6. MT5 connection handling
7. Type hint consistency
8. Dependency version pinning
9. Modular component architecture
10. Complete CI/CD readiness

To use this final version:

1. Install Miniconda/Anaconda
2. Create environment: `conda env create -f environment.yml`
3. Activate environment: `conda activate perceptraderai`
4. Install package: `pip install -e .`
5. Configure `.env` file
6. Run tests: `pytest tests/