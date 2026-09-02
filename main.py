"""Run the full face-id + blockchain verification pipeline against one image."""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))

from pipeline.anchor import anchor_record, build_record, record_hash  # noqa: E402
from pipeline.detect import detect_and_encode  # noqa: E402
from pipeline.exceptions import PipelineError  # noqa: E402
from pipeline.search import reverse_search  # noqa: E402
from pipeline.verify import verify_candidates  # noqa: E402

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")


def run(image_path: str) -> dict:
    encoding = detect_and_encode(image_path)
    print(f"detected face: confidence={encoding.confidence:.3f} bbox={encoding.bbox}")

    candidates = reverse_search(image_path)
    print(f"reverse search: {len(candidates)} social-media candidate(s)")

    match = verify_candidates(image_path, candidates)
    print(
        f"verified match: {match.candidate.url} "
        f"(platform={match.candidate.platform}, distance={match.similarity_score:.4f})"
    )

    record = build_record(image_path, match)
    tx_hash = anchor_record(record)
    print(f"anchored on-chain: tx {tx_hash}")
    print(f"view proof: https://amoy.polygonscan.com/tx/{tx_hash}")

    output = {**record, "record_hash": record_hash(record).hex(), "tx_hash": tx_hash}
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    out_path = os.path.join(OUTPUT_DIR, f"{tx_hash}.json")
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2)
    print(f"saved record to {out_path}")

    return output


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--image", required=True, help="path to the input photo")
    args = parser.parse_args()

    try:
        run(args.image)
    except PipelineError as exc:
        print(f"pipeline failed: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
