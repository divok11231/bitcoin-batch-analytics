import argparse
import time
from .gpu_utxo import gpu_build_utxo
from .cpu_utxo import cpu_build_utxo
from .fetch import get_tip_height, fetch_blocks_parallel
from .encode import global_buffer, encode_block, extend_global_buffer, numpy_array
from .cpu_stats import compute_cpu_stats
from .gpu_stats import gpu_sum

def main(start_height=None, num_blocks=2, use_gpu=False):

    if start_height is None:
        tip = get_tip_height()
        start_height = tip - num_blocks

    block_data = fetch_blocks_parallel(start_height, num_blocks)

    buffers = global_buffer()
    all_transactions = []

    for block_index, height in enumerate(sorted(block_data.keys())):
        txs = block_data[height]
        all_transactions.extend(txs)

        encoded = encode_block(txs, block_index)
        extend_global_buffer(buffers, encoded)

    arrays = numpy_array(buffers)

    cpu_utxo_total, cpu_utxo_count, cpu_utxo_time = cpu_build_utxo(all_transactions)

    cpu_start = time.time()
    cpu_stats = compute_cpu_stats(arrays)
    cpu_fee_time = time.time() - cpu_start
    print("\n=== Stats ===")
    print(f"Blocks analyzed:      {num_blocks}")
    print(f"Total transactions:   {len(all_transactions)}")

    print("\n=== CPU RESULTS ===")

    print(f"UTXO count:           {cpu_utxo_count}")
    print(f"UTXO total value:     {cpu_utxo_total}")
    print(f"Total fees:           {cpu_stats['total_fee']}")
    print(f"CPU UTXO time:        {cpu_utxo_time:.6f}s")
    print(f"CPU fee compute time: {cpu_fee_time:.6f}s")

    if use_gpu:

        gpu_fee_total, gpu_fee_kernel = gpu_sum(arrays["fees"])
        gpu_utxo_stats = gpu_build_utxo(arrays)

        print("\n=== GPU RESULTS ===")
        print(f"UTXO count:           {gpu_utxo_stats['utxo_count']}")
        print(f"UTXO total value:     {gpu_utxo_stats['utxo_total_value']}")
        print(f"Total fees:           {gpu_fee_total}")
        print(f"GPU fee kernel time:  {gpu_fee_kernel:.6f}s")
        print(f"GPU UTXO kernel time: {gpu_utxo_stats['kernel_time']:.6f}s")

        print("\n=== VALIDATION ===")
        print(f"Fee match:   {gpu_fee_total == cpu_stats['total_fee']}")
        print(f"UTXO match:  {gpu_utxo_stats['utxo_total_value'] == cpu_utxo_total}")

def run():
    import argparse

    parser = argparse.ArgumentParser(description="GPU Based Bitcoin Block Analytics Engine")
    parser.add_argument("--start", type=int, default=None)
    parser.add_argument("--blocks", type=int, default=2)
    parser.add_argument("--gpu", action="store_true")

    args = parser.parse_args()

    main(args.start, args.blocks, args.gpu)


if __name__ == "__main__":
    run()

