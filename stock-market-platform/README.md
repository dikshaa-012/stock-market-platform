# Stock Market Data Platform

A comprehensive stock-market data platform built with FastAPI, demonstrating advanced Python programming, API development, data processing, and visualization skills.

## 📋 Features

### Backend API (FastAPI)
- **RESTful APIs** with Swagger/OpenAPI documentation
- **10 stock companies** with 365 days of synthetic historical data
- **Data cleaning** - duplicate removal, missing value handling, date format conversion
- **Financial metrics** - daily returns, 7-day moving average, 52-week high/low, volatility
- **Creative metrics** - annualized volatility, volatility trends, correlation analysis
- **Advanced endpoints** - list companies, get stock data, summary statistics, compare stocks
- **Top gainers/losers** - ranking system with time period filters

### Frontend Dashboard
- **Interactive UI** built with HTML5, CSS3, and vanilla JavaScript
- **Real-time charts** using Plotly.js and Chart.js
- **Company browser** with search functionality
- **Stock comparison** tool with correlation analysis
- **Detailed analysis** with price trends, returns visualization, and volatility stats
- **Responsive design** for desktop and mobile devices

### Data Processing
- **Multiple company support** - INFY, TCS, WIPRO, HDFCBANK, ICICIBANK, RELIANCE, etc.
- **Comprehensive cleaning** - handles duplicates, missing values, invalid data
- **Date format standardization** - consistent YYYY-MM-DD format
- **Financial calculations** - daily returns, moving averages, volatility metrics

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip or conda
- Modern web browser

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/stock-market-platform.git
cd stock-market-platform
```

2. **Create virtual environment**
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# OR
source venv/bin/activate  # macOS/Linux
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

### Running the Application

1. **Start the backend server**
```bash
cd backend
python main.py
```

The API will be available at `http://localhost:8000`
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

2. **Open the frontend dashboard**
```bash
# In another terminal, navigate to the frontend directory
cd frontend
# Open index.html in your browser or use a local server
python -m http.server 8001
# Visit http://localhost:8001
```

## 📚 API Endpoints

### Companies
- `GET /api/companies` - List all available companies

### Stock Data
- `GET /api/stock/{ticker}?days=30` - Get recent stock data
- `GET /api/summary/{ticker}` - Get summary statistics
- `GET /api/compare?ticker1=INFY&ticker2=TCS&days=30` - Compare two stocks

### Rankings
- `GET /api/top-gainers?days=7` - Top gaining stocks
- `GET /api/top-losers?days=7` - Top losing stocks

### Advanced Analytics
- `GET /api/volatility/{ticker}?days=30` - Volatility metrics (creative metric)

### System
- `GET /api/health` - Health check endpoint
- `GET /` - API information

## 📊 Data Structure

### Stock Data Response
```json
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
```

### Summary Statistics Response
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

## 🔬 Metrics Implemented

### Required Metrics
1. **Daily Returns** - Percentage change from previous close
2. **7-Day Moving Average** - Simple moving average over 7 days
3. **52-Week High/Low** - Maximum and minimum prices over 52 weeks

### Creative Metrics
1. **Volatility Analysis**
   - Daily volatility (standard deviation of returns)
   - Annualized volatility (252 trading days basis)
   - Volatility trend (increasing/decreasing)
   - High volatility days (outliers beyond 2 standard deviations)

2. **Stock Correlation** - Pearson correlation between two stock returns

3. **Volatility Ratio** - Comparative volatility between stocks

## 📂 Project Structure

```
stock-market-platform/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI application
│   │   ├── models.py            # Pydantic models
│   │   ├── data_processor.py    # Data cleaning and processing
│   │   └── metrics.py           # Financial metrics calculation
│   └── main.py                  # Entry point
├── frontend/
│   ├── index.html               # Dashboard UI
│   ├── style.css                # Styling
│   └── script.js                # Frontend logic
├── data/                        # Data storage (optional)
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## 🔧 Technologies Used

### Backend
- **FastAPI** - Modern, fast web framework
- **Uvicorn** - ASGI server
- **Pandas** - Data manipulation and analysis
- **NumPy** - Numerical computing
- **Pydantic** - Data validation

### Frontend
- **HTML5** - Semantic markup
- **CSS3** - Modern styling with gradients and animations
- **JavaScript (Vanilla)** - Interactive functionality
- **Plotly.js** - Interactive charts
- **Chart.js** - Bar and line charts

## 💡 Key Features Explained

### Data Cleaning
- **Duplicate Removal** - Removes duplicate date entries
- **Missing Value Handling** - Forward fill strategy for continuity
- **Data Validation** - Ensures high >= low and positive volumes
- **Format Standardization** - Consistent date format (YYYY-MM-DD)

### API Design
- **RESTful Principles** - Standard HTTP methods and status codes
- **CORS Support** - Cross-origin requests enabled
- **Error Handling** - Proper error responses with meaningful messages
- **Pagination Support** - Days parameter for time range filtering

### Frontend Features
- **Real-time Updates** - Dynamic data loading without page refresh
- **Interactive Charts** - Hover tooltips and zoom capabilities
- **Search & Filter** - Find companies by ticker or name
- **Responsive Design** - Works on desktop, tablet, and mobile

## 📈 Example Usage

### Get Company List
```bash
curl http://localhost:8000/api/companies
```

### Get Stock Data for Last 30 Days
```bash
curl http://localhost:8000/api/stock/INFY?days=30
```

### Compare Two Stocks
```bash
curl http://localhost:8000/api/compare?ticker1=INFY&ticker2=TCS&days=30
```

### Get Volatility Metrics
```bash
curl http://localhost:8000/api/volatility/INFY?days=30
```

## 🧪 Testing

The API is fully tested through the Swagger UI:
1. Navigate to `http://localhost:8000/docs`
2. Try out endpoints directly from the browser
3. View request/response schemas

## 📝 Postman Collection

Import the included Postman collection to test all endpoints:
1. Open Postman
2. Import `postman_collection.json`
3. Set environment variable: `BASE_URL = http://localhost:8000`
4. Run requests

## 🎯 Code Quality

- **Clean Code** - Well-organized, readable, and maintainable
- **Type Hints** - Full type annotations for better IDE support
- **Error Handling** - Comprehensive exception handling
- **Documentation** - Clear docstrings and comments
- **Modular Design** - Separation of concerns with dedicated modules

## 🚀 Deployment

### Local Deployment
```bash
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Production with Gunicorn
```bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker backend.app.main:app
```

### Docker (Optional)
Create a `Dockerfile`:
```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0"]
```

## 📊 Dashboard Screenshots

### Dashboard Overview
- Top gainers and losers
- Market statistics

### Stock Analysis
- Price trends with moving averages
- Daily returns visualization
- Volatility statistics

### Comparison Tool
- Side-by-side stock metrics
- Correlation analysis
- Volatility comparison

## 🔐 Future Enhancements

- Real-time data integration with yfinance or Alpha Vantage
- User authentication and portfolios
- Predictive models with machine learning
- Advanced charting with technical indicators
- Mobile app using React Native
- Database integration (PostgreSQL/MongoDB)
- Sentiment analysis from news feeds

## 📄 License

This project is open source and available under the MIT License.

## 👥 Author

Backend Developer Internship Project - 2026

## 🤝 Support

For issues or questions, please create an issue on GitHub or contact the development team.

---

**Happy investing! 📈**
