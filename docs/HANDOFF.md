# Handoff

Last updated: 2026-10-10

## Where things stand

Resumed weeks later to finish this as a resume piece. Hackathon framing is
gone from the README and from the build-log artifact (redesigned as a
status page, not a sprint tracker). The project has a live, free,
read-only on-chain proof viewer (`docs/index.html`, hosted on GitHub
Pages) with its own client-side record-verification tool, ensemble face
verification with the model-agreement count anchored on-chain, and a
real, reproducible accuracy benchmark: 92% TPR, 2% FPR on 100 LFW pairs,
with both error cases manually checked against the actual photos. See
decisions.md for the reasoning behind all of this. Two things left: the
demo GIF, and a full security review the user asked for once everything
else is done.

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
- Fixed issues #1-#7 (see repo issue tracker), all surfaced by real runs
- Clean-clone test passed: fresh clone, fresh venv, README's setup steps
  followed exactly, full pipeline ran successfully unmodified
- Build-log tracker page (source at docs/build-log.html, hosted separately
  from this repo) updated to match throughout
- Hackathon framing removed from README (task banner, "brief" wording)
- Repo topics expanded (blockchain, smart-contracts, python added)
- `docs/index.html`: static, read-only on-chain proof viewer, live on
  GitHub Pages at https://aniruddha072.github.io/face-id-blockchain-verification/,
  repo homepage URL set to it. Looks up a record hash and calls
  `getRecord()` on the verified contract directly from the browser
  (ethers.js v6 via CDN)
- Ensemble verification: every candidate checked against ArcFace,
  Facenet512, and VGG-Face, needs 2-of-3 agreement to count as verified.
  Real run confirmed it end to end (3 candidates found, all 2/3 agreement)
- Contract redeployed to carry the agreement count on-chain:
  `0x98D363d1b816FAc6a034bE3237fA20bcCbbC2c99` (replaces
  `0x80637a622EF860a85c3510b77eb832F356ed08DD`, see decisions.md for why),
  source verified on PolygonScan (Exact Match), Read Contract tab working.
  `anchor.py`, `proof.py`, `verify_record.py`, `docs/index.html` all
  updated to the new ABI and address
- Fresh real example run against the new contract (tx
  dbc22bcddc97a65d7f3b4feb5de166fd090318616921866bbbf153a3acbcd336),
  round-tripped through `verify_record.py` to confirm the on-chain record
  matches. README's "Example output" and the proof viewer's example hash
  both updated to this real data
- Build-log artifact (docs/build-log.html) redesigned from a day-by-day
  sprint checklist into a status page: real anchored record shown as
  proof, ensemble explanation, tech stack, limitations. Reuses the proof
  viewer's exact color/type tokens so the two live pages read as one site
- Proof viewer redesigned: opens with the real anchored record already
  loaded (used to be an empty form), result shown as a ledger card with a
  model-agreement dot indicator, copy buttons on hashes, favicon, Open
  Graph/Twitter meta tags for a real link-preview card
- Found and fixed a stray attribution trailer that had slipped into a
  pushed commit (`a10a521`), despite the long-standing no-AI-traces rule
  for this repo. Amended and force-pushed since it was the branch tip with
  nothing on top of it; full history swept afterward and confirmed clean.
  See decisions.md for how it happened
- Client-side record verification added to the proof viewer: upload a
  photo and a saved `output/<tx>.json`, recomputes the hash in-browser
  byte-identical to Python's `json.dumps`, checks it against the chain.
  Verified against real data with both positive and negative (tampered
  JSON, wrong photo) test cases
- Stopped using personal/ambiguous-consent photos for testing (every real
  anchored match so far was confirmed by the user to not actually be
  them). Live reverse-search testing now uses real consenting family
  members with genuine public presence, going forward
- `benchmark_ensemble.py` added: measures the ensemble against LFW's
  labeled pairs (scikit-learn's `fetch_lfw_pairs`), entirely offline,
  known ground truth. Found and fixed a real reproducibility bug in the
  sampling (random.sample doesn't nest across sample sizes the way
  shuffle-then-slice does) while scaling from an initial 30-pair pilot up
  to 100 pairs. Final result: 92% true positive rate (46/50), 2% false
  positive rate (1/49, one skipped for failed detection). Both error
  cases manually inspected against the real photos (saved locally to
  `lfw_benchmark_images/`, gitignored): the false positive is two
  genuinely similar-looking different men, the hardest false negative is
  the same woman at a very different angle/lighting/age, neither is a
  data error. Documented in the README with the exact command to
  reproduce it, including the honest caveat that these three models were
  historically tuned against LFW by their own authors, so strong LFW
  performance doesn't fully transfer as evidence for the pipeline's
  actual harder real-world photos
- Full security review: covered the pipeline, both entrypoints, the
  smart contract, both static pages, and secrets handling. Specifically
  checked and ruled out XSS in the proof viewer (confirmed untrusted data
  only ever goes through `.textContent`), an overwrite risk in
  `storeRecord()`'s permissionless write (not targetable due to SHA-256
  preimage resistance), and path traversal via CLI arguments (not
  applicable, this is a local trusted-input CLI tool). Zero findings
  cleared the confidence bar, nothing filed as an issue. See decisions.md

**Not done:**
- Demo GIF: ScreenToGif is installed, a test recording was done weeks ago,
  official recording still pending (user wants it done last)

## Next concrete step

Demo GIF (the user's own screen recording), then a final commit and push.
That's the last item on the project.
