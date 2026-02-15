import time


def cpu_build_utxo(transactions):

    print(" UTXO build")

    t0 = time.time()

    utxo = {}
    spent = set()

    for tx in transactions:

        txid = tx["txid"]

        for idx, out in enumerate(tx.get("vout", [])):
            utxo[(txid, idx)] = out.get("value", 0)

        for vin in tx.get("vin", []):
            prev_txid = vin.get("txid")
            prev_vout = vin.get("vout")

            if prev_txid is not None:
                spent.add((prev_txid, prev_vout))

    for key in spent:
        utxo.pop(key, None)

    total_value = sum(utxo.values())

    total_time = time.time() - t0

    print(f" Total value_cpu: {total_value}")
    print(f"Time_cpu: {total_time:.4f}s")

    return total_value, total_time

