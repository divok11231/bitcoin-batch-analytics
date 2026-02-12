from analyzer.fetch import (
    get_tip_height,
    get_block_hash,
    get_block_txids,
    get_transaction,
)
from analyzer.encode import encode_block_transactions, finalize_numpy_arrays


def main():
    tip = get_tip_height()
    block_hash = get_block_hash(tip - 1)
    txids = get_block_txids(block_hash)

    transactions = []
    for txid in txids[:50]:  # limit to 50 for test
        transactions.append(get_transaction(txid))

    encoded = encode_block_transactions(transactions, block_index=0)
    arrays = finalize_numpy_arrays(encoded)

    print("Array shapes:")
    for k, v in arrays.items():
        print(k, v.shape, v.dtype)


if __name__ == "__main__":
    main()
