# main.py

import tkinter as tk  # GUI library used for creating the interface
from tkinter import ttk  # Themed tkinter widgets for consistent look across platforms
from gui.app_window import StockAnalysisApp  # Importing the main stock analysis application window
from uti.styling import apply_styles  # Function to apply custom styles to the application
from gui.register_page import create_registration_page  # Registration page component
from gui.login_page import create_login_page  # Login page component
from database.database import init_db  # Database initialization function
import sys  # To handle system-level operations such as application exit

def on_close(root):
    """
    Handles application exit when the window is closed.

    Parameters:
    root (tk.Tk): The root window of the tkinter application.

    The function ensures that when the user closes the application window,
    it properly quits and destroys the tkinter root window and exits the 
    entire application using sys.exit().
    """
    print("Closing application...")
    root.quit()  # Safely close the tkinter main loop
    root.destroy()  # Destroy the root window
    sys.exit()  # Ensure all background processes exit

def switch_to_register(root):
    """
    Switches to the registration page.

    Parameters:
    root (tk.Tk): The root window of the tkinter application.

    This function destroys all current widgets in the root window and 
    loads the registration page using the create_registration_page function.
    After switching, it also re-centers the window.
    """
    for widget in root.winfo_children():  # Remove all existing widgets from the window
        widget.destroy()
    create_registration_page(root, lambda: switch_to_login(root))  # Load the registration page
    center_window(root)  # Re-center the window after loading the new page

def switch_to_login(root):
    """
    Switches to the login page.

    Parameters:
    root (tk.Tk): The root window of the tkinter application.

    This function destroys all current widgets in the root window and 
    loads the login page using the create_login_page function.
    After switching, it also re-centers the window. The login page
    provides options to switch to registration or start the stock analysis.
    """
    for widget in root.winfo_children():  # Remove all existing widgets from the window
        widget.destroy()
    create_login_page(
        root, 
        lambda: switch_to_register(root),  # Provide option to switch to registration page
        lambda country: start_analysis(root, country)  # Start stock analysis after login
    )
    center_window(root)  # Re-center the window after loading the login page

def start_analysis(root, country):
    """
    Starts the stock analysis based on the user's selected country.

    Parameters:
    root (tk.Tk): The root window of the tkinter application.
    country (str): The country selected by the user for stock analysis.

    This function clears the current window, sets up the main StockAnalysisApp 
    with a styled window, and configures the window dimensions for the analysis 
    interface. The app title is dynamically updated to reflect the chosen country.
    """
    for widget in root.winfo_children():  # Remove all existing widgets from the window
        widget.destroy()

    root.title(f"Stock Analysis - {country}")  # Set the window title to reflect the country
    style = ttk.Style()  # Initialize the ttk Style object for consistent theming
    apply_styles(style)  # Apply the custom styles defined in the utils/styling module

    app = StockAnalysisApp(root, country)  # Initialize the main stock analysis application
    root.geometry("1920x1080")  # Set the window size to full HD resolution
    root.geometry("+0+0")  # Position the window at the top-left corner of the screen

def center_window(root):
    """
    Centers the window on the screen.

    Parameters:
    root (tk.Tk): The root window of the tkinter application.

    This function adjusts the window position so that it appears centered 
    on the user's screen, based on the current window size and the screen's dimensions.
    """
    root.update_idletasks()  # Update the window's current size and position
    width = root.winfo_width()  # Get the current width of the window
    height = root.winfo_height()  # Get the current height of the window
    x = (root.winfo_screenwidth() // 2) - (width // 2)  # Calculate the X position for centering
    y = (root.winfo_screenheight() // 2) - (height // 2)  # Calculate the Y position for centering
    root.geometry('{}x{}+{}+{}'.format(width, height, x, y))  # Apply the centered position to the window

def main():
    """
    Main function that initializes the database, creates the root window, 
    and starts the application with the login page.

    This function initializes the application's database, creates the root tkinter
    window, sets its initial size, and displays the login page. It also ensures 
    the application quits properly when the window is closed.
    """
    init_db()  # Initialize the database connection and structure

    root = tk.Tk()  # Create the root window for the tkinter application
    root.geometry("400x300")  # Set the initial window size for the login/registration pages
    switch_to_login(root)  # Start the application with the login page

    # Set the window close handler to properly quit the application
    root.protocol("WM_DELETE_WINDOW", lambda: on_close(root))

    root.mainloop()  # Start the tkinter main loop, handling events

if __name__ == "__main__":
    main()  # Entry point of the program, calls the main function
