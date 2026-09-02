# Handoff

Last updated: 2026-09-02

## Where things stand

Day 0 (Foundations) is mostly done. Day 1 (face detection + encoding) is
in progress. Day 2-5 haven't started.

**Done:**
- Public repo created: https://github.com/Aniruddha072/face-id-blockchain-verification
- Scaffold committed and pushed: README, LICENSE (MIT), .gitignore, requirements.txt,
  .env.example, contracts/FaceRecord.sol (reference contract from the spec)
- Python 3.13 venv created, all pipeline dependencies installed and import-tested
  (deepface, opencv-python, retina-face, tf-keras, requests, web3, python-dotenv)
- Pipeline code structure designed and confirmed (see decisions.md): package
  layout under src/pipeline/, typed exceptions, retry only on network calls,
  two separate CLI entrypoints (main.py / verify_record.py), argparse
- src/pipeline/exceptions.py: PipelineError + the four typed subclasses
- src/pipeline/detect.py: detect_and_encode(), picks the largest face by
  bounding-box area when more than one is present, raises
  NoFaceDetectedError when none is found. Verified: import succeeds, and
  the no-face path raises correctly against a blank synthetic image.
  Detection against a real face is still unverified (see below).
- Fixed issue #1 (tf-keras missing, retinaface needs it on tensorflow 2.21)
- Build-log tracker page (hosted separately from this repo)
  (source lives in the repo at docs/build-log.html, edit it and republish to
  the same URL via the Artifact tool whenever progress changes; DONE set
  currently has d0-1, d0-2, d1-1, d1-2, d1-4 marked complete, 5/56 overall)

**Not done (needs manual signup / wallet setup, can't be scripted):**
- SerpApi account + key
- Alchemy account + Polygon Amoy app + RPC URL
- Brand-new burner MetaMask wallet, funded from the Amoy testnet faucet
- Pick 1-2 consenting test subjects with a public social presence
- Fill in .env from .env.example once the above exist

## Blocked

d1-3 (test detect_and_encode on 3-5 real sample photos) can't proceed until
real photos exist, which depends on d0-6 (picking consenting test subjects).
The zero-face path is verified with a synthetic blank image; the actual
face-detection path (real embeddings, multi-face ranking) is not yet
verified against real photos.

## Next concrete step

Once real sample photos are available: run detect_and_encode() against them
(d1-3), confirm embeddings/bbox/confidence look sane, then move on to Day 2
(reverse search + verification), which needs the SerpApi key from d0-3.
