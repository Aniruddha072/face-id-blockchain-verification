# Handoff

Last updated: 2026-09-10

## Where things stand

The hackathon submission window closed (Sep 7, 11:59 PM IST) without a
submission. The pipeline works end to end, and the setup steps in the
README were just confirmed to actually work from a clean clone. Two of
the three portfolio-credibility additions (see decisions.md, 2026-09-10
entry) are done: multi-candidate output and PolygonScan contract
verification. The VHS demo and README's example output are what's left.

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
- Fixed issues #1-#7 (see repo issue tracker), all surfaced by real runs
- Clean-clone test passed: fresh clone, fresh venv, README's setup steps
  followed exactly, full pipeline ran successfully unmodified
- Build-log tracker page (source at docs/build-log.html, hosted separately
  from this repo) updated to match, reframed as a portfolio project rather
  than a hackathon countdown
- verify_candidates() now returns the top 3 verified matches ranked by
  distance instead of one forced best guess; only the best still gets
  anchored on-chain. Confirmed live: 3 real candidates found and ranked,
  best one anchored (tx c1bbec42a8fd7116631c4775dfbbaca03cb58e3a02681ba1807fe8548d6cbccb)
- contracts/FaceRecord.sol verified on PolygonScan (Exact Match), Read
  Contract tab confirmed working, getRecord() callable with no wallet

**Not done:**
- VHS demo: script a .tape file, render a GIF, embed it in the README
- README's "Example output" section needs a real run's output dropped in,
  now that the multi-candidate output has landed so it reflects the real
  shape
- Link the verified contract and demo GIF from the README once both exist

## Next concrete step

Set up the VHS demo (.tape script, render, embed in README), then do the
final README pass: real example output, verified-contract link, demo GIF.
