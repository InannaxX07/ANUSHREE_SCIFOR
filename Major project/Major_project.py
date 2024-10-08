import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

# Streamlit app
st.title('Stock Price Prediction App')

# User input
ticker = st.text_input('Enter Stock Ticker (e.g., AAPL, GOOGL)', 'AAPL')
n_years = st.slider('Years of prediction:', 1, 5, 1)

# Load data
@st.cache_data
def load_data(ticker):
    data = yf.download(ticker, start='2010-01-01', end='2023-12-31')
    data.reset_index(inplace=True)
    return data

data = load_data(ticker)

# Prepare data
data['Date'] = pd.to_datetime(data['Date'])
data['Days'] = (data['Date'] - data['Date'].min()).dt.days

X = data[['Days']]
y = data['Close']

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = LinearRegression()
model.fit(X_train, y_train)

# Make predictions
last_date = data['Date'].max()
prediction_days = np.arange(1, n_years * 365 + 1)
future_dates = pd.date_range(start=last_date, periods=len(prediction_days) + 1)[1:]
future_X = pd.DataFrame({'Days': data['Days'].max() + prediction_days})
future_prices = model.predict(future_X)

# Plot results
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(data['Date'], data['Close'], label='Historical Data')
ax.plot(future_dates, future_prices, label='Predicted Prices', color='red')
ax.set_xlabel('Date')
ax.set_ylabel('Stock Price')
ax.set_title(f'{ticker} Stock Price Prediction')
ax.legend()

st.pyplot(fig)

# Display metrics
train_score = model.score(X_train, y_train)
test_score = model.score(X_test, y_test)

st.write(f'Model Performance:')
st.write(f'Training R-squared: {train_score:.2f}')
st.write(f'Testing R-squared: {test_score:.2f}')

# Predicted prices
st.write('Predicted Stock Prices:')
future_df = pd.DataFrame({'Date': future_dates, 'Predicted Price': future_prices})
st.dataframe(future_df.set_index('Date'))

# Disclaimer
st.write('Disclaimer: This is a simple model for demonstration purposes only. Do not use it for actual trading decisions.')
