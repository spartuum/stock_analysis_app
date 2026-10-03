# gui/app_window.py

import tkinter as tk  # GUI library used for creating the main window and widgets
from tkinter import ttk, messagebox  # ttk for themed widgets, messagebox for showing error messages
import traceback  # For detailed error stack tracing in case of exceptions
import logging  # Logging for debugging and tracking application behavior
import re  # Regular expressions for possible input validation (though not used here)
from gui.components import create_input_frame, create_plot_frame, create_recommendation_frame  # Importing GUI component creators
from analysis.stock_analyzer import analyze_stock, get_stock_price  # Stock analysis logic
from uti.constants import TOP_50_STOCKS  # Top 50 stocks data for different countries

# Configuring the logging format and level for the application
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class StockAnalysisApp:
    """
    StockAnalysisApp handles the main application window for stock analysis. 
    It integrates different GUI components like input fields, plots, and recommendations.
    
    Attributes:
    root (tk.Tk): The root window of the tkinter application.
    country (str): The selected country for the stock analysis.
    stock_symbols (list): List of stock symbols and names based on the selected country.
    """

    def __init__(self, root, country):
        """
        Initializes the StockAnalysisApp by setting up the root window and its components.

        Parameters:
        root (tk.Tk): The root tkinter window.
        country (str): The country selected by the user for stock analysis.
        
        The constructor initializes the window's minimum size, retrieves the top 50 stocks for the
        selected country, and calls the function to create necessary widgets (input, plot, and recommendation).
        """
        self.root = root
        self.country = country
        self.stock_symbols = TOP_50_STOCKS[country]  # Load the stock symbols and names for the selected country
        self.root.minsize(800, 600)  # Set the minimum size of the application window
        self.create_widgets()  # Create and layout the widgets for the stock analysis interface

    def create_widgets(self):
        """
        Creates and organizes the main application widgets (input frame, plot frame, and recommendation frame)
        within the window grid.
        
        The window layout is divided into three sections:
        1. Input frame (row 0) for user input
        2. Plot frame (row 1) for displaying stock price graphs
        3. Recommendation frame (row 2) for displaying analysis recommendations
        """
        self.root.grid_rowconfigure(0, weight=1)  # Row for input frame
        self.root.grid_rowconfigure(1, weight=4)  # Row for plot frame
        self.root.grid_rowconfigure(2, weight=2)  # Row for recommendation frame
        self.root.grid_columnconfigure(0, weight=1)  # Single column for all rows

        # Create the input frame with stock symbols passed as options
        self.input_frame = create_input_frame(self.root, self.stock_symbols)
        self.input_frame.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)  # Grid layout configuration

        # Create the plot frame for showing stock charts
        self.plot_frame = create_plot_frame(self.root)
        self.plot_frame.grid(row=1, column=0, sticky='nsew', padx=10, pady=10)  # Grid layout configuration

        # Create the recommendation frame for displaying the analysis result
        self.recommendation_frame = create_recommendation_frame(self.root)
        self.recommendation_frame.grid(row=2, column=0, sticky='nsew', padx=10, pady=10)  # Grid layout configuration

        # Assign button commands for input actions
        self.input_frame.analyze_range_button.config(command=self.analyze_date_range, style='Large.TButton')  # Analyze a date range
        self.input_frame.check_specific_date_button.config(command=self.check_specific_date, style='Large.TButton')  # Check stock price for a specific date

    def analyze_date_range(self):
        """
        Handles the action when the user clicks on the "Analyze Date Range" button.
        
        This function clears any previous plot and recommendation, retrieves the stock symbol and
        date range from the input frame, and calls the analyze_stock function to perform analysis. 
        It then updates the plot and recommendation based on the analysis results.
        """
        logging.debug("Analyze date range button clicked")  # Log button click for debugging
        self.plot_frame.clear_plot()  # Clear the plot frame before starting new analysis
        self.recommendation_frame.clear_recommendation()  # Clear previous recommendations

        symbol = self.input_frame.stock_combobox.get().strip()  # Get the selected stock symbol
        start_date = self.input_frame.start_date_entry.get_date()  # Get the selected start date
        end_date = self.input_frame.end_date_entry.get_date()  # Get the selected end date

        logging.debug(f"Analyzing {symbol} from {start_date} to {end_date}")  # Log the analysis input

        # Validate input: ensure stock symbol is selected and dates are correct
        if not symbol:
            messagebox.showerror("Error", "Please select a stock symbol from the dropdown.")
            return

        if start_date >= end_date:
            messagebox.showerror("Error", "Start date must be before end date.")
            return

        try:
            logging.debug("Calling analyze_stock function")  # Log function call
            stock_symbol = symbol.split(' - ')[0]  # Extract the stock symbol from the dropdown value
            result = analyze_stock(stock_symbol, start_date, end_date, self.country)  # Perform stock analysis
            
            logging.debug("Plotting stock data")  # Log plotting
            self.plot_frame.plot_stock(result['symbol'], result['data'], result['predictions'])  # Plot the stock data and predictions
            
            logging.debug("Providing recommendation")  # Log recommendation action
            self.provide_recommendation(result)  # Provide the analysis recommendation based on results
            
        except Exception as e:
            # If an error occurs during analysis, log the error and show a detailed error message
            error_msg = f"An error occurred while analyzing {symbol}:\n\n{str(e)}\n\nStack Trace:\n{traceback.format_exc()}"
            logging.error(error_msg)
            messagebox.showerror("Error", error_msg)
            print(error_msg)

    def check_specific_date(self):
        """
        Handles the action when the user clicks on the "Check Specific Date" button.
        
        This function retrieves the stock symbol and specific date from the input frame, 
        and fetches the stock price for that date. It displays the price or a message if no data is found.
        """
        symbol = self.input_frame.stock_combobox.get().strip()  # Get the selected stock symbol
        specific_date = self.input_frame.specific_date_entry.get_date()  # Get the specific date selected

        if not symbol:
            messagebox.showerror("Error", "Please select a stock symbol from the dropdown.")
            return

        try:
            stock_symbol = symbol.split(' - ')[0]  # Extract the stock symbol from the dropdown value
            price, currency_symbol = get_stock_price(stock_symbol, specific_date, self.country)  # Fetch stock price for the specific date
            if price is not None:
                # Update recommendation frame with the fetched price
                self.recommendation_frame.update_recommendation(f"The price of {symbol} on {specific_date} was {currency_symbol}{price:.2f}")
            else:
                self.recommendation_frame.update_recommendation(f"No data available for {symbol} on {specific_date}")
        except Exception as e:
            # Log and display any error encountered during the stock price fetch
            error_msg = f"An error occurred while checking {symbol} on {specific_date}:\n\n{str(e)}"
            logging.error(error_msg)
            messagebox.showerror("Error", error_msg)
            print(error_msg)

    def provide_recommendation(self, result):
        """
        Provides a recommendation based on the stock analysis results.

        Parameters:
        result (dict): The result dictionary from the analyze_stock function, containing stock data, 
                       predictions, and error metrics.

        The recommendation is based on the predicted price change, comparing the last closing price 
        with the predicted price. It also takes into account the Mean Squared Error (MSE) of the model.
        """
        symbol = result['symbol']  # Stock symbol
        currency_symbol = result['currency_symbol']  # Currency symbol (e.g., $, €, etc.)
        mse = result['mse_values'][symbol]  # Mean Squared Error of the prediction model
        last_price = result['data']['Close'].iloc[-1]  # Last closing price of the stock
        predicted_price = result['predictions'][-1]  # Predicted next price from the model
        price_change = ((predicted_price - last_price) / last_price) * 100  # Percentage change in price

        # Build the recommendation message
        recommendation = f"Analysis for {symbol}:\n"
        recommendation += f"Last Closing Price: {currency_symbol}{last_price:.2f}\n"
        recommendation += f"Predicted Next Price: {currency_symbol}{predicted_price:.2f}\n"
        recommendation += f"Predicted Change: {price_change:.2f}%\n"
        recommendation += f"Mean Squared Error: {mse:.4f}\n"

        # Provide a recommendation based on the predicted price change
        if price_change > 0:
            recommendation += f"Recommendation: Consider buying {symbol}. The model predicts a potential increase."
        elif price_change < 0:
            recommendation += f"Recommendation: Consider selling {symbol}. The model predicts a potential decrease."
        else:
            recommendation += f"Recommendation: Hold {symbol}. The model predicts stable prices."

        # Update the recommendation frame with the generated recommendation
        self.recommendation_frame.update_recommendation(recommendation)
