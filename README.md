# web3-encryption-reliability

A minimal CLI tool that calculates a **cryptographic reliability score** for different Web3 encryption layers.  
Models are conceptually inspired by:

- **Aztec-style zk encryption**
- **Zama-style fully homomorphic encryption**
- **Soundness-first verified VMs**

The repository contains only two files:
- `app.py`
- `README.md`


## Overview

The evaluator scores a Web3 encryption architecture based on:

- Confidentiality strength  
- Integrity assurance  
- Compute cost  
- Transaction load (TPS)  
- Network volatility factor  
- Optional enhancement layers:
  - extra zk layering  
  - extra FHE logic  
  - additional formal soundness proofs  

Outputs a final reliabilityScore from 0.0 to 1.0.


## Installation

Requirements:
- Python 3.8+
- No dependencies except the Python standard library.

Clone the repo and keep the two files (`app.py` + this README.md`).


## Usage

Run with defaults (Aztec-style encryption):

python app.py

Simulate Zama FHE model under high load:

python app.py --model zama-fhe --load 12000 --pressure 0.4 --enh-fhe

Simulate a soundness-first verified VM:

python app.py --model soundness-vm --enh-formal --pressure 0.2

Get JSON output for dashboards:

python app.py --model zama-fhe --json


## Example Output

🔐 Web3 Encryption Reliability Model  
Model       : Zama Fully Homomorphic Encryption  
Layer       : fhe compute  
Description : FHE evaluation enabling encrypted compute across all operations.

Parameters:
  Load (TPS)          : 12000  
  Network pressure    : 0.4  
  Enhanced ZK         : False  
  Enhanced FHE        : True  
  Enhanced Formal     : False  

Final Score: 0.3721


## Notes

- This tool is conceptual and not based on real-world performance or cryptographic measurements.  
- It is meant for research, experimentation, and architectural exploration.  
- You can extend it by adding additional encryption models or adjustment factors.
