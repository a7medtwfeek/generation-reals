"""
Vercel Serverless Function Entry Point
This file is required for Vercel deployment
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import the Flask app
from main_final import app

# Export for Vercel
handler = app
