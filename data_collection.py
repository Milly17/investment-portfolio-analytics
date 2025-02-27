"""
Data Collection Module for Investment Portfolio Analytics.

This module provides functions to fetch financial data from various sources:
- Yahoo Finance for asset prices and returns
- FRED for economic indicators
- World Bank for global economic data
- Fama-French for risk factor data

The module handles API connections, error handling, and data storage.
"""

import os
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Union, Optional, Tuple

import pandas as pd
import numpy as np
import yfinance as yf
from fredapi import Fred
import wbdata
import pandas_datareader.data as web

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


class DataCollector:
    """Class to collect and manage financial data from multiple sources."""

    def __init__(
        self,
        start_date: str = "2010-01-01",
        end_date: Optional[str] = None,
        data_dir: str = "data/raw",
    ):
        """
        Initialize the DataCollector.

        Parameters
        ----------
        start_date : str
            Start date for historical data in 'YYYY-MM-DD' format.
        end_date : str, optional
            End date for historical data in 'YYYY-MM-DD' format.
            If None, current date is used.
        data_dir : str
            Directory to store raw data files.
        """
        self.start_date = start_date
        self.end_date = end_date if end_date else datetime.now().strftime("%Y-%m-%d")
        self.data_dir = data_dir

        # Ensure data directory exists
        os.makedirs(self.data_dir, exist_ok=True)

        # Initialize API keys (would typically come from environment variables)
        self.fred_api_key = os.environ.get("FRED_API_KEY", "")
        
        logger.info(
            f"Initialized DataCollector from {self.start_date} to {self.end_date}"
        )

    def get_stock_data(
        self, tickers: List[str], interval: str = "1d", include_dividends: bool = True
    ) -> pd.DataFrame:
        """
        Fetch stock price data from Yahoo Finance.

        Parameters
        ----------
        tickers : List[str]
            List of ticker symbols to fetch.
        interval : str
            Data interval: '1d', '1wk', '1mo', etc.
        include_dividends : bool
            Whether to include dividend data.

        Returns
        -------
        pd.DataFrame
            DataFrame with stock price data.
        """
        logger.info(f"Fetching stock data for {len(tickers)} tickers")
        
        try:
            # Download data for all tickers at once
            df = yf.download(
                tickers,
                start=self.start_date,
                end=self.end_date,
                interval=interval,
                group_by="ticker",
                auto_adjust=True,
                actions=include_dividends,
            )

            # If only one ticker is requested, fix the column structure
            if len(tickers) == 1:
                ticker = tickers[0]
                df.columns = pd.MultiIndex.from_product([[ticker], df.columns])
            
            # Save raw data
            output_path = os.path.join(self.data_dir, "stock_prices.parquet")
            df.to_parquet(output_path)
            logger.info(f"Saved stock data to {output_path}")
            
            return df
            
        except Exception as e:
            logger.error(f"Error fetching stock data: {str(e)}")
            raise

    def get_economic_indicators(self, indicator_ids: List[str]) -> pd.DataFrame:
        """
        Fetch economic indicators from FRED.

        Parameters
        ----------
        indicator_ids : List[str]
            List of FRED indicator IDs (e.g., 'GDP', 'UNRATE').

        Returns
        -------
        pd.DataFrame
            DataFrame with economic indicators.
        """
        if not self.fred_api_key:
            logger.warning("FRED API key not set. Using limited access.")
        
        logger.info(f"Fetching {len(indicator_ids)} economic indicators from FRED")
        
        try:
            fred = Fred(api_key=self.fred_api_key)
            data_dict = {}
            
            for indicator in indicator_ids:
                logger.info(f"Fetching indicator: {indicator}")
                series = fred.get_series(
                    indicator, 
                    observation_start=self.start_date,
                    observation_end=self.end_date
                )
                data_dict[indicator] = series
            
            # Combine all indicators into a single DataFrame
            df = pd.DataFrame(data_dict)
            
            # Save raw data
            output_path = os.path.join(self.data_dir, "economic_indicators.parquet")
            df.to_parquet(output_path)
            logger.info(f"Saved economic data to {output_path}")
            
            return df
            
        except Exception as e:
            logger.error(f"Error fetching economic indicators: {str(e)}")
            raise

    def get_world_bank_data(self, indicators: Dict[str, str], countries: List[str]) -> pd.DataFrame:
        """
        Fetch global economic data from World Bank.

        Parameters
        ----------
        indicators : Dict[str, str]
            Dictionary of indicator IDs to names.
        countries : List[str]
            List of country codes.

        Returns
        -------
        pd.DataFrame
            DataFrame with World Bank data.
        """
        logger.info(f"Fetching World Bank data for {len(countries)} countries")
        
        try:
            # Convert dates to format expected by wbdata
            start_date = datetime.strptime(self.start_date, "%Y-%m-%d").date()
            end_date = datetime.strptime(self.end_date, "%Y-%m-%d").date()
            
            # Fetch the data
            df = wbdata.get_dataframe(
                indicators, 
                country=countries, 
                data_date=(start_date, end_date)
            )
            
            # Process the dataframe to handle the multi-level index
            df = df.reset_index()
            
            # Save raw data
            output_path = os.path.join(self.data_dir, "world_bank_data.parquet")
            df.to_parquet(output_path)
            logger.info(f"Saved World Bank data to {output_path}")
            
            return df
            
        except Exception as e:
            logger.error(f"Error fetching World Bank data: {str(e)}")
            raise

    def get_fama_french_factors(self, dataset: str = "F-F_Research_Data_Factors") -> pd.DataFrame:
        """
        Fetch Fama-French factor data from Kenneth French's data library.

        Parameters
        ----------
        dataset : str
            Name of the Fama-French dataset to fetch.

        Returns
        -------
        pd.DataFrame
            DataFrame with Fama-French factor data.
        """
        logger.info(f"Fetching Fama-French factors: {dataset}")
        
        try:
            # Fetch data using pandas_datareader
            df = web.DataReader(
                dataset, 
                "famafrench", 
                start=self.start_date, 
                end=self.end_date
            )[0]
            
            # Convert percent values to decimals
            df = df / 100
            
            # Save raw data
            output_path = os.path.join(self.data_dir, "fama_french_factors.parquet")
            df.to_parquet(output_path)
            logger.info(f"Saved Fama-French data to {output_path}")
            
            return df
            
        except Exception as e:
            logger.error(f"Error fetching Fama-French data: {str(e)}")
            raise

    def get_all_data(
        self,
        tickers: List[str],
        economic_indicators: List[str],
        wb_indicators: Dict[str, str],
        countries: List[str],
    ) -> Dict[str, pd.DataFrame]:
        """
        Fetch all required data sets and return as a dictionary.

        Parameters
        ----------
        tickers : List[str]
            List of stock ticker symbols.
        economic_indicators : List[str]
            List of FRED indicator IDs.
        wb_indicators : Dict[str, str]
            Dictionary of World Bank indicator IDs to names.
        countries : List[str]
            List of country codes for World Bank data.

        Returns
        -------
        Dict[str, pd.DataFrame]
            Dictionary of all fetched datasets.
        """
        logger.info("Fetching all data sources")
        
        try:
            # Create a dictionary to store all data
            all_data = {}
            
            # Fetch stock data
            all_data["stocks"] = self.get_stock_data(tickers)
            
            # Fetch economic indicators
            all_data["economic"] = self.get_economic_indicators(economic_indicators)
            
            # Fetch World Bank data
            all_data["world_bank"] = self.get_world_bank_data(wb_indicators, countries)
            
            # Fetch Fama-French factors
            all_data["factors"] = self.get_fama_french_factors()
            
            logger.info("Successfully fetched all data")
            return all_data
            
        except Exception as e:
            logger.error(f"Error fetching all data: {str(e)}")
            raise

# Example usage
if __name__ == "__main__":
    # Define data to fetch
    tickers = ["SPY", "AGG", "VEA", "VWO", "GLD", "VNQ"]
    economic_indicators = ["GDP", "UNRATE", "CPIAUCSL", "FEDFUNDS", "T10Y2Y"]
    wb_indicators = {
        "NY.GDP.MKTP.KD.ZG": "GDP Growth",
        "FP.CPI.TOTL.ZG": "Inflation",
        "NE.TRD.GNFS.ZS": "Trade % GDP",
    }
    countries = ["USA", "CHN", "EUU", "JPN", "GBR"]

    # Create data collector
    collector = DataCollector(start_date="2010-01-01")
    
    # Fetch all data
    data = collector.get_all_data(
        tickers, economic_indicators, wb_indicators, countries
    )
    
    # Print data shapes
    for name, df in data.items():
        print(f"{name} data shape: {df.shape}")