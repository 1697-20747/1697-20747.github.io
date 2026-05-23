---
title: "Downloading Historical Stock Price Data with Python & Bash"
date: 2026-05-23T17:24:34Z
draft: false
categories: ["data-analytics"]
tags: ["data-analytics", "python", "bash", "yfinance", "automation", "stock-data", "historical-data"]
description: "A practical guide to automatically downloading 30+ years of historical stock price data using a bash script, Python virtual environments, and the yfinance library."
showToc: true
tocopen: true
cover:
  image: ""
  alt: ""
  caption: ""
---

## Overview

This post walks through a complete bash automation script that downloads historical stock price data for any ticker symbol. The script handles Python environment setup, dependency installation, and data download in a single command—no manual configuration required.

> It should not be this hard, regulators take note, especially the no longer listed history which is vital for survivor analysis. This bypasses any AI being locked out, by running the old format API access script directly on your machine. its bollocks that this is necessary, but it is what it is. Don't expect this to work for 1,000 stocks at one time.

The example uses **Groupe Casino (CO.PA)** to download 26 years of daily trading data (2000-2026), but the approach works for any publicly-traded stock.

---

## The Problem

Downloading historical stock price data typically requires:

1. ✗ Installing Python packages manually
2. ✗ Handling system protection errors (`externally-managed-environment`)
3. ✗ Creating virtual environments by hand
4. ✗ Writing and executing separate Python scripts
5. ✗ Managing file outputs

**The solution:** A single bash script that automates all of this.

---

## The Complete Bash Script

Here's the full automation script:

```bash
#!/bin/bash

# Stock Price Data Downloader - Automated Setup & Data Retrieval
# This script creates a Python virtual environment, installs dependencies,
# and downloads historical stock price data using yfinance

set -e  # Exit on any error

echo "======================================================================"
echo "STOCK PRICE DATA DOWNLOADER - AUTOMATED SETUP"
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

VENV_DIR="stock_data_venv"

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
echo "[3/4] Installing yfinance and pandas..."
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
echo "[4/4] Downloading historical stock price data..."
echo ""

SCRIPT_NAME="download_stock_prices.py"

cat > "$SCRIPT_NAME" << 'PYEOF'
#!/usr/bin/env python3
"""
Historical Stock Price Data Downloader
Automatically downloads historical data for any ticker from 1990 to today
"""

import yfinance as yf
import pandas as pd
from datetime import datetime
import sys

print("=" * 70)
print("HISTORICAL STOCK PRICE DATA DOWNLOADER")
print("=" * 70)
print()

try:
    # Get ticker symbol from user or use default
    ticker = input("Enter stock ticker (e.g., CO.PA, AAPL, MSFT): ").strip().upper()
    if not ticker:
        ticker = "CO.PA"  # Default to Casino if no input
    
    print()
    print("Downloading historical data from Yahoo Finance...")
    print(f"  Ticker: {ticker}")
    print("  Period: 1990-01-01 to Today")
    print("  This may take 1-2 minutes...")
    print()
    
    # Download data
    stock_data = yf.download(ticker, start='1990-01-01', progress=True)
    
    # Add some calculations
    stock_data['Percent_Change'] = stock_data['Close'].pct_change() * 100
    stock_data['MA_50'] = stock_data['Close'].rolling(window=50).mean()
    stock_data['MA_200'] = stock_data['Close'].rolling(window=200).mean()
    
    # Reset index to make Date a column
    df = stock_data.reset_index()
    
    # Save to CSV
    output_file = f'{ticker}_historical.csv'
    df.to_csv(output_file, index=False)
    
    print()
    print("=" * 70)
    print("✓ DATA DOWNLOADED SUCCESSFULLY")
    print("=" * 70)
    print()
    print(f"File saved: {output_file}")
    print(f"Total records: {len(df)}")
    print(f"Date range: {df['Date'].min()} to {df['Date'].max()}")
    print()
    print("Columns in file:")
    for col in df.columns:
        print(f"  • {col}")
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
    print("  2. Verify the ticker symbol is correct")
    print("  3. Try again in a few moments")
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
    echo "Next steps:"
    echo "  1. Locate the CSV file in this directory"
    echo "  2. Use it for data analysis, charting, or further processing"
    echo "  3. To activate venv again: source stock_data_venv/bin/activate"
    echo ""
else
    echo ""
    echo "======================================================================"
    echo "⚠ DOWNLOAD FAILED"
    echo "======================================================================"
    echo ""
    exit 1
fi
```

---

## How It Works: Step-by-Step

### Step 1: Python Version Check

```bash
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 not found"
    exit 1
fi
```

- Verifies Python 3 is installed before proceeding
- `command -v` searches for the executable
- `&> /dev/null` suppresses output
- `exit 1` stops the script if Python isn't found

### Step 2: Virtual Environment Setup

```bash
VENV_DIR="stock_data_venv"

if [ ! -d "$VENV_DIR" ]; then
    python3 -m venv "$VENV_DIR"
fi

source "$VENV_DIR/bin/activate"
```

**Why virtual environments?**
- Isolates Python packages from system Python
- Avoids "externally-managed-environment" errors
- Prevents conflicting package versions
- Easy cleanup (just delete the folder)

### Step 3: Dependency Installation

