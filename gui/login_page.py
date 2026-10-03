# gui/login_page.py

import tkinter as tk  # Tkinter for creating GUI components
from tkinter import ttk, messagebox  # ttk for styled widgets, messagebox for displaying alerts
from database.database import authenticate_user  # Function to authenticate the user

def create_login_page(root, switch_to_register, on_login_success):
    """
    Creates the login page where the user can enter their credentials to log in.

    Parameters:
    root (tk.Tk): The root window of the tkinter application.
    switch_to_register (function): A function to switch to the registration page.
    on_login_success (function): A callback function to be executed after successful login, passing the user's country.

    This function sets up the layout for the login page with input fields for username and password,
    and buttons to log in or switch to the registration page.
    """
    root.title("Login")  # Set the window title to "Login"
    
    # Create the main frame that holds the login form
    main_frame = ttk.Frame(root, padding="20")  # Main frame with padding around it
    main_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)  # Center the frame relative to the window

    # Create a frame for the actual login form inside the main frame
    login_frame = ttk.Frame(main_frame, padding="10")
    login_frame.grid(row=0, column=0)  # Place the login frame in the main frame grid

    # Username label and entry field
    ttk.Label(login_frame, text="Username:").grid(row=0, column=0, sticky="e", padx=5, pady=5)  # Label for username
    username_entry = ttk.Entry(login_frame)  # Entry widget for entering username
    username_entry.grid(row=0, column=1, padx=5, pady=5)  # Position entry field next to the label

    # Password label and entry field (with masking using show="*")
    ttk.Label(login_frame, text="Password:").grid(row=1, column=0, sticky="e", padx=5, pady=5)  # Label for password
    password_entry = ttk.Entry(login_frame, show="*")  # Entry widget for entering password (masked)
    password_entry.grid(row=1, column=1, padx=5, pady=5)  # Position password entry next to the label

    def login():
        """
        Handles the login button click event. It retrieves the username and password, 
        authenticates the user, and displays an appropriate message.
        """
        username = username_entry.get()  # Get the entered username
        password = password_entry.get()  # Get the entered password
        country = authenticate_user(username, password)  # Authenticate the user and retrieve the country
        
        if country:
            # If authentication is successful, show a welcome message and proceed to the next step
            messagebox.showinfo("Login", f"Welcome {username} from {country}")
            on_login_success(country)  # Pass the user's country to the next step (e.g., stock analysis page)
        else:
            # If authentication fails, show an error message
            messagebox.showerror("Error", "Invalid username or password.")

    # Login button to trigger the login process
    ttk.Button(login_frame, text="Login", command=login).grid(row=2, column=0, columnspan=2, pady=10)  # Login button

    # Button to switch to the registration page
    ttk.Button(login_frame, text="Go to Register", command=switch_to_register).grid(row=3, column=0, columnspan=2)  # Registration page button

    # Center the frame on the window
    root.update_idletasks()  # Update widget sizes and positions
    width = main_frame.winfo_width()  # Get the width of the main frame
    height = main_frame.winfo_height()  # Get the height of the main frame
    x = (root.winfo_width() // 2) - (width // 2)  # Calculate X position to center the frame horizontally
    y = (root.winfo_height() // 2) - (height // 2)  # Calculate Y position to center the frame vertically
    main_frame.place(x=x, y=y)  # Center the main frame within the window
