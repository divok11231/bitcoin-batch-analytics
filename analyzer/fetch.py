import requests

BASE_URL = "https://mempool.space/api"

def get_tip_height():
    r = requests.get(f"{BASE_URL}/blocks/tip/height")
    r.raise_for_status()
    height = r.json()
    return height


def get_block_hash(height):

    r = requests.get(f"{BASE_URL}/block-height/{height}")
    block_hash = r.text.strip()


    return block_hash


def fetch_block_transactions(height):

    block_hash = get_block_hash(height)


    r = requests.get(f"{BASE_URL}/block/{block_hash}/txs")
    transactions = r.json()


    return transactions

