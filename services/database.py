from app.models import SessionLocal, MarketData, Signals
import pandas as pd
from datetime import datetime, timezone

# This module provides utility functions for interacting with the database:
# - Saving raw market data (`save_market_data`).
# - Fetching recent market data for analysis (`fetch_recent_data`).
# - Saving processed trading signals and indicators (`save_signals`).

# Save the latest market price with its timestamp to the database.
def save_market_data(price):
    timestamp = datetime.now(timezone.utc) 
    print(f"Saving price: {price} at {timestamp}")
    session = SessionLocal()
    market_data = MarketData(price=price, timestamp=timestamp) # Creates a new market data instance.
    session.add(market_data)
    session.commit()

# Fetch recent market data for processing and analysis as a Pandas DataFrame.
def fetch_recent_data():
    session = SessionLocal()
    return pd.read_sql(session.query(MarketData).statement, session.bind)

# Persist processed signals and indicators into the database for tracking and visualization.
def save_signals(data):
    session = SessionLocal()
    try:
        if not data.empty:
            latest_row = data.iloc[-1]
            
            signal = Signals(
                timestamp=latest_row['timestamp'],
                signal_type=latest_row['signals'],
                price=float(latest_row['price']),
                macd_line=float(latest_row['macd_line']),
                signal_line = float(latest_row['signal_line']),
                macd_histogram = float(latest_row['macd_histogram']),
                supertrend = float(latest_row['supertrend']),
                unrealised_gain_loss = float(latest_row['unrealised_gain_loss']),
                cumulative_pnl = float(latest_row['cumulative_pnl'])
            )
            
            session.add(signal)
            session.commit()
            print(f"Saved signal: {signal.signal_type} at {signal.price}")
        else:
            print("No data to save.")
    except Exception as e:
        session.rollback()
        # Rollback changes to ensure database consistency.
        print(f"Error saving signal: {e}")
    finally:
        session.close()

