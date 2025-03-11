#!/bin/bash
# Navigate to the project directory
# REPLACE THIS WITH THE ABSOLUTE PATH TO YOUR mysql-mcp folder
cd /Users/anands/code/sql-mcp

# Activate the virtual environment
source venv/bin/activate  # For Linux/macOS
# source venv/Scripts/activate  # For Windows (Git Bash)
# venv\Scripts\activate  # For Windows (cmd)

# Run the Python script
python sql.py

# Deactivate the virtual environment (optional)
deactivate
