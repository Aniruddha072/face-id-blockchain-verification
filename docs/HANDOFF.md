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
with both error cases manually checked against the actual photos. The
full codebase has been reviewed for security issues with nothing filed,
and both the proof viewer and the status artifact were redesigned around
a photographic-proof-sheet visual identity instead of generic dark-SaaS
defaults. See decisions.md for the reasoning behind all of this. The
project is considered complete; the demo GIF was deliberately skipped
(see decisions.md).

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
- Proof viewer and status artifact redesigned around a photographic-proof-
  sheet visual identity: register-mark corner ticks on content frames, a
  film-sprocket perforation strip as the one deliberate flourish, a warm
  darkroom palette where the two accent colors carry real meaning (signal
  red for actions, developer green reserved for verified/passed states
  only), frame numbers only on the pipeline's actual sequence, and mono
  type reserved for real data instead of UI labels. Tested live in a
  browser, not just opened as a file: on-chain lookup, vote-dot agreement
  indicator, copy buttons, and the verify-your-own-record flow all still
  work, no JS logic was touched. The status artifact also picked up the
  LFW accuracy numbers and the security review result. See decisions.md
- Demo GIF skipped by decision, not an oversight: the live proof viewer
  link already lets anyone see and use the real thing with zero setup,
  which is what a GIF exists to fake. See decisions.md
- 15-slide walkthrough deck added at `docs/presentation.html`, served live
  by GitHub Pages and linked from the README. Built with the frontend-slides
  skill, using a custom style that extends the proof viewer's and status
  artifact's existing visual system instead of one of the skill's stock
  presets, so all three live pages read as one brand. Covers the pipeline,
  the real anchored record, measured accuracy, the security review, and
  the consent/ethics stance, all real project data. See decisions.md for
  a layout bug caught and fixed before shipping
- Visual identity replaced on the proof viewer and the deck: the
  darkroom/proof-sheet look (safelight glow, film grain, register-mark
  frames) is gone, replaced by Ethereal Glass (OLED black, violet/emerald
  orbs, double-bezel glass cards, a floating island nav with a hamburger
  menu on the proof viewer) per a third-party `high-end-visual-design`
  skill the user installed and explicitly asked to apply, full replace,
  not a blend. All existing JS/functionality retested and unchanged. The
  status artifact was left as-is and is now visually out of sync with
  these two pages; flagged, not fixed, since it wasn't in scope. See
  decisions.md for the conflict this skill's own rules created and how
  it was resolved
- Final security audit, stricter than the first one: found and fixed a
  real secret-leak path. Both the SerpApi key and the Alchemy RPC key
  could print in plaintext whenever their network call failed (confirmed
  by actually reproducing the failures, not just reading code). Fixed
  with one `config.redact()` helper applied everywhere an exception
  becomes a printed message, across `search.py`, `anchor.py`, `proof.py`,
  and `deploy.py`, plus a `SearchError` class so search failures are
  actually caught instead of crashing raw. Also fixed: no Subresource
  Integrity on the proof viewer's ethers.js script, and the client-side
  verify checklist built its rows with `innerHTML` instead of
  `textContent` (traced and confirmed not currently exploitable, hardened
  anyway). A second, stricter pass after the fixes found nothing further.
  Issues #8, #9, #10. See decisions.md for how each was verified

## Next concrete step

None. The project is complete.
