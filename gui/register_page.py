# gui/register_page.py

import tkinter as tk  # Tkinter for creating GUI components
from tkinter import ttk, messagebox  # ttk for themed widgets, messagebox for displaying alerts
from database.database import register_user  # Function to register the user (ensure the correct import path)

def create_registration_page(root, switch_to_login):
    """
    Creates the registration page where users can enter their details to register.

    Parameters:
    root (tk.Tk): The root window of the tkinter application.
    switch_to_login (function): A function to switch back to the login page after successful registration.

    This function sets up the layout for the registration page with input fields for username, password,
    and country selection, and buttons to register or switch back to the login page.
    """
    root.title("Register")  # Set the window title to "Register"

    # Create the main frame that holds the registration form
    main_frame = ttk.Frame(root, padding="20")  # Main frame with padding around it
    main_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)  # Center the frame relative to the window

    # Create a frame for the actual registration form inside the main frame
    register_frame = ttk.Frame(main_frame, padding="10")
    register_frame.grid(row=0, column=0)  # Place the registration frame in the main frame grid

    # Username label and entry field
    ttk.Label(register_frame, text="Username:").grid(row=0, column=0, sticky="e", padx=5, pady=5)  # Label for username
    username_entry = ttk.Entry(register_frame)  # Entry widget for entering username
    username_entry.grid(row=0, column=1, padx=5, pady=5)  # Position entry field next to the label

    # Password label and entry field (with masking using show="*")
    ttk.Label(register_frame, text="Password:").grid(row=1, column=0, sticky="e", padx=5, pady=5)  # Label for password
    password_entry = ttk.Entry(register_frame, show="*")  # Entry widget for entering password (masked)
    password_entry.grid(row=1, column=1, padx=5, pady=5)  # Position password entry next to the label

    # Country selection combobox
    ttk.Label(register_frame, text="Select Country:").grid(row=2, column=0, sticky="e", padx=5, pady=5)  # Label for country selection
    country_combobox = ttk.Combobox(register_frame, values=['USA', 'India', 'UK', 'Germany', 'Japan'])  # Combobox with predefined country options
    country_combobox.grid(row=2, column=1, padx=5, pady=5)  # Position combobox next to the label

    def register():
        """
        Handles the registration button click event. It retrieves the username, password, and country,
        validates the input, and registers the user if all fields are filled. Displays appropriate messages
        based on the outcome.
        """
        username = username_entry.get()  # Get the entered username
        password = password_entry.get()  # Get the entered password
        country = country_combobox.get()  # Get the selected country

        # Validate that all fields are filled
        if not (username and password and country):
            messagebox.showerror("Error", "All fields are required.")  # Show error if any field is empty
        else:
            # Try to register the user and handle success or failure
            if register_user(username, password, country):
                messagebox.showinfo("Success", "Registration successful.")  # Show success message
                switch_to_login()  # Switch to login page after successful registration
            else:
                messagebox.showerror("Error", "Username already exists.")  # Show error if username is already taken

    # Register button to trigger the registration process
    ttk.Button(register_frame, text="Register", command=register).grid(row=3, column=0, columnspan=2, pady=10)  # Registration button

    # Button to switch to the login page
    ttk.Button(register_frame, text="Go to Login", command=switch_to_login).grid(row=4, column=0, columnspan=2)  # Login page button

    # Center the frame on the window
    root.update_idletasks()  # Update widget sizes and positions
    width = main_frame.winfo_width()  # Get the width of the main frame
    height = main_frame.winfo_height()  # Get the height of the main frame
    x = (root.winfo_width() // 2) - (width // 2)  # Calculate X position to center the frame horizontally
    y = (root.winfo_height() // 2) - (height // 2)  # Calculate Y position to center the frame vertically
    main_frame.place(x=x, y=y)  # Center the main frame within the window
