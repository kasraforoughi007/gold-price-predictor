'''
Gold Price Forecasting
-----------------------
Downloads gold price data from yfinance site , trains a Prophet time series model ,
forecasts the gold price from 2025-2026 , and store the results in a postgreSQL database .


Author: [Kasra Foroughi]
Date: 2025-10--21
'''



import logging
import pandas as pd
import yfinance as yf
from prophet import Prophet
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import requests_cache
import requests


requests_cache.install_cache('yfinance_cache', expire_after=3600)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)


API_KEY = "6XPCMGDLKCQANVWN"
def get_data(start = "2023-01-01",
             end = "2025-01-01",
             symbol= "XAUUSD") :
    """
        Downloads gold price data from Alphacantage.
        Args:
            symbol: Ticker symbol for the asset (default: XAUUSD).
            start: Start date for data collection.
            end: End date for data collection.

        Returns:
            A pandas dataframe with columns ['ds' , 'y'] for Prophet .
        """

    try:
        url  = "https://www.alphavantage.co/query"
        params = {
            "function": "TIME_SERIES_DAILY",
            "symbol": symbol,
            "apikey": API_KEY,
            "outputsize": "full"
        }
        r = requests.get(url, params=params)
        data = r.json().get('Time Series (Daily)', {})
        if not data:
            logger.warning(f"No data returned for {symbol}. Response: {r.text[:200]}")
            return None
        logger.info(f"Trying to download data for {symbol}")
        df = pd.DataFrame(data).T.reset_index()
        df = df.rename(columns={"index": "ds" , "4. close" : "y"})[["ds" ,"y"]]
        df["ds"] = pd.to_datetime(df["ds"])
        df["y"] = df["y"].astype(float)
        df = df[(df["ds"] >= start) & (df["ds"] <= end)]
        return df
    except Exception as e:
        logger.warning(f"AlphaVantage failed: {e}")


def make_forecast(df: pd.DataFrame,periods: int = 365) -> pd.DataFrame:
    """
    generating Prophet model and forecasts using Prophet ...
    Args:
        df: DataFrame containing columns ['ds', 'y'].
        periods: Number of days to forecast ahead.

    Returns:
        Forecast DataFrame from Prophet.
    """
    if df is None or df.empty:
        raise ValueError("DataFrame is empty. cannot fit model.")

    m =Prophet(
        yearly_seasonality=True ,
        weekly_seasonality=True ,
        daily_seasonality=False
               )
    m.add_seasonality(name='monthly' , period=30.5 , fourier_order=5)

    logger.info("Training Prophet model ...")
    m.fit(df)

    future = m.make_future_dataframe(periods=365)
    forecast = m.predict(future)
    logger.info("forecasting has been completed for %s days." , periods)

    return forecast
def send_to_database(forecast: pd.DataFrame,
                     table_name: str= "gold_db") -> None:
    """
    Save forecast data to postgreSQL database.


    Args:
        forecast: Forecast DataFrame.
        table_name: Target table name in PostgreSQL.
    """

    engine = create_engine('postgresql+psycopg2://postgres:postgres@postgres-db:5432/gold_db')
    try:
        forecast.to_sql(table_name , engine, if_exists='replace' , index=False)
        logger.info("Forecast successfully saved to database table '%s'.", table_name)
    except Exception as e:
        logger.error("Database write failed: %s", e)


if __name__ == "__main__":
    logger.info("Starting gold price forecast pipeline...")

    df = get_data()
    if df is None :
        raise SystemExit("Data retrieval failed. Exiting.")
    full_forecast = make_forecast(df)
    send_to_database(full_forecast)

    logger.info("Pipeline completed successfully.")




