# utils/plotting.py

import matplotlib.dates as mdates  # For converting and handling date data in plots
import numpy as np  # For numerical operations, such as calculating distances
import pandas as pd  # For handling data in tabular format, especially dates

def add_hover_tooltip(ax, all_data, fig):
    """
    Adds a hover tooltip to the matplotlib plot, which displays the stock symbol, date, 
    and stock price when the user hovers over a data point.

    Parameters:
    ax (matplotlib.axes.Axes): The matplotlib axes where the plot is drawn.
    all_data (dict): A dictionary containing stock data for multiple symbols.
                     Keys are stock symbols, and values are pandas DataFrames with 'Date' and other columns.
    fig (matplotlib.figure.Figure): The matplotlib figure object associated with the plot.

    This function adds interactivity to the plot by showing a tooltip when the mouse is 
    close to any data point. It calculates the nearest data point based on mouse coordinates.
    """
    # Initialize the annotation box for displaying tooltips on hover
    annot = ax.annotate("", xy=(0, 0), xytext=(10, 10),
                        textcoords="offset points",
                        bbox=dict(boxstyle="round", fc="w"),  # Rounded box with white background
                        arrowprops=dict(arrowstyle="->"))  # Arrow pointing to the data point
    annot.set_visible(True)  # Start with annotation visible

    # Dictionaries to store x and y data for each stock symbol
    all_xdata = {}
    all_ydata = {}
    
    # Iterate through all the stock data and convert dates to matplotlib's internal date format (numerical)
    for symbol, data in all_data.items():
        xdata = [mdates.date2num(d) for d in data['Date']]  # Convert 'Date' column to numerical format
        ydata = ax.get_lines()[0].get_ydata()  # Get the y-data (closing prices) from the plot
        all_xdata[symbol] = xdata  # Store x-data for each symbol
        all_ydata[symbol] = ydata  # Store y-data for each symbol

    # Function to handle the hover event
    def hover(event):
        """
        Event handler for detecting mouse movements over the plot and displaying tooltips
        when hovering near a data point.
        
        Parameters:
        event (matplotlib.backend_bases.Event): The event object containing mouse coordinates and other information.
        """
        if event.inaxes == ax:  # Ensure the mouse is inside the plot axes
            event_xdata = mdates.date2num(pd.to_datetime(event.xdata, unit='D', origin='unix'))  # Convert mouse x-position to a date
            closest_dist = float('inf')  # Initialize closest distance to infinity
            closest_idx = None  # Initialize the index of the closest point
            closest_symbol = None  # Initialize the symbol of the closest stock
            
            # Iterate through all stock symbols and find the closest data point to the mouse
            for symbol, xdata in all_xdata.items():
                ydata = all_ydata[symbol]
                dist = np.sqrt((np.array(xdata) - event_xdata)**2 + (np.array(ydata) - event.ydata)**2)  # Calculate distance between mouse and data points
                idx = np.argmin(dist)  # Get the index of the closest data point
                if dist[idx] < closest_dist:  # Update the closest point if this one is nearer
                    closest_dist = dist[idx]
                    closest_idx = idx
                    closest_symbol = symbol

            # If the closest point is within a threshold distance, show the tooltip
            if closest_dist < 0.02:  # Define threshold for showing tooltips
                closest_data = all_data[closest_symbol]
                # Set the position of the annotation and update its text with the symbol, date, and price
                annot.xy = (mdates.num2date(all_xdata[closest_symbol][closest_idx]), all_ydata[closest_symbol][closest_idx])
                annot.set_text(f'{closest_symbol}\n{closest_data.index[closest_idx].date()}\n${all_ydata[closest_symbol][closest_idx]:.2f}')
                annot.set_visible(True)  # Make the annotation visible
            else:
                annot.set_visible(False)  # Hide the annotation if no point is close enough
            fig.canvas.draw_idle()  # Redraw the plot with the updated annotation

    # Connect the hover event handler to the matplotlib figure's canvas
    fig.canvas.mpl_connect('motion_notify_event', hover)
