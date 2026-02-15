# Bitcoin Batch Analytics CLI

GPU-accelerated Bitcoin blockchain analytics tool. Analyze transaction fees, input/output statistics, and UTXOs for multiple blocks efficiently using CPU and/or GPU.

---

## Overview

**Bitcoin Batch Analytics** is a command-line tool designed for high-performance batch analysis of Bitcoin blockchain data. It leverages GPU acceleration (via PyCUDA) to compute heavy operations like UTXO construction and transaction fee aggregation.  



### Why it’s useful:

- It's not. The process is currently network bound and 95%< of the time is spent on retrieving the data. However it does allow you to....
- Quickly analyze thousands of transactions across multiple blocks.
- Compare CPU vs GPU performance for blockchain analytics.
---

## Features

- **Parallel block fetching**.
- **GPU UTXO builder**.
- **CPU fallback**.
- **CLI tool**.

---

## Installation

### Using pip

```bash
conda create -n btc-gpu python=3.10 -y
conda activate btc-gpu

pip install git+https://github.com/yourusername/bitcoin-batch-analytics.git

