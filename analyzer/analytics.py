import numpy as np


def compute_analytics(arrays, utxo_total, utxo_count):

    fees = arrays["fees"]
    input_counts = arrays["input_counts"]
    output_counts = arrays["output_counts"]
    script_types = arrays["script_types"]

    total_txs = len(fees)
    total_fees = int(np.sum(fees))
    total_inputs = int(np.sum(input_counts))
    total_outputs = int(np.sum(output_counts))

    avg_fee = total_fees / total_txs if total_txs else 0
    avg_inputs = total_inputs / total_txs if total_txs else 0
    avg_outputs = total_outputs / total_txs if total_txs else 0

    script_counts = {}
    for s in np.unique(script_types):
        script_counts[int(s)] = int(np.sum(script_types == s))

    analytics = {
        "total_transactions": total_txs,
        "total_fees": total_fees,
        "total_inputs": total_inputs,
        "total_outputs": total_outputs,
        "avg_fee_per_tx": avg_fee,
        "avg_inputs_per_tx": avg_inputs,
        "avg_outputs_per_tx": avg_outputs,
        "utxo_total_value": utxo_total,
        "utxo_count": utxo_count,
        "avg_utxo_size": utxo_total / utxo_count if utxo_count else 0,
        "script_distribution": script_counts,
    }

    return analytics

