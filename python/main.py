import requests
from quixstreams import Application
import json
import logging
import time
from web3 import Web3


w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

if not w3.is_connected():
    logging.error("Web3 is not connected")
else:
    logging.info("Web3 is connected")

def get_block():
    response = w3.eth.get_block('latest')

    block = Web3.to_json(response)
    return block

def main():
    app = Application(
        broker_address="localhost:9092", 
        loglevel="DEBUG",
        )

    with app.get_producer() as producer:
        while True:
            block = get_block()
            logging.debug("Got block data: %s", block)
            producer.produce(
                topic="block",
                key="temperature",
                value=json.dumps(block)
            )
            logging.debug("Produced block data to Kafka")
            logging.debug("Sleeping for 10 seconds")
            time.sleep(10)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    main()