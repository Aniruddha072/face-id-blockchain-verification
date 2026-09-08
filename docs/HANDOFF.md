# Handoff

Last updated: 2026-09-08

## Where things stand

The hackathon submission window closed (Sep 7, 11:59 PM IST) without a
submission. The pipeline itself works end to end though, and this is worth
finishing as a portfolio piece: real photo, real SerpApi reverse search,
real DeepFace verification, real transaction anchored on Polygon Amoy,
confirmed on PolygonScan. Reframing the remaining work around that instead
of a deadline.

**Done:**
- Public repo created: https://github.com/Aniruddha072/face-id-blockchain-verification
- Scaffold committed and pushed: README, LICENSE (MIT), .gitignore, requirements.txt
  (pinned), .env.example, contracts/FaceRecord.sol
- Python 3.13 venv created, all pipeline dependencies installed and import-tested
- Pipeline code structure designed and confirmed (see decisions.md)
- Full pipeline written and verified live, not just offline: detect,
  search, verify, contract compile, deploy, anchor, proof, main.py,
  verify_record.py
- SerpApi key active, Alchemy Amoy RPC URL working (chain ID 80002
  confirmed), burner wallet funded from the Polygon faucet
- Contract deployed to Amoy: 0x80637a622EF860a85c3510b77eb832F356ed08DD
  (deploy.py, not Remix, see decisions.md)
- Multiple real end-to-end runs against live photos: face detection,
  reverse search, verification, and on-chain anchoring all confirmed
  working against real data, not just synthetic tests
- Fixed issues #1-#7 (see repo issue tracker); #4-#7 only surfaced once the
  pipeline touched a real RPC endpoint, a real console encoding, and a real
  downloaded photo for the first time:
  - web3.py needed POA middleware for Amoy's block headers, and explicit
    gas/gasPrice instead of its default overshoot
  - Windows console encoding was crashing DeepFace's model-download logging
    and getting misreported as "no face detected"
  - DeepFace.verify() was silently falling back to a broken opencv detector
    backend, failing every candidate regardless of whether it matched
- Build-log tracker page (source at docs/build-log.html, hosted separately
  from this repo) updated to match, reframed as a portfolio project rather
  than a hackathon countdown

**Not done:**
- README's "Example output" section needs a real run's output dropped in
- Clean-clone test: verify the README's own setup steps work from scratch
- Demo recording: optional now (no judge to show it to), but worth having
  for a resume/portfolio link if time allows

## Next concrete step

Fill in README's "Example output" with a real run's output (using a
well-indexed source photo so the match is genuinely convincing, not just
technically correct), then do a clean-clone test of the setup steps, then
decide on a demo recording.
