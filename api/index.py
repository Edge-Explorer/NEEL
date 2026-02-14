import os
import sys

# Ensure the project root is in the path so Vercel can find the 'backend' module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.main import app

# Vercel looks for 'app' usually, but 'handler' or naming it 'app' is fine
# We are exposing the 'app' from backend.main
