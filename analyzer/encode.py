import numpy as np

SCRIPT_ENUM = {
    "p2pkh": 0,
    "v0_p2wpkh": 1,
    "v0_p2wsh": 2,
    "v1_p2tr": 3,
}

# Setting default type to invalid

DEFAULT_SCRIPT_TYPE = 4


def map_script_type(script_str: str) -> int:
    return SCRIPT_ENUM.get(script_str, DEFAULT_SCRIPT_TYPE)


def encode_block(transactions:list,block_index: int) -> dict:
    fees = []
    input_counts = []
    output_counts = []
    script_types = []
    block_ids = []

    for tx in transactions:
        
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

    return {
        "fees": fees,
        "input_counts": input_counts,
        "output_counts": output_counts,
        "script_types": script_types,
        "block_ids": block_ids,
    }

def global_buffer() -> dict:
        return {
        "fees": [],
        "input_counts": [],
        "output_counts": [],
        "script_types": [],
        "block_ids": [],
    }

def extend_global_buffer(global_buffer:dict, encode_block:dict):
    for key in global_buffer:
        global_buffer[key].extend(encode_block[key])

def numpy_array(global_buffer: dict) -> dict:
    return {
        "fees": np.array(global_buffer["fees"], dtype=np.int64),
        "input_counts": np.array(global_buffer["input_counts"], dtype=np.int32),
        "output_counts": np.array(global_buffer["output_counts"], dtype=np.int32),
        "script_types": np.array(global_buffer["script_types"], dtype=np.int8),
        "block_ids": np.array(global_buffer["block_ids"], dtype=np.int32),
    }
