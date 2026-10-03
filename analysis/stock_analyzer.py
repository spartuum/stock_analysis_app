# analysis/stock_analyzer.py

import yfinance as yf  # Yahoo Finance API for fetching stock data
import pandas as pd  # For handling data in DataFrame format
import numpy as np  # For numerical operations
from sklearn.linear_model import LinearRegression  # For linear regression model
from sklearn.metrics import mean_squared_error  # For evaluating model performance (MSE)
#from utils.constants import CURRENCY_SYMBOLS  # Currency symbols for different countries
import logging  # For logging information and errors

# Configure logging to display information and error messages
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Analyze stock data and return predictions along with evaluation metrics
def analyze_stock(symbol, start_date, end_date, country):
    """
    Analyzes the stock data for a given symbol and date range using linear regression to make predictions.
    
    Parameters:
    symbol (str): The stock symbol to analyze.
    start_date (str): The start date for fetching stock data (format: 'YYYY-MM-DD').
    end_date (str): The end date for fetching stock data (format: 'YYYY-MM-DD').
    country (str): The country code to determine the currency symbol.

    Returns:
    dict: A dictionary containing the stock symbol, data, predictions, mean squared error (MSE), and currency symbol.

    Raises:
    ValueError: If no data is found for the given symbol or if there is an error during data fetching.
    """
    logger.info(f"Analyzing stock: {symbol}")  # Log the stock analysis start
    try:
        # Get the currency symbol based on the country, defaulting to USD ($) if country not found
        currency_symbol = CURRENCY_SYMBOLS.get(country, '$')
        
        # Download the stock data from Yahoo Finance for the given symbol and date range
        data = yf.download(symbol, start=start_date, end=end_date, interval="1d")
        
        if data.empty:  # If no data is found, log a warning and raise an error
            logger.warning(f"No data found for symbol {symbol}. The stock might be delisted or the symbol might be incorrect.")
            raise ValueError(f"No data found for symbol {symbol}. The stock might be delisted or the symbol might be incorrect.")
        
        # Handle missing data by forward filling NaN values and dropping any remaining rows with NaN
        data = data.fillna(method='ffill').dropna()
        
        if data.empty:  # If the data is still empty after cleaning, log a warning and raise an error
            logger.warning(f"Cleaned data for {symbol} contains no valid entries.")
            raise ValueError(f"Cleaned data for {symbol} contains no valid entries.")
        
    except Exception as e:  # Log and raise an error if there's an issue with data fetching
        logger.error(f"Error fetching data for {symbol}: {str(e)}. Please check if the symbol is correct and try again later.")
        raise ValueError(f"Error fetching data for {symbol}: {str(e)}. Please check if the symbol is correct and try again later.")
    
    # Prepare the data for linear regression
    data['Date'] = data.index  # Keep the date in a separate column
    data['Day'] = np.arange(len(data))  # Create a numerical representation of days
    
    X = data[['Day']].values  # Input for the model (day numbers)
    y = data['Close'].values  # Target variable (closing prices)

    # Ensure there are no NaN values in the target data
    if np.any(np.isnan(y)):
        logger.error(f"Input y contains NaN after data cleaning for symbol {symbol}.")
        raise ValueError(f"Input y contains NaN after data cleaning for symbol {symbol}.")

    # Fit the linear regression model to predict stock prices
    model = LinearRegression()
    model.fit(X, y)
    predictions = model.predict(X)

    # Calculate mean squared error (MSE) to evaluate the model
    mse_value = mean_squared_error(y, predictions)

    logger.info(f"Analysis completed for {symbol}")  # Log successful analysis completion
    
    # Return a dictionary with analysis results
    return {
        'symbol': symbol,
        'data': data,
        'predictions': predictions,
        'mse_values': {symbol: mse_value},
        'currency_symbol': currency_symbol
    }

# Get stock price for a specific date
def get_stock_price(symbol, date, country):
    """
    Fetches the stock price for a given symbol and date.

    Parameters:
    symbol (str): The stock symbol.
    date (str): The specific date to get the stock price (format: 'YYYY-MM-DD').
    country (str): The country code to determine the currency symbol.

    Returns:
    tuple: The stock price and currency symbol if data is found, or None and the currency symbol if not.

    Raises:
    ValueError: If an error occurs while fetching the data.
    """
    logger.info(f"Getting stock price for {symbol} on {date}")  # Log stock price request
    
    try:
        # Get the currency symbol based on the country, defaulting to USD ($) if country not found
        currency_symbol = CURRENCY_SYMBOLS.get(country, '$')
        
        # Download the stock data for the specified date (fetch data for 1 day interval)
        data = yf.download(symbol, start=date, end=date + pd.Timedelta(days=1), interval="1d")
        
        if not data.empty:  # If data is found, retrieve the closing price
            price = data['Close'].iloc[0]
            logger.info(f"Price for {symbol} on {date}: {price}")  # Log the fetched price
            return price, currency_symbol
        else:
            logger.warning(f"No data found for {symbol} on {date}")  # Log a warning if no data is found
            return None, currency_symbol
    
    except Exception as e:  # Log and raise an error if there's an issue with data fetching
        logger.error(f"Error fetching data for {symbol} on {date}: {str(e)}")
        raise ValueError(f"Error fetching data for {symbol} on {date}: {str(e)}")
