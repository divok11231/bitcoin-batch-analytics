import numpy as np


def compute_cpu_stats(arrays: dict) -> dict:
    fees = arrays["fees"]
    input_counts = arrays["input_counts"]
    output_counts = arrays["output_counts"]
    script_types = arrays["script_types"]
    block_ids = arrays["block_ids"]

    stats = {}

    stats["total_fee"] = int(np.sum(fees))
    stats["avg_fee"] = float(np.mean(fees))
    stats["min_fee"] = int(np.min(fees))
    stats["max_fee"] = int(np.max(fees))

    stats["total_inputs"] = int(np.sum(input_counts))
    stats["total_outputs"] = int(np.sum(output_counts))

    stats["avg_inputs_per_tx"] = float(np.mean(input_counts))
    stats["avg_outputs_per_tx"] = float(np.mean(output_counts))

    stats["script_histogram"] = np.bincount(script_types, minlength=5)

    stats["block_fee_totals"] = np.bincount(block_ids, weights=fees)

    return stats

