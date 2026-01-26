# Data Documentation

## Data Source
The platform uses synthetically generated stock data for demonstration purposes. Each company has 365 days of historical data generated using realistic market simulation.

## Data Generation Process

### Base Configuration
- Historical period: 365 days from today
- Number of companies: 10
- Data frequency: Daily (including only trading days)

### Price Generation
1. **Base Price**: Random initial price between ₹100 and ₹5000
2. **Daily Returns**: Normal distribution with mean=0.0005, std=0.02
3. **OHLCV Calculation**:
   - Opening: ±2% variation from previous close
   - Closing: ±2% variation from simulated price
   - High: Max(Open, Close) × random(1.00-1.02)
   - Low: Min(Open, Close) × random(0.98-1.00)
   - Volume: Random 1M-10M shares

## Data Cleaning Pipeline

### Step 1: Duplicate Removal
```python
df = df.drop_duplicates(subset=['date'])
```
Removes any duplicate date entries.

### Step 2: Missing Value Handling
```python
df['close'] = df['close'].fillna(method='ffill').fillna(method='bfill')
df['volume'] = df['volume'].fillna(0)
```
- Forward fill for OHLC prices
- Zero fill for volume (if trading halted)

### Step 3: Date Format Standardization
```python
df['date'] = pd.to_datetime(df['date'])
```
Converts to ISO 8601 format: YYYY-MM-DD

### Step 4: Data Validation
```python
df = df[(df['close'] > 0) & (df['high'] >= df['low'])]
```
Ensures:
- All prices > 0
- High price >= Low price
- Valid OHLC relationships

## Data Structure

### Raw CSV Format (if imported from external source)
```csv
date,open,high,low,close,volume
2025-01-26,1500.50,1510.25,1495.75,1505.00,5000000
2025-01-27,1505.00,1520.00,1500.00,1515.50,5500000
```

### In-Memory Structure (Python)
```python
{
    'ticker': 'INFY',
    'data': [
        {
            'date': '2025-01-26',
            'open': 1500.50,
            'high': 1510.25,
            'low': 1495.75,
            'close': 1505.00,
            'volume': 5000000
        }
    ]
}
```

### API Response Format
```json
{
    "ticker": "INFY",
    "date": "2025-01-26",
    "open_price": 1500.50,
    "high_price": 1510.25,
    "low_price": 1495.75,
    "close_price": 1505.00,
    "volume": 5000000,
    "daily_return": 0.32,
    "moving_avg_7": 1502.14
}
```

## Calculated Metrics

### 1. Daily Returns
```python
daily_return = (close_price - previous_close) / previous_close * 100
```
Represents percentage change from previous day's close.

### 2. 7-Day Moving Average
```python
ma_7 = df['close'].rolling(window=7, min_periods=1).mean()
```
Simple moving average over 7 days.

### 3. 30-Day Moving Average
```python
ma_30 = df['close'].rolling(window=30, min_periods=1).mean()
```
Simple moving average over 30 days.

### 4. 52-Week High/Low
```python
high_52week = df[df['date'] >= one_year_ago]['high'].max()
low_52week = df[df['date'] >= one_year_ago]['low'].min()
```
Maximum and minimum prices over the last year.

### 5. Volatility (Creative Metric)
```python
daily_volatility = returns.std()
annualized_volatility = daily_volatility * sqrt(252)  # 252 trading days
```
Standard deviation of daily returns, annualized for comparison.

### 6. Correlation (Creative Metric)
```python
correlation = stock1_returns.corr(stock2_returns)
```
Pearson correlation between two stocks' daily returns.

## Data Quality Metrics

### Completeness
- Target: 100% for all trading days
- Current: 100% (365 days per company)

### Validity
- Price ranges: ₹100 - ₹5000
- Volume: 1M - 10M shares
- All OHLC relationships valid

### Consistency
- Dates in chronological order
- No duplicate entries
- Uniform interval (daily)

## Storage

### In-Memory (Current)
Data is generated at application startup and stored in Python dictionaries. No persistent storage.

### Future: Database Options
- SQLite: For development/testing
- PostgreSQL: For production
- MongoDB: For flexible schema

## Companies in Dataset

| Ticker | Name | Sector | Base Price |
|--------|------|--------|-----------|
| INFY | Infosys | IT | ~₹1500 |
| TCS | TCS | IT | ~₹3500 |
| WIPRO | Wipro | IT | ~₹500 |
| HDFCBANK | HDFC Bank | Banking | ~₹1600 |
| ICICIBANK | ICICI Bank | Banking | ~₹1000 |
| RELIANCE | Reliance | Energy | ~₹2500 |
| BAJAJFINSV | Bajaj Finserv | Finance | ~₹1800 |
| MARUTI | Maruti Suzuki | Automobile | ~₹9000 |
| NESTLEIND | Nestle India | FMCG | ~₹2000 |
| ITC | ITC | FMCG | ~₹420 |

## Importing Real Data

To use real data from external sources:

### Option 1: yfinance
```python
import yfinance as yf
data = yf.download('INFY.NS', start='2025-01-26', end='2026-01-26')
```

### Option 2: Alpha Vantage API
```python
from alpha_vantage.timeseries import TimeSeries
ts = TimeSeries(key='YOUR_KEY')
data, meta = ts.get_daily('INFY')
```

### Option 3: CSV Files
```python
import pandas as pd
df = pd.read_csv('stock_data.csv')
```

## Data Privacy

No real personal data is used. All data is synthetic or publicly available market data.

## Update Frequency

In this version, data is static (365 historical days). Future versions will include:
- Real-time data feeds
- Daily updates at market close
- Intraday data (5-min, 15-min candles)

## Data Retention

Current implementation: Data kept in memory for session duration.

Future implementation: Configure data retention policies:
- 5 years of daily data
- 2 years of intraday data
- 1 year of tick data
