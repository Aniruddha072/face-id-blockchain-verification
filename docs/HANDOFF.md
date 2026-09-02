# Handoff

Last updated: 2026-09-02

## Where things stand

Day 0 (Foundations) is mostly done. Day 1-5 haven't started.

**Done:**
- Public repo created: https://github.com/Aniruddha072/face-id-blockchain-verification
- Scaffold committed and pushed: README, LICENSE (MIT), .gitignore, requirements.txt,
  .env.example, contracts/FaceRecord.sol (reference contract from the spec)
- Python 3.13 venv created, all pipeline dependencies installed and import-tested
  (deepface, opencv-python, retina-face, requests, web3, python-dotenv)
- Pipeline code structure designed and individually confirmed (see decisions.md):
  package layout under src/pipeline/, typed exceptions, retry only on network
  calls, two separate CLI entrypoints (main.py / verify_record.py), argparse

**Not done (needs manual signup / wallet setup, can't be scripted):**
- SerpApi account + key
- Alchemy account + Polygon Amoy app + RPC URL
- Brand-new burner MetaMask wallet, funded from the Amoy testnet faucet
- Pick 1-2 consenting test subjects with a public social presence
- Fill in .env from .env.example once the above exist

## Pending sign-off

The pipeline code structure design (docs/decisions.md, the four entries dated
2026-09-02) was presented in full and the sub-decisions were confirmed one at
a time, but the final "does this look right overall" confirmation on the
complete write-up was still outstanding when this doc was last updated -
confirm that before writing any src/pipeline/ code.

## Next concrete step

Once the design sign-off above lands: start Day 1 (face detection + encoding)
- write src/pipeline/detect.py per the confirmed layout.
