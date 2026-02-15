def build_utxo_map(transactions):

    utxo = {}
    spent = set()

    for tx in transactions:

        txid = tx["txid"]

        # outputs
        for idx, out in enumerate(tx.get("vout", [])):
            utxo[(txid, idx)] = out.get("value", 0)

        # inputs
        for vin in tx.get("vin", []):
            prev_txid = vin.get("txid")
            prev_vout = vin.get("vout")

            if prev_txid is not None:
                spent.add((prev_txid, prev_vout))

    # remove spent outputs
    for key in spent:
        utxo.pop(key, None)

    return utxo


