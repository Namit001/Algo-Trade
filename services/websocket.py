import asyncio
import websockets
import json
from services.database import save_market_data 
from app.tasks import process_market_data


# WebSocket Client for Coinbase:
# - Connects to Coinbase WebSocket API to receive live BTC-USD ticker data.
# - Saves received prices to the database.
# - Triggers data processing tasks (e.g., trading strategies).


# WebSocket endpoint for Coinbase
COINBASE_WS_URI = "wss://ws-feed.exchange.coinbase.com"

# The subscription message for BTC price ticker
SUBSCRIBE_MESSAGE = {
    "type": "subscribe",
    "product_ids": ["BTC-USD"],
    "channels": [{"name": "ticker", "product_ids": ["BTC-USD"]}],
}

# Save the received price to the database asynchronously to ensure the main WebSocket loop remains non-blocking.
async def save_data(price):
    print(f"attempting to save data: {price}")
    try:
        await asyncio.to_thread(save_market_data, price) 
        print(f"Saved price to database: {price}")
    except Exception as e:
        print(f"Error saving data to database: {e}")

# Process incoming WebSocket messages: Extract price data and trigger processing if valid
async def handle_message(message):
    try:
        data = json.loads(message)
        if data.get("type") == "ticker" and "price" in data:
            price = float(data["price"])
            await save_data(price)
            print("Applying Startegy!")
            process_market_data.apply_async()
        else:
            print(f"Unhandled message type: {data}")
    except json.JSONDecodeError as e:
        print(f"Error decoding message: {e}")
    except Exception as e:
        print(f"Error handling message: {e}")

# Start the WebSocket client and manage the connection lifecycle.
async def start_websocket():
    try:
        print("Attempting to connect to Coinbase WebSocket...")
        async with websockets.connect(COINBASE_WS_URI) as websocket:
            print("Connected to Coinbase WebSocket")
            await websocket.send(json.dumps(SUBSCRIBE_MESSAGE))
            print("Subscription message sent")

            while True:
                try:
                    message = await websocket.recv()  # Receive messages from the WebSocket
                    print(f"Raw message received: {message}")
                    await asyncio.sleep(30)
                    await handle_message(message) # Process the received message.
                except websockets.ConnectionClosed as e:
                    # Handle unexpected disconnection.
                    print(f"WebSocket connection closed: {e}")
                    break
                except Exception as e:
                    print(f"Error receiving message: {e}")
    except Exception as e:
        # Log errors during connection setup.
        print(f"Error connecting to WebSocket: {e}")

if __name__ == "__main__":
    asyncio.run(start_websocket())

