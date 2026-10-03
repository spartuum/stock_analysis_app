# gui/components.py

import tkinter as tk  # Tkinter for creating GUI components
from tkinter import ttk  # Themed widgets from Tkinter for consistent look-and-feel across platforms
from tkcalendar import DateEntry  # DateEntry widget for selecting dates
import matplotlib.pyplot as plt  # Plotting library for stock data visualization
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # Matplotlib canvas to embed plots in Tkinter
import matplotlib.dates as mdates  # Helper module for formatting date-based plots
import logging  # For logging and debugging purposes

def create_input_frame(parent, stock_symbols):
    """
    Creates the input frame where the user can select a stock symbol, a date range,
    and check stock data for a specific date.

    Parameters:
    parent (tk.Widget): The parent widget where the frame will be placed.
    stock_symbols (list): List of stock symbols and company names.

    Returns:
    ttk.Frame: A frame containing all the input widgets (combobox, date entries, buttons).
    """
    frame = ttk.Frame(parent, padding="5", style="TFrame")  # Create the frame with padding

    # Configure the frame's grid layout: 3 rows and 4 columns with equal weight
    for i in range(3):  # 3 rows for different input options
        frame.grid_rowconfigure(i, weight=1)
    for i in range(4):  # 4 columns to arrange labels, input fields, and buttons
        frame.grid_columnconfigure(i, weight=1)

    # Format the stock symbols for display in the dropdown list (combobox)
    stock_options = [f"{stock['symbol']} - {stock['name']}" for stock in stock_symbols]

    # Row 1: Stock Symbol Selection
    ttk.Label(frame, text="Select Stock Symbol:", font=('Arial', 12)).grid(row=0, column=0)
    frame.stock_combobox = ttk.Combobox(frame, values=stock_options, width=40, font=('Arial', 12))
    frame.stock_combobox.grid(row=0, column=1)  # Combobox for selecting a stock symbol

    # Row 2: Date Range Selection
    ttk.Label(frame, text="Select Date Range:", font=('Arial', 12)).grid(row=1, column=0)

    # DateEntry widgets for selecting the start and end dates
    frame.start_date_entry = DateEntry(frame, width=12, background='darkblue', foreground='white', borderwidth=2,
                                       font=('Arial', 12), calendar_font=('Arial', 12))
    frame.start_date_entry.grid(row=1, column=1)

    frame.end_date_entry = DateEntry(frame, width=12, background='darkblue', foreground='white', borderwidth=2,
                                     font=('Arial', 12), calendar_font=('Arial', 12))
    frame.end_date_entry.grid(row=1, column=2)

    # Button to analyze stock data for the selected date range
    frame.analyze_range_button = ttk.Button(frame, text="Analyze Date Range", style='Large.TButton')
    frame.analyze_range_button.grid(row=1, column=3)

    # Row 3: Specific Date Check
    ttk.Label(frame, text="Check Stock on Specific Date:", font=('Arial', 12)).grid(row=2, column=0)

    # DateEntry widget for selecting a specific date to check stock price
    frame.specific_date_entry = DateEntry(frame, width=12, background='darkblue', foreground='white', borderwidth=2,
                                          font=('Arial', 12), calendar_font=('Arial', 12))
    frame.specific_date_entry.grid(row=2, column=1)

    # Button to check the stock price for the selected specific date
    frame.check_specific_date_button = ttk.Button(frame, text="Check Specific Date", style='Large.TButton')
    frame.check_specific_date_button.grid(row=2, column=3)

    return frame  # Return the fully populated input frame

