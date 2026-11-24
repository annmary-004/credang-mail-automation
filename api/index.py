import sys
import os

current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)
backend_dir = os.path.join(parent_dir, "backend")

sys.path.insert(0, parent_dir)
sys.path.insert(0, backend_dir)

from backend.main import app
