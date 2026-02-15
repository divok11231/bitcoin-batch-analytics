import numpy as np


SCRIPT_ENUM = {
    "p2pkh": 0,
    "v0_p2wpkh": 1,
    "v0_p2wsh": 2,
    "v1_p2tr": 3,
}

DEFAULT_SCRIPT_TYPE = 4


def map_script_type(script_str: str) -> int:
    return SCRIPT_ENUM.get(script_str, DEFAULT_SCRIPT_TYPE)



def txid_to_uint64(txid: str) -> int:
    if not txid:
        return 0
    return int(txid[:16], 16)



def encode_block(transactions: list, block_index: int) -> dict:

    fees = []
    input_counts = []
    output_counts = []
    script_types = []
    block_ids = []

    out_hash = []
    out_index = []
    out_value = []

    in_hash = []
    in_index = []

    for tx in transactions:

        txid = tx.get("txid", "")
        tx_hash64 = txid_to_uint64(txid)

        fee = tx.get("fee", 0)
        vin = tx.get("vin", [])
        vout = tx.get("vout", [])

        fees.append(fee)
        input_counts.append(len(vin))
        output_counts.append(len(vout))
        block_ids.append(block_index)

        if vout:
            script_str = vout[0].get("scriptpubkey_type", "")
            script_types.append(map_script_type(script_str))
        else:
            script_types.append(DEFAULT_SCRIPT_TYPE)

        for idx, out in enumerate(vout):
            out_hash.append(tx_hash64)
            out_index.append(idx)
            out_value.append(out.get("value", 0))

        for inp in vin:
            prev_txid = inp.get("txid")
            prev_vout = inp.get("vout")

            if prev_txid is not None and prev_vout is not None:
                in_hash.append(txid_to_uint64(prev_txid))
                in_index.append(prev_vout)

    return {
        "fees": fees,
        "input_counts": input_counts,
        "output_counts": output_counts,
        "script_types": script_types,
        "block_ids": block_ids,

        "out_hash": out_hash,
        "out_index": out_index,
        "out_value": out_value,
        "in_hash": in_hash,
        "in_index": in_index,
    }



def global_buffer() -> dict:
    return {
        "fees": [],
        "input_counts": [],
        "output_counts": [],
        "script_types": [],
        "block_ids": [],

        "out_hash": [],
        "out_index": [],
        "out_value": [],
        "in_hash": [],
        "in_index": [],
    }


def extend_global_buffer(global_buffer: dict, encoded_block: dict):
    for key in global_buffer:
        global_buffer[key].extend(encoded_block[key])



def numpy_array(global_buffer: dict) -> dict:
    return {
        "fees": np.array(global_buffer["fees"], dtype=np.int64),
        "input_counts": np.array(global_buffer["input_counts"], dtype=np.int32),
        "output_counts": np.array(global_buffer["output_counts"], dtype=np.int32),
        "script_types": np.array(global_buffer["script_types"], dtype=np.int8),
        "block_ids": np.array(global_buffer["block_ids"], dtype=np.int32),

        "out_hash": np.array(global_buffer["out_hash"], dtype=np.uint64),
        "out_index": np.array(global_buffer["out_index"], dtype=np.uint32),
        "out_value": np.array(global_buffer["out_value"], dtype=np.uint64),
        "in_hash": np.array(global_buffer["in_hash"], dtype=np.uint64),
        "in_index": np.array(global_buffer["in_index"], dtype=np.uint32),
    }

