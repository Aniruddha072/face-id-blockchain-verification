# Handoff

Last updated: 2026-09-02

## Where things stand

Day 0 (Foundations) is mostly done. Days 1-3 (detect, search/verify, anchor)
are code-complete. Day 4-5 haven't started.

**Done:**
- Public repo created: https://github.com/Aniruddha072/face-id-blockchain-verification
- Scaffold committed and pushed: README, LICENSE (MIT), .gitignore, requirements.txt,
  .env.example, contracts/FaceRecord.sol
- Python 3.13 venv created, all pipeline dependencies installed and import-tested
  (deepface, opencv-python, retina-face, tf-keras, requests, web3, python-dotenv, py-solc-x)
- Pipeline code structure designed and confirmed (see decisions.md)
- src/pipeline/exceptions.py, config.py, retry.py: typed errors, .env loading,
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
- Fixed issue #1 (tf-keras missing for retinaface on tensorflow 2.21)
- Build-log tracker page (source at docs/build-log.html, hosted separately
  from this repo; DONE set now has d0-1, d0-2, d1-1, d1-2, d1-4, d2-1..d2-4,
  d3-1, d3-3, d3-4, 12/56 overall)

**Not done (needs manual signup / wallet setup, can't be scripted):**
- SerpApi account + key (d0-3) - blocks live search.py/verify.py
- Alchemy account + Polygon Amoy app + RPC URL (d0-4) - blocks deploy.py, anchor.py, proof.py
- Brand-new burner MetaMask wallet, funded from the Amoy testnet faucet (d0-5) - same blockers as d0-4
- Pick 1-2 consenting test subjects with a public social presence (d0-6) - blocks real-photo testing
- Fill in .env from .env.example once the above exist

## Blocked

Everything code-complete so far has only been exercised with offline logic
checks, synthetic data, and (for the contract) a real compile. Nothing has
run against a live SerpApi key, a real photo, or the actual chain yet. All
of that is one `.env` away, once d0-3 through d0-6 land: fill .env, run
`python deploy.py` to get CONTRACT_ADDRESS, then the pipeline stages become
testable end to end.

## Next concrete step

Day 4: write verify_record.py (read-back proof CLI), wire main.py as the
single `python main.py --image photo.jpg` entrypoint chaining
detect -> search -> verify -> anchor and writing output/<tx_hash>.json,
add error handling at the top level (catch PipelineError once), fill in the
README's remaining TODO sections. None of this needs external credentials to
write; running it end to end still does.
