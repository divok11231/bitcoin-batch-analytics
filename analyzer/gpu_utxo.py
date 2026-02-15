import numpy as np
import pycuda.autoinit
import pycuda.driver as cuda
from pycuda.compiler import SourceModule
import time


KERNEL_CODE = """
extern "C"
__global__ void mark_and_reduce(
    unsigned long long *out_hash,
    unsigned int *out_index,
    unsigned long long *out_value,
    unsigned long long *in_hash,
    unsigned int *in_index,
    unsigned char *spent,
    unsigned long long *result,
    int out_n,
    int in_n)
{
    int idx = blockIdx.x * blockDim.x + threadIdx.x;

    if (idx >= out_n)
        return;

    unsigned long long oh = out_hash[idx];
    unsigned int oi = out_index[idx];

    // Check if spent
    for (int j = 0; j < in_n; j++) {
        if (oh == in_hash[j] && oi == in_index[j]) {
            spent[idx] = 1;
            break;
        }
    }

    // If not spent, add to total
    if (spent[idx] == 0) {
        atomicAdd(result, out_value[idx]);
    }
}
"""


MODULE = SourceModule(KERNEL_CODE)
KERNEL = MODULE.get_function("mark_and_reduce")


def gpu_build_utxo(arrays):


    t0 = time.time()

    out_hash = arrays["out_hash"].astype(np.uint64)
    out_index = arrays["out_index"].astype(np.uint32)
    out_value = arrays["out_value"].astype(np.uint64)
    in_hash = arrays["in_hash"].astype(np.uint64)
    in_index = arrays["in_index"].astype(np.uint32)

    out_n = np.int32(len(out_hash))
    in_n = np.int32(len(in_hash))

    print(f" Outputs: {out_n}")
    print(f" Inputs:  {in_n}")

    d_out_hash = cuda.mem_alloc(out_hash.nbytes)
    d_out_index = cuda.mem_alloc(out_index.nbytes)
    d_out_value = cuda.mem_alloc(out_value.nbytes)
    d_in_hash = cuda.mem_alloc(in_hash.nbytes)
    d_in_index = cuda.mem_alloc(in_index.nbytes)

    spent = np.zeros(out_n, dtype=np.uint8)
    d_spent = cuda.mem_alloc(spent.nbytes)

    result = np.zeros(1, dtype=np.uint64)
    d_result = cuda.mem_alloc(result.nbytes)

    cuda.memcpy_htod(d_out_hash, out_hash)
    cuda.memcpy_htod(d_out_index, out_index)
    cuda.memcpy_htod(d_out_value, out_value)
    cuda.memcpy_htod(d_in_hash, in_hash)
    cuda.memcpy_htod(d_in_index, in_index)
    cuda.memcpy_htod(d_spent, spent)
    cuda.memcpy_htod(d_result, result)

    block = 256
    grid = int((out_n + block - 1) / block)


    t_kernel = time.time()

    KERNEL(
        d_out_hash,
        d_out_index,
        d_out_value,
        d_in_hash,
        d_in_index,
        d_spent,
        d_result,
        out_n,
        in_n,
        block=(block, 1, 1),
        grid=(grid, 1),
    )

    cuda.Context.synchronize()

    kernel_time = time.time() - t_kernel

    cuda.memcpy_dtoh(result, d_result)
    cuda.memcpy_dtoh(spent, d_spent)

    total_time = time.time() - t0

    live_utxo_count = int(np.sum(spent == 0))


    return {
        "utxo_total_value": int(result[0]),
        "utxo_count": live_utxo_count,
        "kernel_time": kernel_time,
        "total_time": total_time,
    }

