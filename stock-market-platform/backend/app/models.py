from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class Company(BaseModel):
    """Company model"""
    ticker: str
    name: str
    sector: str

class StockData(BaseModel):
    """Stock data model"""
    ticker: str
    date: str
    open_price: float
    high_price: float
    low_price: float
    close_price: float
    volume: int
    daily_return: Optional[float] = None
    moving_avg_7: Optional[float] = None

class SummaryStats(BaseModel):
    """Summary statistics model"""
    ticker: str
    current_price: float
    high_52week: float
    low_52week: float
    moving_avg_7: float
    moving_avg_30: Optional[float] = None
    daily_return: float
    volatility: float
    price_range: float
    avg_volume: float
    total_data_points: int

class StockComparison(BaseModel):
    """Individual stock comparison data"""
    ticker: str
    current_price: float
    return_percent: float
    volatility: float
    highest_price: float
    lowest_price: float

class ComparisonResponse(BaseModel):
    """Comparison response model"""
    stock1: StockComparison
    stock2: StockComparison
    correlation: float
    volatility_ratio: float
    return_difference: float
    period_days: int

class VolatilityMetrics(BaseModel):
    """Volatility metrics"""
    ticker: str
    daily_volatility: float
    annualized_volatility: float
    volatility_trend: str
    high_volatility_days: int
    volatility_mean: float
    volatility_std: float

class TopStock(BaseModel):
    """Top stock entry"""
    ticker: str
    name: str
    return_percent: float
    price: float

class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    timestamp: datetime
    data_points: int
