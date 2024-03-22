"""
File: config.py
Author: Brianda Yáñez-Arrondo
Description: Configuration file for the chatbot assistant for citizen assemblies.
"""

import os
from pathlib import Path


# Get the current directory
current_dir = Path(os.getcwd())

# Define the data directory path
data_dir = current_dir.parent / 'data'

# Define other useful paths
config_dir = current_dir.parent / 'config'