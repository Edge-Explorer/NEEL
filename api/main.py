import os
import sys

# Add project root to sys.path
root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_path not in sys.path:
    sys.path.append(root_path)

from backend.main import app

# Important for Vercel: expose 'app' or 'handler'
# Using 'app' since that's what FastAPI usually uses
