import argparse
import time

from analyzer.fetch import get_tip_height, fetch_block_transactions
from analyzer.encode import global_buffer, encode_block, extend_global_buffer, numpy_array
from analyzer.cpu_stats import compute_cpu_stats
from analyzer.gpu_stats import gpu_sum


def main(start_height=None, num_blocks=2, use_gpu=False):

    if start_height is None:
        tip = get_tip_height()
        start_height = tip - num_blocks

    buffers = global_buffer()
    all_transactions = []

    for block_index, height in enumerate(range(start_height, start_height + num_blocks)):

        txs = fetch_block_transactions(height)
        all_transactions.extend(txs)

        encoded = encode_block(txs, block_index)
        extend_global_buffer(buffers, encoded)

    arrays = numpy_array(buffers)

    print("CPU")
    cpu_start = time.time()
    stats = compute_cpu_stats(arrays)
    cpu_time = time.time() - cpu_start

    print(f"CPU total_fee: {stats['total_fee']}")
    print(f"CPU time: {cpu_time:.4f}s")

    if use_gpu:
        print("GPU")
        gpu_total, kernel_time = gpu_sum(arrays["fees"])

        print(f"GPU total_fee: {gpu_total}")
        print(f"Kernel time: {kernel_time:.4f}s")
        print(f"Match: {gpu_total == stats['total_fee']}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", type=int, default=None)
    parser.add_argument("--blocks", type=int, default=2)
    parser.add_argument("--gpu", action="store_true")

    args = parser.parse_args()

    main(args.start, args.blocks, args.gpu)
