# conftest.py
"""
Pytest configuration and shared fixtures.
"""

import os
import sys

# Absolute path to the project root
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# Prepend the root directory to sys.path if it's not already there.
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)
