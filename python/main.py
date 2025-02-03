import asyncio
import json
import websockets
import jwt
import time
from quixstreams import Application
import logging
from web3 import Web3

w3 = Web3(Web3.HTTPProvider("http://localhost:8545"))

# WebSocket server URL (replace with your Geth node's address)
GETH_WS_URL = "ws://localhost:8546"
GETH_BROKER_ADDRESS = "localhost:9092"


app = Application(
    broker_address=GETH_BROKER_ADDRESS, 
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
                print("Received data:", data)
                producer.produce(
                    topic="new_blocks", 
                    key="block", 
                    value=json.dumps(data)
                )
                if "params" in data and "result" in data["params"]:
                    await request_block_data(data["params"]["result"]["hash"])
                logging.info("Sent new block to Kafka")

async def request_block_data(block_hash):
    get_block_request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "eth_getBlockByHash",
        "params": [block_hash, True]
    }
    async with websockets.connect(GETH_WS_URL) as websocket:
        logging.info("Connected to Geth WebSocket server")
        await websocket.send(json.dumps(get_block_request))
        logging.info("Sent getBlock request")
        async for message in websocket:
            data = json.loads(message)
            print("Received data:", w3.to_json(data))
            break


async def main():
    logging.basicConfig(level=logging.ERROR)

    await subscribe_to_new_heads()
    logging.info("WebSocket client started")


# Run the WebSocket client
asyncio.run(main())