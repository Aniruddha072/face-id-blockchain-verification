# Handoff

Last updated: 2026-09-10

## Where things stand

The hackathon submission window closed (Sep 7, 11:59 PM IST) without a
submission. The pipeline works end to end, and the setup steps in the
README were confirmed to work from a clean clone. All three
portfolio-credibility additions from the 2026-09-10 decisions.md entry are
now done except the demo GIF: multi-candidate output, PolygonScan contract
verification, and a full README pass (real example output, match-
confidence explainer, verified-contract link). VHS didn't work on Windows
(ttyd dies when spawned by vhs.exe, a Windows-specific subprocess issue,
not something worth chasing further), switched to ScreenToGif instead.
Demo recording is scheduled for the next session.

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
  (deploy.py, not Remix, see decisions.md), source verified on PolygonScan
  (Exact Match), Read Contract tab confirmed working with no wallet needed
- Multiple real end-to-end runs against live photos: face detection,
  reverse search, verification, and on-chain anchoring all confirmed
  working against real data, not just synthetic tests
- Fixed issues #1-#7 (see repo issue tracker), all surfaced by real runs
- Clean-clone test passed: fresh clone, fresh venv, README's setup steps
  followed exactly, full pipeline ran successfully unmodified
- verify_candidates() returns the top 3 verified matches ranked by
  distance instead of one forced best guess; only the best still gets
  anchored on-chain. Confirmed live: 3 real candidates found and ranked,
  best one anchored (tx c1bbec42a8fd7116631c4775dfbbaca03cb58e3a02681ba1807fe8548d6cbccb)
- README fully updated: Overview and tech stack table mention the
  multi-candidate ranking, new "Match confidence" section explains the
  design, "Example output" has the real console log from the run above
  plus a PolygonScan link, "Blockchain choice" links the verified contract
- Build-log tracker page (source at docs/build-log.html, hosted separately
  from this repo) updated to match throughout

**Not done:**
- Demo GIF: ScreenToGif is installed, a test recording was done, official
  recording scheduled for the next session
- Embed the demo GIF in the README's "Demo recording" section once it exists
- Final commit and push once the GIF lands

## Next concrete step

Record the real demo with ScreenToGif (pipeline run showing the
multi-candidate output and the on-chain anchor), embed the GIF in the
README, then the project is essentially done.
