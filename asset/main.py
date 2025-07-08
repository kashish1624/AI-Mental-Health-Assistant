import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "gui"))

from gui.dashboard import launch_dashboard

# Replace with actual user from login (we’ll pass this from login_window.py)
logged_in_user = "temp_user@example.com"  # Placeholder

create_dashboard(logged_in_user)

