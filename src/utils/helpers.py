def get_shortcut_path(shortcut_name):
    # This function returns the full path of a given shortcut name
    import os
    import ctypes

    # Get the path to the user's desktop
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    
    # Construct the full path to the shortcut
    shortcut_path = os.path.join(desktop_path, f"{shortcut_name}.lnk")
    
    # Check if the shortcut exists
    if os.path.exists(shortcut_path):
        return shortcut_path
    else:
        return None

def format_shortcut_list(shortcut_list):
    # This function formats a list of shortcuts into a string for display
    return "\n".join(shortcut_list) if shortcut_list else "No shortcuts available."