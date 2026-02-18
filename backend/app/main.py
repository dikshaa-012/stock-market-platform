from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from datetime import datetime, timedelta
import pandas as pd
from typing import List, Optional
import os

from .models import Company, StockData, ComparisonResponse, SummaryStats
from .data_processor import DataProcessor
from .metrics import MetricsCalculator

app = FastAPI(
    title="Stock Market Data Platform",
    description="A comprehensive API for stock market data analysis",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize processors
processor = DataProcessor()
metrics_calc = MetricsCalculator()

@app.on_event("startup")
async def startup_event():
    """Initialize data on startup"""
    processor.load_sample_data()
    print("Stock Market Platform initialized successfully")

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Stock Market Data Platform API",
        "docs": "/docs",
        "version": "1.0.0"
    }

@app.get("/api/companies", response_model=List[Company])
async def list_companies():
    """List all available companies"""
    try:
        companies = processor.get_all_companies()
        return companies
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/stock/{ticker}", response_model=List[StockData])
async def get_stock_data(
    ticker: str,
    days: Optional[int] = Query(30, ge=1, le=365)
):
    """
    Get recent stock data for a specific ticker
    
    - **ticker**: Stock ticker symbol (e.g., INFY, TCS)
    - **days**: Number of days of historical data (default: 30, max: 365)
    """
    try:
        data = processor.get_stock_data(ticker, days)
        if not data:
            raise HTTPException(status_code=404, detail=f"No data found for ticker {ticker}")
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/summary/{ticker}", response_model=SummaryStats)
async def get_summary_stats(ticker: str):
    """
    Get summary statistics for a stock
    
    Includes:
    - Current price, high, low
    - Daily returns
    - 7-day moving average
    - 52-week high/low
    - Volatility
    - Price range
    """
    try:
        stats = metrics_calc.calculate_summary_stats(ticker, processor)
        if not stats:
            raise HTTPException(status_code=404, detail=f"No data found for ticker {ticker}")
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/compare")
async def compare_stocks(
    ticker1: str = Query(..., description="First stock ticker"),
    ticker2: str = Query(..., description="Second stock ticker"),
    days: Optional[int] = Query(30, ge=1, le=365)
):
    """
    Compare two stocks
    
    Returns comparative metrics including:
    - Price trends
    - Returns comparison
    - Volatility comparison
    - Correlation between stocks
    """
    try:
        comparison = metrics_calc.compare_stocks(ticker1, ticker2, days, processor)
        if not comparison:
            raise HTTPException(status_code=404, detail="Could not compare stocks")
        return comparison
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/top-gainers")
async def get_top_gainers(days: Optional[int] = Query(7, ge=1, le=365)):
    """Get top gaining stocks for the specified period"""
    try:
        gainers = metrics_calc.get_top_gainers(days, processor)
        return {"gainers": gainers[:10]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/top-losers")
async def get_top_losers(days: Optional[int] = Query(7, ge=1, le=365)):
    """Get top losing stocks for the specified period"""
    try:
        losers = metrics_calc.get_top_losers(days, processor)
        return {"losers": losers[:10]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/volatility/{ticker}")
async def get_volatility(ticker: str, days: Optional[int] = Query(30, ge=1, le=365)):
    """
    Get volatility metrics for a stock
    
    Creative Metric: Calculates annualized volatility, daily volatility,
    and volatility trend over the period
    """
    try:
        volatility = metrics_calc.calculate_volatility(ticker, days, processor)
        if not volatility:
            raise HTTPException(status_code=404, detail=f"No data found for ticker {ticker}")
        return volatility
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "data_points": processor.get_total_data_points()
    }
