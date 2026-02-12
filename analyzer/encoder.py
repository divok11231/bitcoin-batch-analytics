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
