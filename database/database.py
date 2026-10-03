# database/database.py

import sqlite3  # SQLite module for interacting with the SQLite database

# Initialize the database and create the users table if it doesn't exist
def init_db():
    """
    Initializes the SQLite database by creating a 'users' table if it doesn't exist.

    The 'users' table will store:
    - username (TEXT): The username, which is the primary key.
    - password (TEXT): The password for the user account (stored as plain text in this example).
    - country (TEXT): The country associated with the user.

    This function connects to 'users.db', creates the table, and closes the connection.
    """
    conn = sqlite3.connect('users.db')  # Connect to the database (or create it if it doesn't exist)
    cursor = conn.cursor()

    # Create the 'users' table if it doesn't already exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        username TEXT PRIMARY KEY,
                        password TEXT NOT NULL,
                        country TEXT NOT NULL)''')
    
    conn.commit()  # Commit the transaction (save changes to the database)
    conn.close()  # Close the connection to the database

# Register a new user in the database
def register_user(username, password, country):
    """
    Registers a new user by inserting the username, password, and country into the 'users' table.

    Parameters:
    username (str): The username for the new account.
    password (str): The password for the new account (stored as plain text in this example).
    country (str): The country associated with the user.

    Returns:
    bool: True if the user was registered successfully, False if the username already exists.
    
    If the username already exists, an IntegrityError will be raised due to the PRIMARY KEY constraint.
    This function handles that error and returns False without crashing.
    """
    conn = sqlite3.connect('users.db')  # Connect to the database
    cursor = conn.cursor()

    try:
        # Insert the new user's details into the 'users' table
        cursor.execute("INSERT INTO users (username, password, country) VALUES (?, ?, ?)", 
                       (username, password, country))
        conn.commit()  # Commit the transaction (save changes to the database)
        return True  # Return True if registration was successful
    except sqlite3.IntegrityError:
        # Return False if the username already exists (due to PRIMARY KEY constraint)
        return False
    finally:
        conn.close()  # Ensure the connection is closed whether successful or not

# Authenticate the user by checking the username and password
def authenticate_user(username, password):
    """
    Authenticates a user by checking if the provided username and password match an entry in the database.

    Parameters:
    username (str): The username provided by the user.
    password (str): The password provided by the user.

    Returns:
    str: The country associated with the user if authentication is successful.
    None: If the username and password do not match any entry in the database.

    This function queries the database for a matching username and password and returns the country.
    """
    conn = sqlite3.connect('users.db')  # Connect to the database
    cursor = conn.cursor()

    # Query the database for the user's country if the username and password match
    cursor.execute("SELECT country FROM users WHERE username = ? AND password = ?", (username, password))
    result = cursor.fetchone()  # Fetch one result (if it exists)

    conn.close()  # Close the connection to the database
    return result[0] if result else None  # Return the country if authentication is successful, otherwise None
