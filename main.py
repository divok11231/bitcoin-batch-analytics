import time
from analyzer.fetch import get_tip_height, fetch_block_transactions
from analyzer.encode import (
    encode_block,
    global_buffer,
    extend_global_buffer,
    numpy_array,
)
from analyzer.cpu_stats import compute_cpu_stats

def main(start_height=None, num_blocks=2):


    if start_height is None:
        tip = get_tip_height()
        start_height = tip - num_blocks
        print(f"Latest tip: {tip}")
        print(f"Starting at height: {start_height}\n")

    global_buffers = global_buffer()
    total_tx = 0


    for block_index, height in enumerate(
        range(start_height, start_height + num_blocks)
    ):


        transactions = fetch_block_transactions(height)

        tx_count = len(transactions)
        total_tx += tx_count

        encoded = encode_block(transactions, block_index)
        extend_global_buffer(global_buffers, encoded)


    arrays = numpy_array(global_buffers)
    stats = compute_cpu_stats(arrays)

    print("CPU Stats:")
    for k, v in stats.items():
        print(f"   {k}: {v}")



    for key, arr in arrays.items():
        print(f"   {key}: shape={arr.shape}, dtype={arr.dtype}")



if __name__ == "__main__":
    main()

