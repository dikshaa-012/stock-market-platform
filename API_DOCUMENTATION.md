# API Documentation

## Authentication
Currently, no authentication is required. All endpoints are public.

## Rate Limiting
No rate limiting is implemented in this version.

## Response Codes

| Code | Description |
|------|-------------|
| 200  | Success |
| 404  | Resource not found |
| 422  | Validation error |
| 500  | Server error |

## Error Response Format

```json
{
  "detail": "Error message here"
}
```

## Data Types

### Price
All prices are in decimal format (₹ Indian Rupees) with 2 decimal places.

### Dates
All dates are in ISO 8601 format: `YYYY-MM-DD`

### Volumes
Volume is an integer representing number of shares traded.

### Returns/Percentages
Returns and percentages are decimal values representing percentage change.
Example: 2.5 means +2.5%

## Pagination

Use the `days` parameter to fetch historical data:
- Minimum: 1 day
- Maximum: 365 days
- Default: 30 days

## Available Tickers

| Ticker | Company | Sector |
|--------|---------|--------|
| INFY | Infosys | IT |
| TCS | Tata Consultancy Services | IT |
| WIPRO | Wipro | IT |
| HDFCBANK | HDFC Bank | Banking |
| ICICIBANK | ICICI Bank | Banking |
| RELIANCE | Reliance Industries | Energy |
| BAJAJFINSV | Bajaj Finserv | Finance |
| MARUTI | Maruti Suzuki | Automobile |
| NESTLEIND | Nestle India | FMCG |
| ITC | ITC | FMCG |

## Detailed Endpoint Documentation

### GET /api/companies

**Description**: Returns a list of all available companies in the platform.

**Response**:
```json
[
  {
    "ticker": "INFY",
    "name": "Infosys",
    "sector": "IT"
  }
]
```

---

### GET /api/stock/{ticker}

**Description**: Returns stock data for a specific ticker.

**Parameters**:
- `ticker` (path, required): Stock ticker symbol
- `days` (query, optional): Number of days (1-365, default: 30)

**Response**:
```json
[
  {
    "ticker": "INFY",
    "date": "2026-01-26",
    "open_price": 1500.50,
    "high_price": 1510.25,
    "low_price": 1495.75,
    "close_price": 1505.00,
    "volume": 5000000,
    "daily_return": 0.32,
    "moving_avg_7": 1502.14
  }
]
```

---

### GET /api/summary/{ticker}

**Description**: Returns summary statistics for a stock.

**Parameters**:
- `ticker` (path, required): Stock ticker symbol

**Response**:
```json
{
  "ticker": "INFY",
  "current_price": 1505.00,
  "high_52week": 2000.00,
  "low_52week": 1000.00,
  "moving_avg_7": 1502.14,
  "moving_avg_30": 1480.50,
  "daily_return": 0.32,
  "volatility": 2.45,
  "price_range": 1000.00,
  "avg_volume": 4500000,
  "total_data_points": 365
}
```

---

### GET /api/compare

**Description**: Compares two stocks with correlation analysis.

**Parameters**:
- `ticker1` (query, required): First stock ticker
- `ticker2` (query, required): Second stock ticker
- `days` (query, optional): Period in days (1-365, default: 30)

**Response**:
```json
{
  "stock1": {
    "ticker": "INFY",
    "current_price": 1505.00,
    "return_percent": 15.5,
    "volatility": 0.0245,
    "highest_price": 2000.00,
    "lowest_price": 1000.00
  },
  "stock2": {
    "ticker": "TCS",
    "current_price": 3500.00,
    "return_percent": 12.3,
    "volatility": 0.0198,
    "highest_price": 4000.00,
    "lowest_price": 2500.00
  },
  "correlation": 0.7234,
  "volatility_ratio": 1.2373,
  "return_difference": 3.2,
  "period_days": 30
}
```

---

### GET /api/top-gainers

**Description**: Returns top 10 gaining stocks.

**Parameters**:
- `days` (query, optional): Period in days (1-365, default: 7)

**Response**:
```json
{
  "gainers": [
    {
      "ticker": "INFY",
      "name": "Infosys",
      "return_percent": 25.5,
      "price": 1505.00
    }
  ]
}
```

---

### GET /api/top-losers

**Description**: Returns top 10 losing stocks.

**Parameters**:
- `days` (query, optional): Period in days (1-365, default: 7)

**Response**:
```json
{
  "losers": [
    {
      "ticker": "WIPRO",
      "name": "Wipro",
      "return_percent": -15.3,
      "price": 420.00
    }
  ]
}
```

---

### GET /api/volatility/{ticker}

**Description**: Returns comprehensive volatility metrics (creative metric).

**Parameters**:
- `ticker` (path, required): Stock ticker symbol
- `days` (query, optional): Period in days (1-365, default: 30)

**Response**:
```json
{
  "ticker": "INFY",
  "daily_volatility": 0.0245,
  "annualized_volatility": 0.3888,
  "volatility_trend": "Increasing",
  "high_volatility_days": 8,
  "volatility_mean": 0.0005,
  "volatility_std": 0.0245
}
```

---

### GET /api/health

**Description**: Health check endpoint.

**Response**:
```json
{
  "status": "healthy",
  "timestamp": "2026-01-26T10:30:00",
  "data_points": 3650
}
```

## Usage Examples

### Example 1: Get INFY Stock Data
```bash
curl http://localhost:8000/api/stock/INFY?days=30
```

### Example 2: Compare INFY and TCS
```bash
curl http://localhost:8000/api/compare?ticker1=INFY&ticker2=TCS&days=30
```

### Example 3: Get Top Gainers for Last 7 Days
```bash
curl http://localhost:8000/api/top-gainers?days=7
```

### Example 4: Get Volatility Metrics
```bash
curl http://localhost:8000/api/volatility/INFY?days=30
```

## Webhook Support (Future)

Webhooks for real-time price updates are planned for future versions.

## Rate Limits (Future)

Rate limiting will be implemented in future versions to prevent abuse.

## Versioning

Current API version: 1.0.0

API endpoints will maintain backward compatibility for at least 2 versions.
