"""
Test configuration for pytest

This file is automatically loaded by pytest and sets up the Python path
so tests can import modules from the project.
"""

import os
import sys

# Add project root to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)
