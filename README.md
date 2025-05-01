markdown

# PerceptraderAI

Automated trading framework integrating ML/RL with MetaTrader5

## Features

- Live/paper trading via MT5
- RSI-MACD & Deep RL strategies
- Risk management system
- Backtesting framework

## Installation

conda env create -f environment.yml
conda activate perceptraderai
pip install -e .[PerceptraderAI.zip](PerceptraderAI.zip)
Usage
bash

# Live trading

perceptrader --live --paper

# Backtesting

perceptrader --backtest EURUSD 2023-01-01 2023-06-01