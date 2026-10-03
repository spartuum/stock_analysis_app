# utils/styling.py

def apply_styles(style):
    """
    Applies custom styles to the application's widgets using ttk's styling system.
    
    Parameters:
    style (ttk.Style): The ttk.Style object used to configure widget styles globally.

    This function sets the 'clam' theme as the base theme and customizes the appearance 
    of various widgets like frames, labels, buttons, and comboboxes with specific colors, 
    fonts, and behavior for active states.
    """
    style.theme_use('clam')  # Set the 'clam' theme as the base for consistent styling

    # Configure global styles for all widgets, setting a base background, text color, and font
    style.configure('.',
                    background='#f0f0f0',  # Light gray background for all widgets
                    foreground='#333333',  # Dark gray text color
                    font=('Arial', 12))  # Base font size and type for all widgets

    # Configure specific styles for individual widget types

    # Frame styling: light gray background
    style.configure('TFrame', background='#f0f0f0')

    # Label styling: light gray background and increased font size
    style.configure('TLabel', background='#f0f0f0', font=('Arial', 12))

    # Custom style for large buttons with green background and white text
    style.configure('Large.TButton', 
                    background='#4CAF50',  # Green background for buttons
                    foreground='#ffffff',  # White text on buttons
                    font=('Arial', 12, 'bold'))  # Bold font with increased size for buttons
    
    # Change button background color to a darker green when active (clicked or hovered)
    style.map('Large.TButton',
              background=[('active', '#45a049')])  # Darker green on active state

    # Increase font size and customize background for comboboxes
    style.configure('TCombobox', 
                    background='#ffffff',  # White background for combobox
                    font=('Arial', 12))  # Increased font size for combobox text
    
    # Keep the background white when combobox is in read-only state
    style.map('TCombobox',
              fieldbackground=[('readonly', '#ffffff')])

    # Attempt to increase the font size of the combobox's drop-down list (listbox)
    style.configure('TCombobox.Listbox', font=('Arial', 12))  # Larger font size for dropdown list items

    # Configure the plot frame style with a white background for the plot area
    style.configure('PlotFrame.TFrame', background='#ffffff')  # White background for plot frame
