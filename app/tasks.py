from celery import Celery
from services.strategy import apply_strategy
from services.database import fetch_recent_data, save_signals

celery = Celery('tasks', broker="redis://redis:6379/0", backend="redis://redis:6379/0")

@celery.task
def process_market_data():
    print("Data fetch starting.....")
    data = fetch_recent_data()
    processed_data = apply_strategy(data)
    save_signals(processed_data)
    print(f"Signals processed and saved!")



    