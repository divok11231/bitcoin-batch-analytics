import numpy as np
import pycuda.autoinit
import pycuda.driver as cuda
from pycuda.compiler import SourceModule
import time


KERNEL_CODE = """
__global__ void sum_kernel(unsigned long long *data,unsigned long long *result, int n)
{
    __shared__ unsigned long long sdata[256];

    int tid = threadIdx.x;
    int i = blockIdx.x * blockDim.x + threadIdx.x;

    sdata[tid] = (i < n) ? data[i] : 0;
    __syncthreads();

    for (int s = blockDim.x/2; s > 0; s >>= 1)
    {
        if (tid < s)
            sdata[tid] += sdata[tid + s];
        __syncthreads();
    }

    if (tid == 0)
        atomicAdd(result, sdata[0]);
}
"""

def gpu_sum(arr):

    arr = arr.astype(np.uint64)

    n = np.int32(len(arr))

    arr_gpu = cuda.mem_alloc(arr.nbytes)
    result_gpu = cuda.mem_alloc(8)

    cuda.memcpy_htod(arr_gpu, arr)

    cuda.memcpy_htod(result_gpu, np.zeros(1, dtype=np.uint64))

    mod = SourceModule(KERNEL_CODE)
    kernel = mod.get_function("sum_kernel")

    block = 256
    grid = int((len(arr) + block - 1) / block)

    start = time.time()

    kernel(
        arr_gpu,
        result_gpu,
        n,
        block=(block, 1, 1),
        grid=(grid, 1),
    )

    cuda.Context.synchronize()
    kernel_time = time.time() - start

    result = np.zeros(1, dtype=np.uint64)
    cuda.memcpy_dtoh(result, result_gpu)

    return int(result[0]), kernel_time

