#!/usr/bin/env python3
import argparse
import json
from dataclasses import dataclass
from typing import Dict, Any
import math


@dataclass
class EncryptionModel:
    key: str
    name: str
    layer: str
    confidentiality: float    # 0–1
    integrity: float          # 0–1
    compute_cost: float       # 0–1 (higher = more expensive)
    description: str


MODELS: Dict[str, EncryptionModel] = {
    "aztec-enc": EncryptionModel(
        key="aztec-enc",
        name="Aztec Layered zk Encryption",
        layer="zk circuits",
        confidentiality=0.92,
        integrity=0.85,
        compute_cost=0.40,
        description="Zero-knowledge encrypted state with selective disclosure.",
    ),
    "zama-fhe": EncryptionModel(
        key="zama-fhe",
        name="Zama Fully Homomorphic Encryption",
        layer="fhe compute",
        confidentiality=0.97,
        integrity=0.88,
        compute_cost=0.76,
        description="FHE evaluation enabling encrypted compute across all operations.",
    ),
    "soundness-vm": EncryptionModel(
        key="soundness-vm",
        name="Soundness-Driven Verified VM",
        layer="verified semantics",
        confidentiality=0.55,
        integrity=0.99,
        compute_cost=0.32,
        description="Formally verified execution environment with high correctness focus.",
    ),
}


def calc_curve(conf: float, integ: float, cost: float, load: int, pressure: float) -> float:
    """
    Combined crypto reliability curve using:
    - confidentiality
    - integrity
    - compute cost
    - load (TPS)
    - pressure (network volatility factor)
    """
    crypto_strength = 0.50 * conf + 0.50 * integ
    load_penalty = math.exp(-load / 8000)
    cost_penalty = 1 - cost * 0.35
    volatile_penalty = math.exp(-pressure * 1.2)

    final = crypto_strength * load_penalty * cost_penalty * volatile_penalty
    return max(0.0, min(final, 1.0))


def compute_model(
    model: EncryptionModel,
    load: int,
    pressure: float,
    enhance_zk: bool,
    enhance_fhe: bool,
    enhance_formal: bool,
) -> Dict[str, Any]:

    conf = model.confidentiality
    integ = model.integrity
    cost = model.compute_cost

    if enhance_zk:
        conf += 0.05
        integ += 0.03
        cost += 0.02

    if enhance_fhe:
        conf += 0.04
        integ += 0.04
        cost += 0.09

    if enhance_formal:
        integ += 0.06
        cost += 0.01

    conf = min(conf, 1.0)
    integ = min(integ, 1.0)
    cost = min(cost, 1.0)

    score = calc_curve(conf, integ, cost, load, pressure)

    return {
        "model": model.key,
        "name": model.name,
        "layer": model.layer,
        "description": model.description,
        "load": load,
        "pressure": pressure,
        "enhancedZk": enhance_zk,
        "enhancedFhe": enhance_fhe,
        "enhancedFormal": enhance_formal,
        "finalScore": round(score, 4),
    }


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Compute cryptographic reliability score for Web3 encryption models."
    )
    p.add_argument("--model", choices=list(MODELS.keys()), default="aztec-enc")
    p.add_argument("--load", type=int, default=3000, help="Transaction load (TPS).")
    p.add_argument("--pressure", type=float, default=0.3, help="Network volatility factor (0–1).")
    p.add_argument("--enh-zk", action="store_true", help="Enable additional zk enhancements.")
    p.add_argument("--enh-fhe", action="store_true", help="Enable FHE enhancements.")
    p.add_argument("--enh-formal", action="store_true", help="Enable formal verification enhancements.")
    p.add_argument("--json", action="store_true")
    return p.parse_args()


def print_human(d: Dict[str, Any]):
    print("🔐 Web3 Encryption Reliability Model")
    print(f"Model       : {d['name']} ({d['model']})")
    print(f"Layer       : {d['layer']}")
    print(f"Description : {d['description']}")
    print("")
    print("Parameters:")
    print(f"  Load (TPS)          : {d['load']}")
    print(f"  Network pressure    : {d['pressure']}")
    print(f"  Enhanced ZK         : {d['enhancedZk']}")
    print(f"  Enhanced FHE        : {d['enhancedFhe']}")
    print(f"  Enhanced Formal     : {d['enhancedFormal']}")
    print("")
    print(f"Final Score: {d['finalScore']:.4f}")


def main():
    args = parse_args()
    model = MODELS[args.model]

    result = compute_model(
        model,
        load=args.load,
        pressure=args.pressure,
        enhance_zk=args.enh_zk,
        enhance_fhe=args.enh_fhe,
        enhance_formal=args.enh_formal,
    )

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print_human(result)


if __name__ == "__main__":
    main()
