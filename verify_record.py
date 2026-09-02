"""Given a tx hash from main.py's output, confirm the on-chain record matches."""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))

from pipeline.anchor import record_hash  # noqa: E402
from pipeline.exceptions import PipelineError  # noqa: E402
from pipeline.proof import read_record  # noqa: E402

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")

RECORD_FIELDS = (
    "source_image_sha256",
    "match_url",
    "platform",
    "similarity_score",
    "model",
    "search_engine",
    "timestamp_utc",
)


def verify(tx_hash: str) -> bool:
    path = os.path.join(OUTPUT_DIR, f"{tx_hash}.json")
    if not os.path.exists(path):
        raise FileNotFoundError(f"no saved record for tx {tx_hash} at {path}")

    with open(path) as f:
        saved = json.load(f)

    record = {field: saved[field] for field in RECORD_FIELDS}
    local_hash = record_hash(record)
    print(f"recomputed local hash: {local_hash.hex()}")

    onchain = read_record(local_hash)
    print(f"on-chain record: {onchain}")

    onchain_hash = onchain["recordHash"].removeprefix("0x")
    if onchain_hash == "00" * 32:
        print("MISMATCH: nothing stored on-chain under this hash")
        return False
    if onchain_hash != local_hash.hex():
        print("MISMATCH: on-chain hash does not match the recomputed local hash")
        return False

    print("MATCH: on-chain record matches the local record")
    return True


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tx", required=True, help="transaction hash from main.py's output")
    args = parser.parse_args()

    try:
        ok = verify(args.tx)
    except PipelineError as exc:
        print(f"verification failed: {exc}", file=sys.stderr)
        sys.exit(1)

    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
