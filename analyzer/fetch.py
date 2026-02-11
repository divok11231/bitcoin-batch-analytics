import requests

BASE_URL = "https://mempool.space/api"

def get_tip_height():
    return int(requests.get(f"{BASE_URL}/blocks/tip/height").text)

def get_block_hash(height):
    return requests.get(f"{BASE_URL}/block-height/{height}").text.strip()

def get_block_txids(block_hash):
    return requests.get(f"{BASE_URL}/block/{block_hash}/txids").json()

def get_transaction(txid):
    return requests.get(f"{BASE_URL}/tx/{txid}").json()

