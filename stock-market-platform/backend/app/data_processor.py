import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List, Optional, Dict
import os
import json
from pathlib import Path

from .models import StockData, Company

class DataProcessor:
    """Handles data loading, cleaning, and processing"""
    
    def __init__(self):
        self.data = {}
        self.companies = {}
        
    def load_sample_data(self):
        """Load sample stock data"""
        companies_info = {
            'INFY': {'name': 'Infosys', 'sector': 'IT'},
            'TCS': {'name': 'Tata Consultancy Services', 'sector': 'IT'},
            'WIPRO': {'name': 'Wipro', 'sector': 'IT'},
            'HDFCBANK': {'name': 'HDFC Bank', 'sector': 'Banking'},
            'ICICIBANK': {'name': 'ICICI Bank', 'sector': 'Banking'},
            'RELIANCE': {'name': 'Reliance Industries', 'sector': 'Energy'},
            'BAJAJFINSV': {'name': 'Bajaj Finserv', 'sector': 'Finance'},
            'MARUTI': {'name': 'Maruti Suzuki', 'sector': 'Automobile'},
            'NESTLEIND': {'name': 'Nestle India', 'sector': 'FMCG'},
            'ITC': {'name': 'ITC', 'sector': 'FMCG'},
        }
        
        # Generate synthetic data for each company
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365)
        
        for ticker, info in companies_info.items():
            self.companies[ticker] = Company(
                ticker=ticker,
                name=info['name'],
                sector=info['sector']
            )
            
            # Generate synthetic OHLCV data
            dates = pd.date_range(start=start_date, end=end_date, freq='D')
            base_price = np.random.uniform(100, 5000)
            
            prices = []
            current_price = base_price
            
            for date in dates:
                daily_return = np.random.normal(0.0005, 0.02)
                current_price *= (1 + daily_return)
                
                open_price = current_price * np.random.uniform(0.98, 1.02)
                close_price = current_price * np.random.uniform(0.98, 1.02)
                high_price = max(open_price, close_price) * np.random.uniform(1.00, 1.02)
                low_price = min(open_price, close_price) * np.random.uniform(0.98, 1.00)
                volume = np.random.randint(1000000, 10000000)
                
                prices.append({
                    'date': date.strftime('%Y-%m-%d'),
                    'open': round(open_price, 2),
                    'high': round(high_price, 2),
                    'low': round(low_price, 2),
                    'close': round(close_price, 2),
                    'volume': int(volume)
                })
            
            self.data[ticker] = prices
    
    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean stock data"""
        # Remove duplicates
        df = df.drop_duplicates(subset=['date'])
        
        # Handle missing values
        df['close'] = df['close'].fillna(method='ffill').fillna(method='bfill')
        df['volume'] = df['volume'].fillna(0)
        
        # Convert date to datetime
        df['date'] = pd.to_datetime(df['date'])
        
        # Sort by date
        df = df.sort_values('date').reset_index(drop=True)
        
        # Ensure price data is valid
        df = df[(df['close'] > 0) & (df['high'] >= df['low'])]
        
        return df
    
    def calculate_moving_averages(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate moving averages"""
        df['ma7'] = df['close'].rolling(window=7, min_periods=1).mean()
        df['ma30'] = df['close'].rolling(window=30, min_periods=1).mean()
        return df
    
    def calculate_returns(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate daily returns"""
        df['daily_return'] = df['close'].pct_change() * 100
        return df
    
    def get_stock_data(self, ticker: str, days: int = 30) -> List[StockData]:
        """Get stock data for specified ticker"""
        if ticker not in self.data:
            return []
        
        raw_data = self.data[ticker]
        df = pd.DataFrame(raw_data)
        
        # Clean data
        df = self.clean_data(df)
        
        # Calculate metrics
        df = self.calculate_returns(df)
        df = self.calculate_moving_averages(df)
        
        # Get last N days
        df = df.tail(days)
        
        # Convert to StockData objects
        result = []
        for _, row in df.iterrows():
            stock_data = StockData(
                ticker=ticker,
                date=row['date'].strftime('%Y-%m-%d'),
                open_price=row['open'],
                high_price=row['high'],
                low_price=row['low'],
                close_price=row['close'],
                volume=row['volume'],
                daily_return=round(row['daily_return'], 2) if pd.notna(row['daily_return']) else None,
                moving_avg_7=round(row['ma7'], 2) if pd.notna(row['ma7']) else None
            )
            result.append(stock_data)
        
        return result
    
    def get_all_companies(self) -> List[Company]:
        """Get all available companies"""
        return list(self.companies.values())
    
    def get_total_data_points(self) -> int:
        """Get total number of data points"""
        return sum(len(v) for v in self.data.values())
    
    def get_raw_dataframe(self, ticker: str, days: int = 365) -> Optional[pd.DataFrame]:
        """Get raw dataframe for analysis"""
        if ticker not in self.data:
            return None
        
        raw_data = self.data[ticker]
        df = pd.DataFrame(raw_data)
        df = self.clean_data(df)
        df = self.calculate_returns(df)
        df = self.calculate_moving_averages(df)
        
        return df.tail(days)
