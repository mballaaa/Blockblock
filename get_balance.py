# get the balance of an ethereum address given the address as an argument

import json
import logging
import sys
import websockets

from web3 import Web3

w3 = Web3(Web3.HTTPProvider("http://localhost:8545"))

async def get_balance(address):
    balance = w3.eth.get_balance(address)
    return balance

async def main():
    logging.basicConfig(level=logging.ERROR)
    address = sys.argv[1]
    balance = await get_balance(address)
    print(balance)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
