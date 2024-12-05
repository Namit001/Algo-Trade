from sqlalchemy import Column, Integer, Float, String, DateTime, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime ,timezone

Base = declarative_base()

# Models for an algorithmic trading application. 
# `MarketData` stores raw price data.
# `Signals` contains indicators and actions derived from strategies like MACD and Supertrend.

# Table for storing Raw Market Data.
class MarketData(Base):
    __tablename__ = "market_data"
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.now(timezone.utc))
    price = Column(Float)

# Table for storing Signals and Indicators Data.
class Signals(Base):
    __tablename__ = "signals"
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.now(timezone.utc))
    signal_type = Column(String)  # "BUY" or "SELL"
    price = Column(Float)
    macd_line = Column(Float)
    signal_line = Column(Float)
    macd_histogram = Column(Float)
    supertrend = Column(Float)
    unrealised_gain_loss = Column(Float)   # Tracks unrealized PnL to monitor open trade performance.
    cumulative_pnl = Column(Float)

DATABASE_URL = "postgresql+psycopg2://postgres:1234@database:5432/algo_trade"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)
