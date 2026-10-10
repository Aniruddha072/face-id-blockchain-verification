"""Measure the ensemble's real accuracy against LFW's labeled same/different pairs.

Offline only: no reverse-image search, no blockchain, no API calls. Downloads
a small public, academically-standard benchmark (scikit-learn's bundled LFW
pairs) and runs it through the exact same model ensemble verify_candidates()
uses, to get real true-positive/false-positive numbers instead of guessing.
"""

import argparse
import random
import sys

sys.path.insert(0, "src")

sys.stdout.reconfigure(encoding="utf-8")

from pipeline.verify import AGREEMENT_NEEDED, ENSEMBLE_MODELS, ensemble_vote  # noqa: E402


def to_image(arr):
    """LFW arrays are float32 in [0, 1]; DeepFace expects uint8 in [0, 255]."""
    return (arr * 255).astype("uint8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--per-class", type=int, default=15, help="pairs to sample per class (same/different)")
    parser.add_argument("--subset", default="test", choices=["train", "test", "10_folds"])
    parser.add_argument("--seed", type=int, default=0)
    args = parser.parse_args()

    from sklearn.datasets import fetch_lfw_pairs

    print(f"loading LFW pairs ({args.subset} subset)...")
    data = fetch_lfw_pairs(subset=args.subset, resize=1.0, color=True)

    rng = random.Random(args.seed)
    same_idx = [i for i, t in enumerate(data.target) if data.target_names[t] == "Same person"]
    diff_idx = [i for i, t in enumerate(data.target) if data.target_names[t] == "Different persons"]
    # Shuffle once, then slice. This keeps a smaller --per-class run's pairs as a
    # guaranteed prefix of any larger run with the same seed, so increasing the
    # sample size extends previous results instead of silently replacing them.
    rng.shuffle(same_idx)
    rng.shuffle(diff_idx)
    sample_idx = same_idx[: min(args.per_class, len(same_idx))] + \
        diff_idx[: min(args.per_class, len(diff_idx))]

    print(f"testing {len(sample_idx)} pairs ({args.per_class} same-person, {args.per_class} different-person)")
    print(f"ensemble: {ENSEMBLE_MODELS}, majority needed: {AGREEMENT_NEEDED}\n")

    results = []
    skipped = 0
    for n, i in enumerate(sample_idx, 1):
        img1 = to_image(data.pairs[i][0])
        img2 = to_image(data.pairs[i][1])
        is_same = data.target_names[data.target[i]] == "Same person"

        try:
            agreed, total, primary_distance = ensemble_vote(img1, img2)
        except Exception as exc:
            skipped += 1
            print(f"[{n}/{len(sample_idx)}] skipped (detection failed): {exc}")
            continue

        ensemble_verified = agreed >= AGREEMENT_NEEDED
        results.append(
            {
                "is_same": is_same,
                "ensemble_verified": ensemble_verified,
                "agreed": agreed,
                "total": total,
                "primary_distance": primary_distance,
            }
        )
        label = "same" if is_same else "diff"
        outcome = "verified" if ensemble_verified else "rejected"
        print(f"[{n}/{len(sample_idx)}] {label:4s} -> {outcome:8s} ({agreed}/{total} agreed, distance={primary_distance:.4f})")

    report(results, skipped)


def report(results: list[dict], skipped: int) -> None:
    same = [r for r in results if r["is_same"]]
    diff = [r for r in results if not r["is_same"]]

    tpr = sum(r["ensemble_verified"] for r in same) / len(same) if same else 0.0
    fpr = sum(r["ensemble_verified"] for r in diff) / len(diff) if diff else 0.0

    print("\n--- ensemble accuracy ---")
    print(f"true positive rate:  {tpr:.1%}  ({sum(r['ensemble_verified'] for r in same)}/{len(same)} genuine matches correctly verified)")
    print(f"false positive rate: {fpr:.1%}  ({sum(r['ensemble_verified'] for r in diff)}/{len(diff)} different people incorrectly verified)")
    if skipped:
        print(f"skipped (face not detected): {skipped}")

    print("\n--- model agreement distribution ---")
    for label, group in (("same-person pairs", same), ("different-person pairs", diff)):
        if not group:
            continue
        counts = {}
        for r in group:
            counts[r["agreed"]] = counts.get(r["agreed"], 0) + 1
        dist = ", ".join(f"{k}/{group[0]['total']}={v}" for k, v in sorted(counts.items()))
        print(f"{label}: {dist}")


if __name__ == "__main__":
    main()
