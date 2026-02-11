from analyzer.fetch import (
    get_tip_height,
    get_block_hash,
    get_block_txids,
    get_transaction
)

def main():
    print("Mempool layer check")

    tip = get_tip_height()
    print(tip)

    test_height = tip - 3

    block_hash = get_block_hash(test_height)
    print(block_hash)

    txids = get_block_txids(block_hash)
    print(txids)

    first_txid = txids[0]
    print(first_txid)

    tx = get_transaction(first_txid)

    print( tx.get('fee'))
    print({len(tx.get('vin', []))})
    print({len(tx.get('vout', []))})

    if tx["vout"]:
        print({tx['vout'][0].get('scriptpubkey_type')})

if __name__ == "__main__":
    main()

