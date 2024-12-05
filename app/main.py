from services.websocket import start_websocket
import threading
import asyncio
from fastapi import FastAPI

app = FastAPI()

async def main():
    print("websocket started!")
    while True:
        try: 
            await start_websocket()
        except Exception as e:
            print(f"websocket error, reconnectinf: {e}")
            await asyncio.sleep(5)

asyncio.run(main())
