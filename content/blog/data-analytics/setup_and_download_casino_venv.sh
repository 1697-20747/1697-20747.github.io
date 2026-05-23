#!/bin/bash

# Casino Share Price Data - Setup using Python Virtual Environment
# This script creates a virtual environment and downloads historical data

set -e  # Exit on any error

echo "======================================================================"
echo "GROUPE CASINO (CO.PA) - AUTOMATIC SETUP & DATA DOWNLOAD"
echo "======================================================================"
echo ""

# Step 1: Check if Python 3 is installed
echo "[1/4] Checking Python 3 installation..."
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 not found"
    exit 1
fi

PYTHON_VERSION=$(python3 --version)
echo "✓ Found: $PYTHON_VERSION"
echo ""

# Step 2: Create virtual environment
echo "[2/4] Creating Python virtual environment..."

VENV_DIR="casino_venv"

if [ ! -d "$VENV_DIR" ]; then
    python3 -m venv "$VENV_DIR"
    echo "✓ Virtual environment created: $VENV_DIR"
else
    echo "✓ Virtual environment already exists: $VENV_DIR"
fi

# Activate virtual environment
source "$VENV_DIR/bin/activate"
echo "✓ Virtual environment activated"
echo ""

# Step 3: Install required packages in virtual environment
echo "[3/4] Installing yfinance and pandas in virtual environment..."
pip install --upgrade pip yfinance pandas > /dev/null 2>&1

if [ $? -eq 0 ]; then
    echo "✓ Python packages installed successfully"
else
    echo "ERROR: Failed to install packages"
    deactivate
    exit 1
fi
echo ""

# Step 4: Create and run the download script
echo "[4/4] Downloading Casino historical price data..."
echo ""

SCRIPT_NAME="download_casino_prices.py"

cat > "$SCRIPT_NAME" << 'PYEOF'
#!/usr/bin/env python3
"""
Casino Share Price Data Downloader
Automatically downloads historical data for CO.PA from 1994 to today
"""

import yfinance as yf
import pandas as pd
from datetime import datetime
import sys

print("=" * 70)
print("GROUPE CASINO (CO.PA) - HISTORICAL PRICE DOWNLOADER")
print("=" * 70)
print()

try:
    print("Downloading historical data from Yahoo Finance...")
    print("  Ticker: CO.PA")
    print("  Period: 1994-01-01 to Today")
    print("  This may take 1-2 minutes...")
    print()
    
    # Download data
    casino = yf.download('CO.PA', start='1994-01-01', progress=True)
    
    # Add some calculations
    casino['Percent_Change'] = casino['Close'].pct_change() * 100
    casino['MA_50'] = casino['Close'].rolling(window=50).mean()
    casino['MA_200'] = casino['Close'].rolling(window=200).mean()
    
    # Reset index to make Date a column
    casino_df = casino.reset_index()
    
    # Save to CSV
    output_file = 'casino_co_pa_historical.csv'
    casino_df.to_csv(output_file, index=False)
    
    print()
    print("=" * 70)
    print("✓ DATA DOWNLOADED SUCCESSFULLY")
    print("=" * 70)
    print()
    print(f"File saved: {output_file}")
    print(f"Total records: {len(casino_df)}")
    print(f"Date range: {casino_df['Date'].min()} to {casino_df['Date'].max()}")
    print()
    print("Columns in file:")
    for col in casino_df.columns:
        print(f"  • {col}")
    print()
    print("CSV File Preview (first 5 rows):")
    print(casino_df.head().to_string())
    print()
    print("CSV File Preview (last 5 rows):")
    print(casino_df.tail().to_string())
    print()
    print("=" * 70)
    print("SUCCESS: Casino price data is ready!")
    print("=" * 70)
    print()
    print("Next steps:")
    print("  1. Find the file: casino_co_pa_historical.csv")
    print("  2. Upload it to Claude")
    print("  3. Ask me to create the share price chart")
    print()
    
except ImportError as e:
    print("ERROR: Missing required package")
    print(f"Details: {e}")
    sys.exit(1)

except Exception as e:
    print(f"ERROR: {e}")
    print()
    print("Troubleshooting:")
    print("  1. Check your internet connection")
    print("  2. Try running again in a few moments")
    sys.exit(1)
PYEOF

chmod +x "$SCRIPT_NAME"
python3 "$SCRIPT_NAME"

DOWNLOAD_STATUS=$?

# Deactivate virtual environment
deactivate

if [ $DOWNLOAD_STATUS -eq 0 ]; then
    echo ""
    echo "======================================================================"
    echo "✓ ALL STEPS COMPLETED SUCCESSFULLY"
    echo "======================================================================"
    echo ""
    echo "CSV file location: casino_co_pa_historical.csv"
    echo ""
    echo "NEXT STEP:"
    echo "  1. Upload casino_co_pa_historical.csv to Claude"
    echo "  2. Ask: 'Create a professional share price chart from this data'"
    echo ""
else
    echo ""
    echo "======================================================================"
    echo "⚠ DOWNLOAD FAILED"
    echo "======================================================================"
    echo ""
    exit 1
fi

