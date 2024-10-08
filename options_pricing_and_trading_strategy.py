# -*- coding: utf-8 -*-
"""Options Pricing and Trading Strategy.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1os-tZrVMg4FGqdhMXMN8vU2-pKi5CPvN
"""

import numpy as np
import scipy.stats as si
import matplotlib.pyplot as plt
import yfinance as yf
from datetime import datetime, timedelta

def black_scholes(S, K, T, r, sigma, option_type="call"):
    """
    S: Spot price of the underlying asset
    K: Strike price of the option
    T: Time to maturity (in years)
    r: Risk-free interest rate (annual)
    sigma: Volatility of the underlying asset
    option_type: "call" for call option, "put" for put option
    """
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    if option_type == "call":
        option_price = S * si.norm.cdf(d1, 0.0, 1.0) - K * np.exp(-r * T) * si.norm.cdf(d2, 0.0, 1.0)
    elif option_type == "put":
        option_price = K * np.exp(-r * T) * si.norm.cdf(-d2, 0.0, 1.0) - S * si.norm.cdf(-d1, 0.0, 1.0)

    return option_price

# Example usage
S = 100  # Current stock price
K = 100  # Strike price
T = 1    # Time to maturity (1 year)
r = 0.05 # Risk-free rate (5%)
sigma = 0.2  # Volatility (20%)

call_price = black_scholes(S, K, T, r, sigma, option_type="call")
put_price = black_scholes(S, K, T, r, sigma, option_type="put")

print(f"Call Option Price: {call_price:.2f}")
print(f"Put Option Price: {put_price:.2f}")

# Download stock data (Example: AAPL)
ticker = 'AAPL'
start_date = datetime.today() - timedelta(days=365)
end_date = datetime.today()

data = yf.download(ticker, start=start_date, end=end_date)
data['Returns'] = data['Adj Close'].pct_change()
data = data.dropna()

# Visualize the stock price
plt.figure(figsize=(10, 6))
data['Adj Close'].plot()
plt.title(f'{ticker} Adjusted Close Price')
plt.show()

def delta(S, K, T, r, sigma, option_type="call"):
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    if option_type == "call":
        return si.norm.cdf(d1, 0.0, 1.0)
    elif option_type == "put":
        return si.norm.cdf(d1, 0.0, 1.0) - 1

# Trading strategy
initial_cash = 100000  # Initial cash in the portfolio
positions = 0          # No initial positions

for i in range(len(data)):
    S = data['Adj Close'].iloc[i]
    T = (end_date - data.index[i]).days / 365
    delta_value = delta(S, K, T, r, sigma, option_type="call")

    # Maintain a delta-neutral position
    positions -= delta_value

    # Calculate the portfolio value
    portfolio_value = initial_cash + positions * S
    data.at[data.index[i], 'Portfolio Value'] = portfolio_value
    data.at[data.index[i], 'Delta'] = delta_value

# Visualize the portfolio value over time
plt.figure(figsize=(10, 6))
data['Portfolio Value'].plot()
plt.title(f'{ticker} Delta-Neutral Portfolio Value')
plt.show()