class PlotFrame(ttk.Frame):
    """
    PlotFrame is a custom frame that embeds a matplotlib plot to display stock price data
    and predicted trends.

    Attributes:
    fig (Figure): The matplotlib figure object for creating the plot.
    ax (Axes): The axes object for plotting stock data.
    canvas (FigureCanvasTkAgg): The canvas that embeds the matplotlib figure within the Tkinter frame.
    """
    def __init__(self, parent, **kwargs):
        """
        Initializes the PlotFrame by setting up the canvas for displaying the stock plot.

        Parameters:
        parent (tk.Widget): The parent widget where this frame will be placed.
        kwargs: Additional arguments passed to the ttk.Frame initializer.
        """
        super().__init__(parent, style="PlotFrame.TFrame", **kwargs)  # Initialize as a ttk.Frame
        self.fig, self.ax = plt.subplots(figsize=(12, 8), dpi=100)  # Create a figure and axes for plotting
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)  # Embed the figure into a Tkinter canvas
        self.canvas.draw()  # Draw the empty plot initially
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)  # Pack the canvas into the frame

    def plot_stock(self, symbol, data, predictions):
        """
        Plots the actual and predicted stock prices on the matplotlib canvas.

        Parameters:
        symbol (str): The stock symbol being analyzed.
        data (DataFrame): The stock price data with date and closing price.
        predictions (list): The predicted stock prices for the same date range.
        """
        logging.debug(f"Plotting stock data for {symbol}")
        self.ax.clear()  # Clear any existing plot
        self.ax.plot(data['Date'], data['Close'], label=f'{symbol} Actual Prices', color='#1f77b4', marker='o', markersize=4)  # Plot actual prices
        self.ax.plot(data['Date'], predictions, label=f'{symbol} Predicted Prices', color='#ff7f0e', linestyle='--')  # Plot predicted prices
        self.ax.set_title(f'Stock Prices and Predictions for {symbol}', fontsize=16, fontweight='bold')  # Set plot title
        self.ax.set_xlabel('Date', fontsize=12)  # X-axis label
        self.ax.set_ylabel('Price', fontsize=12)  # Y-axis label
        self.ax.legend(fontsize=10)  # Display the legend
        self.ax.grid(True, linestyle=':', alpha=0.6)  # Add grid lines to the plot
        self.ax.tick_params(axis='both', which='major', labelsize=10)  # Configure tick size

        # Configure date formatting on the X-axis
        self.ax.xaxis.set_major_locator(mdates.AutoDateLocator())
        self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        plt.setp(self.ax.xaxis.get_majorticklabels(), rotation=45, ha='right')  # Rotate date labels for better readability

        self.fig.tight_layout()  # Ensure the layout is adjusted to avoid overlapping labels
        self.canvas.draw()  # Redraw the canvas with the new plot
        logging.debug("Plot drawn")

    def clear_plot(self):
        """
        Clears the plot by resetting the axes and showing a placeholder title.
        """
        logging.debug("Clearing plot")
        self.ax.clear()  # Clear the axes
        self.ax.set_title("No data to display")  # Set a placeholder title
        self.ax.set_xlabel("Date")  # Set default X-axis label
        self.ax.set_ylabel("Price")  # Set default Y-axis label
        self.canvas.draw()  # Redraw the canvas with the cleared plot

def create_plot_frame(parent):
    """
    Creates and returns an instance of PlotFrame.

    Parameters:
    parent (tk.Widget): The parent widget where the frame will be placed.

    Returns:
    PlotFrame: The custom frame for displaying stock price plots.
    """
    return PlotFrame(parent)

class RecommendationFrame(ttk.Frame):
    """
    RecommendationFrame is a custom frame for displaying stock analysis recommendations.
    It includes a scrollable text widget to hold multi-line recommendations.

    Attributes:
    recommendation_text (tk.Text): The text widget where recommendations are displayed.
    scrollbar (ttk.Scrollbar): The scrollbar for the text widget.
    """
    def __init__(self, parent, **kwargs):
        """
        Initializes the RecommendationFrame with a scrollable text widget to display recommendations.

        Parameters:
        parent (tk.Widget): The parent widget where this frame will be placed.
        kwargs: Additional arguments passed to the ttk.Frame initializer.
        """
        super().__init__(parent, style="RecommendationFrame.TFrame", **kwargs)  # Initialize as a ttk.Frame

        # Create a Text widget to hold the recommendations
        self.recommendation_text = tk.Text(self, wrap=tk.WORD, font=('Arial', 16), height=10)
        
        # Create a vertical scrollbar and associate it with the Text widget
        self.scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.recommendation_text.yview)
        self.recommendation_text.config(yscrollcommand=self.scrollbar.set)

        # Pack the Text widget and the Scrollbar into the frame
        self.recommendation_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def update_recommendation(self, recommendation):
        """
        Updates the recommendation displayed in the text widget.

        Parameters:
        recommendation (str): The recommendation text to be displayed.
        """
        self.recommendation_text.delete('1.0', tk.END)  # Clear existing text
        self.recommendation_text.insert(tk.END, recommendation)  # Insert the new recommendation
        
        # Scroll to the bottom to ensure the latest recommendation is visible
        self.recommendation_text.see(tk.END)
        self.recommendation_text.update_idletasks()  # Update the widget to reflect changes

    def clear_recommendation(self):
        """
        Clears the recommendation text displayed in the text widget.
        """
        self.recommendation_text.delete('1.0', tk.END)  # Clear all text in the widget

def create_recommendation_frame(parent):
    """
    Creates and returns an instance of RecommendationFrame.

    Parameters:
    parent (tk.Widget): The parent widget where the frame will be placed.

    Returns:
    RecommendationFrame: The custom frame for displaying stock recommendations.
    """
    return RecommendationFrame(parent)
