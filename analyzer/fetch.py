import requests
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE_URL = "https://mempool.space/api"


session = requests.Session()
session.headers.update({
    "User-Agent": "btc-gpu-analytics"
})

adapter = requests.adapters.HTTPAdapter(
    pool_connections=20,
    pool_maxsize=20
)

session.mount("https://", adapter)
session.mount("http://", adapter)



def get_tip_height():
    print("[FETCH] tip height...")
    t0 = time.time()

    r = session.get(
        f"{BASE_URL}/blocks/tip/height",
        timeout=10
    )
    r.raise_for_status()

    height = int(r.text.strip())

    print(f"[FETCH] Tip height: {height}")
    print(f"[FETCH] {time.time() - t0:.2f}s")
    return height



def get_block_hash(height):
    r = session.get(
        f"{BASE_URL}/block-height/{height}",
        timeout=10
    )
    r.raise_for_status()

    return r.text.strip()



def fetch_block_transactions(height):
    print(f"[FETCH] Block {height}")

    t0 = time.time()

    block_hash = get_block_hash(height)

    r = session.get(
        f"{BASE_URL}/block/{block_hash}/txs",
        timeout=30
    )
    r.raise_for_status()

    transactions = r.json()

    print(f"[FETCH] Block {height} → {len(transactions)} txs "
          f"({time.time() - t0:.2f}s)")

    return transactions



def fetch_blocks_parallel(start_height, num_blocks, max_workers=8):

    print(f"[FETCH] Parallel fetching {num_blocks} blocks...")

    heights = list(range(start_height, start_height + num_blocks))
    results = {}

    t0 = time.time()

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_height = {
            executor.submit(fetch_block_transactions, h): h
            for h in heights
        }

        for future in as_completed(future_to_height):
            height = future_to_height[future]
            try:
                results[height] = future.result()
            except Exception as e:
                print(f"[FETCH] Block {height} failed: {e}")

    print(f"[FETCH] Parallel fetch complete "
          f"({time.time() - t0:.2f}s)")

    return results

