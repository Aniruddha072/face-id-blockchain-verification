# Handoff

Last updated: 2026-09-02

## Where things stand

Day 0 (Foundations) is mostly done. Days 1-4 are code-complete: the whole
pipeline (detect, search/verify, anchor, main.py, verify_record.py) is
written. Day 5 (record + submit) hasn't started, and nothing has actually
run end to end yet.

**Done:**
- Public repo created: https://github.com/Aniruddha072/face-id-blockchain-verification
- Scaffold committed and pushed: README, LICENSE (MIT), .gitignore, requirements.txt
  (pinned), .env.example, contracts/FaceRecord.sol
- Python 3.13 venv created, all pipeline dependencies installed and import-tested
  (deepface, opencv-python, retina-face, tf-keras, requests, web3, python-dotenv, py-solc-x)
- Pipeline code structure designed and confirmed (see decisions.md)
- src/pipeline/exceptions.py, config.py, retry.py: typed errors (including
  ConfigError so a missing .env value is caught cleanly), .env loading,
  retry-with-backoff for network calls
- src/pipeline/detect.py: detect_and_encode(), verified offline
- src/pipeline/search.py: reverse_search() via SerpApi's image-upload flow,
  filtered to social domains, verified offline; live call unverified (d0-3)
- src/pipeline/verify.py: verify_candidates(), downloads + DeepFace.verify()
  per candidate, unverified against real data (d0-3, d0-6)
- src/pipeline/contract.py: compiles contracts/FaceRecord.sol via py-solc-x,
  actually verified (4-entry ABI, real bytecode), shared by deploy/anchor/proof
- deploy.py: deploys the contract programmatically via web3.py (see
  decisions.md for why this replaces the spec's Remix suggestion); unverified,
  pending d0-4 and d0-5
- src/pipeline/anchor.py: build_record() and record_hash() verified offline
  (deterministic, sensitive to record changes); anchor_record() (storeRecord()
  call) unverified, pending d0-4 and d0-5
- src/pipeline/proof.py: read_record() (getRecord() call) unverified, same
  blockers
- main.py: chains detect -> search -> verify -> anchor, saves
  output/<tx_hash>.json; verify_record.py: reloads a saved record, recomputes
  its hash, confirms against the on-chain value. Both verified only at the
  --help / argument-parsing level and for the missing-record error path;
  running either end to end is unverified, same blockers as above
- README rewritten: project layout, setup, configuration, how to run,
  known limitations, all filled in. "Example output" and the demo recording
  link are still open, they need an actual run
- Fixed issue #1 (tf-keras missing for retinaface on tensorflow 2.21), issue
  #2 (config.require() exception type), issue #3 (stray drafting links and
  branding in this file and decisions.md, including a git history rewrite)
- Build-log tracker page (source at docs/build-log.html, hosted separately
  from this repo; DONE set now covers d0-1, d0-2, d1-1, d1-2, d1-4, d2-1..d2-4,
  d3-1, d3-3, d3-4, d4-1..d4-5, 17/56 overall)

**Not done (needs manual signup / wallet setup, can't be scripted):**
- SerpApi account + key (d0-3) - blocks every live API call below
- Alchemy account + Polygon Amoy app + RPC URL (d0-4) - blocks deploy.py, anchor.py, proof.py
- Brand-new burner MetaMask wallet, funded from the Amoy testnet faucet (d0-5) - same blockers as d0-4
- Pick 1-2 consenting test subjects with a public social presence (d0-6) - blocks real-photo testing
- Fill in .env from .env.example once the above exist

## Blocked

Every stage is code-complete but only exercised with offline logic checks,
synthetic data, and (for the contract) a real compile. Nothing has run
against a live SerpApi key, a real photo, or the actual chain yet. All of
that is one `.env` away: fill it in once d0-3 through d0-6 land, run
`python deploy.py` to get CONTRACT_ADDRESS, then `python main.py --image
<path>` for a real end-to-end run.

## Next concrete step

Once `.env` is complete: run the pipeline end to end against a real photo,
fix whatever breaks (file issues for real bugs found, per the usual
pattern), then Day 5: clone into a clean folder and follow the README
exactly, record one unedited take, link the recording, final push, submit
before Sep 7 11:59 PM IST.
