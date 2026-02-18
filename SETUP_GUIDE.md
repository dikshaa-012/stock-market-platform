# Stock Market Platform - Quick Setup Guide

## 🚀 Start Here

Follow these steps to get the application running on your machine.

### Step 1: Clone or Download the Project
```bash
cd "C:\Users\diksh\OneDrive\Desktop\New folder\stock-market-platform"
```

### Step 2: Set Up Python Environment

#### On Windows:
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

#### On macOS/Linux:
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Start the Backend Server

```bash
cd backend
python main.py
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

### Step 4: Test the API

Open your browser and go to:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **API Health**: http://localhost:8000/api/health

### Step 5: Access the Frontend Dashboard

Open the frontend in your browser:
1. **Option A**: Open `frontend/index.html` directly in your browser
2. **Option B**: Use a local server:
```bash
# In a new terminal
cd frontend
python -m http.server 8001
# Visit http://localhost:8001
```

## 📊 Testing the Application

### Via Swagger UI (Recommended)
1. Go to http://localhost:8000/docs
2. Click on any endpoint to expand it
3. Click "Try it out"
4. Modify parameters if needed
5. Click "Execute"

### Via Dashboard
1. Open the frontend
2. Navigate through different sections
3. Try searching for companies
4. Compare stocks
5. Analyze individual stocks

### Via curl Commands
```bash
# Get all companies
curl http://localhost:8000/api/companies

# Get INFY stock data
curl http://localhost:8000/api/stock/INFY?days=30

# Get summary statistics
curl http://localhost:8000/api/summary/INFY

# Compare stocks
curl http://localhost:8000/api/compare?ticker1=INFY&ticker2=TCS

# Get top gainers
curl http://localhost:8000/api/top-gainers

# Get volatility
curl http://localhost:8000/api/volatility/INFY
```

## 🔧 Project Structure

```
stock-market-platform/
├── backend/
│   ├── app/
│   │   ├── main.py              ← FastAPI app & routes
│   │   ├── models.py            ← Data models
│   │   ├── data_processor.py    ← Data cleaning & processing
│   │   ├── metrics.py           ← Financial calculations
│   │   └── __init__.py
│   └── main.py                  ← Entry point
├── frontend/
│   ├── index.html               ← Dashboard UI
│   ├── style.css                ← Styling
│   └── script.js                ← Interactive features
├── requirements.txt             ← Python dependencies
├── README.md                    ← Full documentation
├── API_DOCUMENTATION.md         ← API details
├── DATA_DOCUMENTATION.md        ← Data details
├── postman_collection.json      ← Postman requests
├── Dockerfile                   ← Docker configuration
├── docker-compose.yml           ← Docker compose setup
└── .gitignore                   ← Git ignore rules
```

## 🎯 Key Features to Try

### 1. Company Listing
- Click "Companies" tab
- See all 10 companies
- Search by ticker or name

### 2. Stock Analysis
- Enter ticker (e.g., INFY)
- Set time period
- View price trends
- See daily returns
- Check volatility metrics

### 3. Stock Comparison
- Enter two tickers (e.g., INFY & TCS)
- View side-by-side comparison
- See correlation between stocks
- Compare volatility and returns

### 4. Market Rankings
- View top 10 gainers
- View top 10 losers
- Filter by time period

## 📈 Available Companies

**IT Sector**
- INFY (Infosys)
- TCS (Tata Consultancy Services)
- WIPRO (Wipro)

**Banking**
- HDFCBANK (HDFC Bank)
- ICICIBANK (ICICI Bank)

**Other Sectors**
- RELIANCE (Energy)
- BAJAJFINSV (Finance)
- MARUTI (Automobile)
- NESTLEIND (FMCG)
- ITC (FMCG)

## 🐛 Troubleshooting

### Issue: "Module not found" error
**Solution**: Make sure you activated the virtual environment
```bash
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux
```

### Issue: Port 8000 already in use
**Solution**: Change the port in `backend/main.py`
```python
uvicorn.run(
    app,
    host="0.0.0.0",
    port=8001,  # Change to different port
    reload=True
)
```

### Issue: Frontend cannot connect to API
**Solution**: Make sure backend is running on port 8000
**Check**: Open http://localhost:8000/api/health

### Issue: CORS errors in browser console
**Solution**: CORS is already enabled for all origins (development mode)
For production, edit `backend/app/main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # Restrict in production
)
```

## 🚀 Deployment Options

### Option 1: Local Development
```bash
cd backend
python main.py
```

### Option 2: Docker
```bash
docker build -t stock-platform .
docker run -p 8000:8000 stock-platform
```

### Option 3: Docker Compose
```bash
docker-compose up
```

### Option 4: Heroku
```bash
# Create Procfile
web: gunicorn -w 4 -k uvicorn.workers.UvicornWorker backend.app.main:app

# Deploy
heroku create
git push heroku main
```

## 📚 Learning Resources

- **FastAPI**: https://fastapi.tiangolo.com/
- **Pandas**: https://pandas.pydata.org/docs/
- **Plotly**: https://plotly.com/javascript/
- **Docker**: https://docs.docker.com/

## 🤝 Need Help?

1. Check `API_DOCUMENTATION.md` for endpoint details
2. Check `DATA_DOCUMENTATION.md` for data structure
3. Read `README.md` for complete project information

## ✅ Verification Checklist

- [ ] Python 3.8+ installed
- [ ] Virtual environment created
- [ ] Dependencies installed (pip install -r requirements.txt)
- [ ] Backend starts without errors
- [ ] Swagger UI accessible at localhost:8000/docs
- [ ] Frontend dashboard opens
- [ ] Can see company list in dashboard
- [ ] Can analyze a stock
- [ ] Can compare two stocks

Once all items are checked, you're ready to go! 🎉

---

**Last Updated**: January 26, 2026
**Version**: 1.0.0
