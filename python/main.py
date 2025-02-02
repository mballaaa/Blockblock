import asyncio
import json
import websockets
import jwt
import time
from quixstreams import Application
import logging

# WebSocket server URL (replace with your Geth node's address)
GETH_WS_URL = "ws://localhost:8546"


app = Application(
    broker_address="localhost:9092", 
    loglevel="DEBUG",
)

async def subscribe_to_new_heads():
    async with websockets.connect(GETH_WS_URL) as websocket:
        logging.info("Connected to Geth WebSocket server")

        # Subscribe to new block headers
        subscription_request = {
            "jsonrpc": "2.0",  # Add JSON-RPC version
            "id": 1,           # Unique ID for the request
            "method": "eth_subscribe",
            "params": ["newHeads"]
        }
        await websocket.send(json.dumps(subscription_request))
        logging.info("Subscribed to new block headers")

        # Listen for incoming messages
        with app.get_producer() as producer:
            async for message in websocket:
                data = json.loads(message)
                # print("Received data:", data)
                producer.produce(
                    topic="new_blocks", 
                    key="block", 
                    value=json.dumps(data)
                )
                logging.info("Sent new block to Kafka")



async def main():
    await subscribe_to_new_heads()

# Run the WebSocket client
asyncio.run(main())