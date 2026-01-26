import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Optional, Dict, List

from .models import (
    SummaryStats, StockComparison, ComparisonResponse, 
    VolatilityMetrics, TopStock
)
from .data_processor import DataProcessor

class MetricsCalculator:
    """Calculate financial metrics"""
    
    def calculate_summary_stats(self, ticker: str, processor: DataProcessor) -> Optional[SummaryStats]:
        """Calculate summary statistics for a stock"""
        df = processor.get_raw_dataframe(ticker, 365)
        if df is None or df.empty:
            return None
        
        current_price = df['close'].iloc[-1]
        high_52week = df['high'].max()
        low_52week = df['low'].min()
        ma7 = df['ma7'].iloc[-1]
        ma30 = df['ma30'].iloc[-1]
        daily_return = df['daily_return'].iloc[-1]
        volatility = df['daily_return'].std()
        avg_volume = df['volume'].mean()
        price_range = high_52week - low_52week
        
        return SummaryStats(
            ticker=ticker,
            current_price=round(current_price, 2),
            high_52week=round(high_52week, 2),
            low_52week=round(low_52week, 2),
            moving_avg_7=round(ma7, 2),
            moving_avg_30=round(ma30, 2),
            daily_return=round(daily_return, 2),
            volatility=round(volatility, 2),
            price_range=round(price_range, 2),
            avg_volume=round(avg_volume, 0),
            total_data_points=len(df)
        )
    
    def calculate_volatility(self, ticker: str, days: int, processor: DataProcessor) -> Optional[VolatilityMetrics]:
        """
        Creative Metric: Calculate comprehensive volatility metrics
        """
        df = processor.get_raw_dataframe(ticker, days)
        if df is None or df.empty:
            return None
        
        returns = df['daily_return'].dropna()
        
        # Daily volatility
        daily_vol = returns.std()
        
        # Annualized volatility (252 trading days)
        annual_vol = daily_vol * np.sqrt(252)
        
        # Volatility trend
        first_half_vol = returns[:len(returns)//2].std()
        second_half_vol = returns[len(returns)//2:].std()
        volatility_trend = "Increasing" if second_half_vol > first_half_vol else "Decreasing"
        
        # High volatility days (return > 2 std dev)
        threshold = returns.mean() + (2 * returns.std())
        high_vol_days = len(returns[returns > threshold])
        
        return VolatilityMetrics(
            ticker=ticker,
            daily_volatility=round(daily_vol, 4),
            annualized_volatility=round(annual_vol, 4),
            volatility_trend=volatility_trend,
            high_volatility_days=int(high_vol_days),
            volatility_mean=round(returns.mean(), 4),
            volatility_std=round(returns.std(), 4)
        )
    
    def compare_stocks(self, ticker1: str, ticker2: str, days: int, processor: DataProcessor) -> Optional[ComparisonResponse]:
        """Compare two stocks"""
        df1 = processor.get_raw_dataframe(ticker1, days)
        df2 = processor.get_raw_dataframe(ticker2, days)
        
        if df1 is None or df2 is None or df1.empty or df2.empty:
            return None
        
        # Align dates for correlation
        common_dates = df1['date'].isin(df2['date'])
        df1_aligned = df1[common_dates].reset_index(drop=True)
        df2_aligned = df2[df2['date'].isin(df1_aligned['date'])].reset_index(drop=True)
        
        # Stock 1 metrics
        current_price1 = df1['close'].iloc[-1]
        initial_price1 = df1['close'].iloc[0]
        return1 = ((current_price1 - initial_price1) / initial_price1) * 100
        vol1 = df1['daily_return'].std()
        
        # Stock 2 metrics
        current_price2 = df2['close'].iloc[-1]
        initial_price2 = df2['close'].iloc[0]
        return2 = ((current_price2 - initial_price2) / initial_price2) * 100
        vol2 = df2['daily_return'].std()
        
        # Correlation
        returns1 = df1_aligned['daily_return'].dropna()
        returns2 = df2_aligned['daily_return'].dropna()
        
        if len(returns1) > 0 and len(returns2) > 0:
            correlation = returns1.corr(returns2)
        else:
            correlation = 0.0
        
        return ComparisonResponse(
            stock1=StockComparison(
                ticker=ticker1,
                current_price=round(current_price1, 2),
                return_percent=round(return1, 2),
                volatility=round(vol1, 4),
                highest_price=round(df1['high'].max(), 2),
                lowest_price=round(df1['low'].min(), 2)
            ),
            stock2=StockComparison(
                ticker=ticker2,
                current_price=round(current_price2, 2),
                return_percent=round(return2, 2),
                volatility=round(vol2, 4),
                highest_price=round(df2['high'].max(), 2),
                lowest_price=round(df2['low'].min(), 2)
            ),
            correlation=round(correlation, 4),
            volatility_ratio=round(vol1 / vol2 if vol2 > 0 else 0, 4),
            return_difference=round(return1 - return2, 2),
            period_days=days
        )
    
    def get_top_gainers(self, days: int, processor: DataProcessor) -> List[TopStock]:
        """Get top gaining stocks"""
        gainers = []
        
        for company in processor.get_all_companies():
            df = processor.get_raw_dataframe(company.ticker, days)
            if df is not None and not df.empty:
                current_price = df['close'].iloc[-1]
                initial_price = df['close'].iloc[0]
                return_percent = ((current_price - initial_price) / initial_price) * 100
                
                gainers.append(TopStock(
                    ticker=company.ticker,
                    name=company.name,
                    return_percent=round(return_percent, 2),
                    price=round(current_price, 2)
                ))
        
        return sorted(gainers, key=lambda x: x.return_percent, reverse=True)
    
    def get_top_losers(self, days: int, processor: DataProcessor) -> List[TopStock]:
        """Get top losing stocks"""
        losers = []
        
        for company in processor.get_all_companies():
            df = processor.get_raw_dataframe(company.ticker, days)
            if df is not None and not df.empty:
                current_price = df['close'].iloc[-1]
                initial_price = df['close'].iloc[0]
                return_percent = ((current_price - initial_price) / initial_price) * 100
                
                losers.append(TopStock(
                    ticker=company.ticker,
                    name=company.name,
                    return_percent=round(return_percent, 2),
                    price=round(current_price, 2)
                ))
        
        return sorted(losers, key=lambda x: x.return_percent)
