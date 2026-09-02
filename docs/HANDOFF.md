# Handoff

Last updated: 2026-09-02

## Where things stand

Day 0 (Foundations) is mostly done. Day 1 (detect/encode) is code-complete.
Day 2 (reverse search + verification) is code-complete. Day 3-5 haven't
started.

**Done:**
- Public repo created: https://github.com/Aniruddha072/face-id-blockchain-verification
- Scaffold committed and pushed: README, LICENSE (MIT), .gitignore, requirements.txt,
  .env.example, contracts/FaceRecord.sol (reference contract from the spec)
- Python 3.13 venv created, all pipeline dependencies installed and import-tested
  (deepface, opencv-python, retina-face, tf-keras, requests, web3, python-dotenv)
- Pipeline code structure designed and confirmed (see decisions.md)
- src/pipeline/exceptions.py, config.py, retry.py: typed errors, .env loading
  with a clear require() check, and a retry-with-backoff helper for network
  calls
- src/pipeline/detect.py: detect_and_encode(), verified offline (import,
  no-face path against a synthetic image)
- src/pipeline/search.py: reverse_search(), uploads the source image via
  SerpApi's Image API (image_id flow, no separate image host, see
  decisions.md) then runs a Google Lens search, filtered to social domains.
  Verified offline (domain filter, oversized-image guard); live API call
  unverified, pending a SerpApi key (d0-3)
- src/pipeline/verify.py: verify_candidates(), downloads each candidate and
  runs DeepFace.verify() against the source, keeps the best genuine match.
  Unverified against real data, pending d0-3 and real sample photos (d0-6)
- Fixed issue #1 (tf-keras missing for retinaface on tensorflow 2.21)
- Build-log tracker page (hosted separately from this repo)
  (source at docs/build-log.html, edit + republish to the same URL; DONE set
  now has d0-1, d0-2, d1-1, d1-2, d1-4, d2-1, d2-2, d2-3, d2-4, 9/56 overall)

**Not done (needs manual signup / wallet setup, can't be scripted):**
- SerpApi account + key (d0-3) — blocks live-testing search.py and verify.py
- Alchemy account + Polygon Amoy app + RPC URL (d0-4) — blocks Day 3
- Brand-new burner MetaMask wallet, funded from the Amoy testnet faucet (d0-5) — blocks Day 3
- Pick 1-2 consenting test subjects with a public social presence (d0-6) — blocks
  real-photo testing across Day 1 and Day 2
- Fill in .env from .env.example once the above exist

## Blocked

Everything code-complete so far (detect, search, verify) has only been
exercised with offline logic checks and synthetic data; none of it has run
against a real photo or a live SerpApi key yet. d1-3 and the equivalent
live checks for Day 2 stay open until d0-3 and d0-6 land.

## Next concrete step

Day 3 (blockchain anchoring): build the match record JSON and
anchor.py (build_record / anchor_record via web3.py), deploy
contracts/FaceRecord.sol to Polygon Amoy via Remix. Deployment and any live
web3 calls need d0-4 (Alchemy RPC) and d0-5 (funded burner wallet) first;
the record-building and hashing logic doesn't.