```bash
pip install --upgrade pip yfinance pandas > /dev/null 2>&1
```

**What's happening:**
- `pip install --upgrade pip` - Updates pip itself
- `yfinance` - Library for downloading stock data from Yahoo Finance
- `pandas` - Data manipulation library
- `> /dev/null 2>&1` - Suppresses verbose output
- `$?` - Captures the exit code (0 = success)

### Step 4: Create & Run Python Script

```bash
cat > "$SCRIPT_NAME" << 'PYEOF'
# ... Python code here ...
PYEOF
```

This uses a **heredoc** to:
- Create a Python file on the fly
- Include the full Python script inline
- Execute it immediately after creation

---

## The Python Data Download Script

The embedded Python script handles the actual data retrieval:

```python
# Get ticker from user
ticker = input("Enter stock ticker (e.g., CO.PA, AAPL, MSFT): ").strip().upper()

# Download data
stock_data = yf.download(ticker, start='1990-01-01', progress=True)

# Add calculations
stock_data['Percent_Change'] = stock_data['Close'].pct_change() * 100
stock_data['MA_50'] = stock_data['Close'].rolling(window=50).mean()
stock_data['MA_200'] = stock_data['Close'].rolling(window=200).mean()

# Save to CSV
df.to_csv(f'{ticker}_historical.csv', index=False)
```

---

## Output Data Structure

The script generates a CSV with these columns:

```
Date,Open,High,Low,Close,Volume,Percent_Change,MA_50,MA_200
2026-05-22,0.225,0.235,0.22,0.23,816691,-2.13,0.28,0.45
2026-05-21,0.231,0.237,0.22,0.235,963545,1.29,0.30,0.47
...
1990-01-01,3.50,3.60,3.48,3.52,0,0.57,NaN,NaN
```

- **OHLCV**: Open, High, Low, Close, Volume
- **Percent_Change**: Daily % change
- **MA_50 & MA_200**: 50-day and 200-day moving averages

---

## Running the Script

### Prerequisites

```bash
python3 --version
chmod +x setup_and_download_stock_prices.sh
```

### Execute

```bash
bash setup_and_download_stock_prices.sh
```

### Output Example

```
======================================================================
STOCK PRICE DATA DOWNLOADER - AUTOMATED SETUP
======================================================================

[1/4] Checking Python 3 installation...
✓ Found: Python 3.14.5

[2/4] Creating Python virtual environment...
✓ Virtual environment created: stock_data_venv

[3/4] Installing yfinance and pandas...
✓ Python packages installed successfully

[4/4] Downloading historical stock price data...
Enter stock ticker (e.g., CO.PA, AAPL, MSFT): CO.PA

Downloading historical data from Yahoo Finance...
[########|########|########] 100%

✓ DATA DOWNLOADED SUCCESSFULLY

File saved: CO.PA_historical.csv
Total records: 6779
```

---

## Use Cases

### Data Analysis
```python
import pandas as pd
df = pd.read_csv('CO.PA_historical.csv')
print(df.describe())
```

### Charting
```python
import matplotlib.pyplot as plt
df['Date'] = pd.to_datetime(df['Date'])
plt.plot(df['Date'], df['Close'])
plt.show()
```

### Technical Analysis
```python
df['Signal'] = df['MA_50'] > df['MA_200']
buy_signals = df[df['Signal'] == True]
```

### Risk Analysis
```python
df['Volatility'] = df['Percent_Change'].rolling(window=30).std()
```

---

## Advantages

| Feature | Benefit |
|---------|---------|
| Single command | No manual setup required |
| Virtual environment | Avoids system Python conflicts |
| Automated | No user interaction (except ticker) |
| Error handling | Fails gracefully with clear messages |
| Reproducible | Same result every time |
| Flexible | Works with any publicly-traded ticker |
| Clean | Self-contained in one folder |

---

## Limitations

- **Data availability**: Yahoo Finance may not have data for very old stocks
- **Delisted tickers**: Removed companies may have limited historical data
- **Rate limiting**: Downloading multiple tickers quickly may be throttled

---

## Troubleshooting

### "Python 3 not found"
```bash
brew install python3  # macOS
```

### Download hangs or times out
- Check your internet connection
- Try a different ticker
- Wait a few minutes and try again

### Virtual environment activation issues
```bash
source stock_data_venv/bin/activate
python3 download_stock_prices.py
```

---

## Full Script Reference

**[→ Download: setup_and_download_stock_prices.sh](./setup_and_download_stock_prices.sh)**

Save this file, make it executable, and run:

```bash
bash setup_and_download_stock_prices.sh
```

---

## Key Takeaways

- ✓ Bash scripts automate complex Python workflows
- ✓ Virtual environments prevent system Python conflicts
- ✓ yfinance makes accessing historical data trivial
- ✓ A single script encapsulates entire data pipelines
- ✓ Error handling ensures reproducible results
- ✓ This approach scales to any financial ticker

---

**Ready to download stock data?** Run the bash script and get started!

## Download the Script

The complete bash script is available for download:

**[→ Download: setup_and_download_stock_prices.sh](./setup_and_download_stock_prices.sh)**

Save this file to your computer, make it executable with:

```bash
chmod +x setup_and_download_stock_prices.sh
```

Then run it:

```bash
bash setup_and_download_stock_prices.sh
```
