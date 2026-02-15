import requests
import time

BASE_URL = "https://mempool.space/api"


def get_tip_height():
    print("[FETCH] tip height...")
    t0 = time.time()

    try:
        r = requests.get(
            f"{BASE_URL}/blocks/tip/height",
            timeout=10
        )
        r.raise_for_status()
        height = int(r.text.strip())

        print(f"[FETCH] Tip height: {height}")
        print(f"[FETCH]  {time.time() - t0:.2f}s")
        return height

    except requests.exceptions.Timeout:
        print("[FETCH]timed out")
        raise

    except requests.exceptions.RequestException as e:
        print(f"[FETCH]failed: {e}")
        raise


def get_block_hash(height):
    print(f"[FETCH] Getting block hash for {height}...")

    r = requests.get(
        f"{BASE_URL}/block-height/{height}",
        timeout=10
    )
    r.raise_for_status()

    block_hash = r.text.strip()
    print(f"[FETCH] Block hash: {block_hash}")
    return block_hash


def fetch_block_transactions(height):
    print(f"[FETCH]transactions for block {height}")

    block_hash = get_block_hash(height)

    r = requests.get(
        f"{BASE_URL}/block/{block_hash}/txs",
        timeout=30
    )
    r.raise_for_status()

    transactions = r.json()

    print(f"[FETCH] Retrieved {len(transactions)} transactions")
    return transactions

