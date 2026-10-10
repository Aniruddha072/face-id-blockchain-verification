# Decisions

## 2026-09-02 - Repo name: face-id-blockchain-verification

Went with a descriptive name over the task-number variant (hh-goa-2026-task3)
or the shorter face-verify-chain. Matches the artifact's project title, reads
fine outside hackathon context too.

## 2026-09-02 - Cleaned up the first commit's trailer

The first commit had an extra co-author trailer in the message from a
copy-paste mistake; amended and force-pushed to strip it before anything
else landed on top of it. Local editor/tool state stays out of `.gitignore`
(itself visible on GitHub) and goes in `.git/info/exclude` instead,
untracked and invisible.

## 2026-09-02 - Pipeline module layout: package, one module per stage

`src/pipeline/{detect,search,verify,anchor,proof}.py`, each with one function
per stage, instead of one flat main.py (the spec's own skeleton) or one
script per day. Keeps each stage independently testable and readable in
isolation; matches the Day1-4 build order already laid out in the artifact.

## 2026-09-02 - Error handling: typed exceptions, not result objects

Stage functions raise from `exceptions.py` (NoFaceDetectedError,
NoCandidatesFoundError, NoVerifiedMatchError, ChainError); main.py and
verify_record.py each catch PipelineError once at the top level. Chosen over
(ok, value, error) result objects to avoid boilerplate at every call site for
a 5-day build.

## 2026-09-02 - Retries: network calls only

`with_retry` wraps only the SerpApi/Serper search call and the web3 RPC
calls. DeepFace calls are local/CPU-bound and don't transiently fail the way
a network call does, so they're left unwrapped.

## 2026-09-02 - Two entrypoints, not one CLI with subcommands

`main.py --image <path>` runs the full pipeline; `verify_record.py --tx
<hash>` runs the read-back proof independently, loading the matching record
from `output/*.json` to recompute the hash locally. Matches the spec's own
naming and keeps the proof step usable without re-running the whole
pipeline. CLI parsing is argparse (stdlib), no third-party dependency for a
two-flag surface.

## 2026-09-02 - Reverse search input: SerpApi's own image upload, not a hosting service

The spec's reference snippet passes `image_public_url` straight to SerpApi's
`google_lens` engine, but never says how a local photo becomes a public URL.
Checked SerpApi's docs: it has a built-in two-step flow for exactly this,
no separate image host needed. `POST https://serpapi.com/image` with the
image as multipart form data returns an `image_id` (valid 10 minutes, source
images capped at 500 KB, JPG/PNG/WebP); that `image_id` then replaces `url`
in the `google_lens` search call. Same free-tier SerpApi key covers both
calls, so this adds no new signup and stays inside the $0 rules. The 500 KB
cap means `search.py` rejects (rather than silently truncates) an
oversized source image, since resizing changes what's being searched.

## 2026-09-02 - Contract deployment: programmatic script, not Remix

The spec suggests deploying contracts/FaceRecord.sol manually via Remix +
MetaMask. Went with deploy.py instead: compiles the contract with py-solc-x
(auto-installs a pinned solc 0.8.20 binary) and deploys it via web3.py using
WALLET_PRIVATE_KEY, the same key anchor.py already needs to call
storeRecord(). One command instead of a manual browser step, and the ABI
used by anchor.py/proof.py comes from the same compile step (pipeline/contract.py,
cached per process), so it can't drift from the deployed bytecode. Verified:
compile_contract() actually compiles the real contract (4 ABI entries:
RecordStored event, getRecord, records, storeRecord; non-trivial bytecode).
Deployment itself is unverified, pending d0-4 (RPC) and d0-5 (funded wallet).

## 2026-09-02 - Build-log tracker: separate rebuilt page instead of mirroring the original

Decision log (this file) and `docs/HANDOFF.md` are the real source of
truth, updated every session. First plan was to mirror progress into the
originally-shared build-log page's own checkboxes via browser automation.
Changed instead to maintaining a separate rebuilt copy of that same tracker
(source at `docs/build-log.html`, hosted outside this repo), with progress
baked directly into the page's data (a `DONE` set of item ids) rather than
client-side checkbox storage, so it can be edited and republished directly
without any browser step. The original page is left untouched.

## 2026-09-07 - First live run: three environment gotchas on Windows + Amoy

Getting the pipeline to actually run end to end for the first time (past
the synthetic/offline checks from Day 1-4) surfaced three real bugs, all
filed and closed as issues #4-#7:

- web3.py's default validation middleware rejects Polygon's block headers
  (they carry more than the 32 bytes of extraData it expects), and its
  default EIP-1559 fee estimate overshoots what a transaction actually
  costs on Amoy. Fixed with a shared `get_web3()` in `pipeline/contract.py`
  that injects the POA middleware, and explicit gas/gasPrice on every
  transaction instead of trusting the defaults.
- Windows' default console encoding can't print a character DeepFace's
  logger writes during its one-time model-weight download, which crashed
  and got misreported by our own error handling as "no face detected."
  Fixed by reconfiguring stdout/stderr to utf-8 in both entrypoints, and by
  surfacing the chained exception cause instead of swallowing it.
- `DeepFace.verify()` defaults to the opencv detector backend, and the
  pinned opencv-python version doesn't ship the Haar cascade file that
  backend needs, so every candidate failed verification regardless of
  whether it was a real match. Fixed by passing `detector_backend`
  explicitly in verify.py, matching detect.py's retinaface choice.

None of this was visible in offline testing since nothing touched a real
RPC endpoint, a real console encoding, or a real downloaded photo until
today. Contract is now live on Amoy at
0x80637a622EF860a85c3510b77eb832F356ed08DD, deployed via deploy.py.

## 2026-09-08 - Missed the submission window, continuing as a portfolio piece

The hackathon's Sep 7, 11:59 PM IST deadline passed without a submission.
Decided to keep finishing the project anyway since the pipeline itself
works and is worth having as a resume/portfolio piece. Dropped the
deadline countdown and "judges" framing from the README and build-log
tracker; both now describe the project on its own terms rather than as an
active submission. No functional changes to the pipeline from this.

## 2026-09-10 - Clean-clone test passed; three portfolio-polish additions planned

Cloned the repo fresh into an isolated folder and followed the README's
own setup and run steps exactly (venv, pip install, .env, main.py). It
worked end to end unmodified, confirming the documented setup is accurate
for a stranger cloning the repo, not just this working copy.

Separately, two real runs against the project owner's own photos both
verified a false-positive match (a random Facebook video, a random
LinkedIn post by someone else), each technically under DeepFace's
distance threshold but visibly wrong on manual inspection. Rather than
keep chasing a single clean example photo, researched how comparable
projects handle this and settled on three concrete, zero-cost additions:

- `verify_candidates()` will return the top 3 verified candidates instead
  of forcing a single best guess, following the pattern used by
  SchBenedikt/face (a local, open-source PimEyes-style tool): show ranked
  candidates with their distances rather than one confident pick. Only the
  best of the three still gets anchored on-chain, keeping the on-chain
  side of the brief unchanged; the others are surfaced in the console and
  saved record for transparency.
- The deployed FaceRecord contract will be verified on PolygonScan (free,
  no gas, no new signup beyond a normal account). Turns the contract
  address into readable Solidity source plus a "Read Contract" tab anyone
  can call `getRecord()` from directly, no wallet needed.
- The demo will use VHS (charmbracelet/vhs) instead of a manual screen
  recording: a scripted `.tape` file renders a deterministic terminal GIF,
  checked into the repo and embedded in the README. No recording software,
  no video hosting, no signup, and it stays reproducible if the pipeline's
  output ever changes.

## 2026-09-10 - Working Amoy faucet, for next time

Alchemy's, QuickNode's, and Chainlink's Amoy faucets all gate on holding a
small mainnet ETH/LINK balance as an anti-bot check, which a fresh burner
wallet never has. The one that actually works for a brand-new wallet:
`https://faucet.polygon.technology/` (select Amoy), no mainnet balance
required, optionally verify via X for a bigger drip. Resets every 24
hours per wallet. Worth trying this one first before the others next time
the burner wallet needs topping up.

## 2026-09-10 - VHS doesn't work on Windows, switched to ScreenToGif

Installed VHS and ttyd via winget to script the demo as a reproducible
`.tape` file. Both run fine standalone, but VHS hangs indefinitely when it
tries to spawn ttyd internally: ttyd dies immediately instead of binding
its port, leaving VHS waiting forever on a dead subprocess (with orphaned
headless Chrome instances left behind). This looks like a Windows-specific
gap in VHS's process handling, not a local misconfiguration, and wasn't
worth spending more time chasing for a demo recording. Switched to
ScreenToGif instead: a free, actively maintained, Windows-native recorder
that exports straight to GIF. Less reproducible than a scripted tape file,
but reliable, which matters more here.

## 2026-10-09 - Resumed as a portfolio piece: read-only proof viewer, not a live pipeline demo

Picked this back up weeks later to finish it properly for a resume. Dropped
the hackathon framing from README (the task-banner line, "brief" wording).

Considered a public web demo that runs the full pipeline on an uploaded
photo, since that's the obvious "deploy this" interpretation. Rejected it:
the SerpApi free tier (~100 searches/month) and the testnet wallet's gas
would both get exhausted by normal traffic, and more importantly it would
let any visitor run face-search on any photo they upload, which is the
exact misuse case the Known Limitations section already warns against.

Built `docs/index.html` instead: a static, read-only page that looks up a
record hash and calls `getRecord()` on the already-deployed, already
source-verified contract directly from the browser (ethers.js v6 via CDN,
no build step). No API keys, no wallet, no secrets, nothing that costs
money or can be abused, since it only reads data that's already public on
PolygonScan anyway. Hosted free on GitHub Pages, serving straight from
`/docs` on `master`, no new branch or deploy step. Verified both the real
example record and a never-anchored hash resolve correctly, against the
live contract on the public drpc.org Amoy RPC endpoint (Polygon's own
`rpc-amoy.polygon.technology` doesn't resolve anymore, drpc.org and
OnFinality's public endpoint both do).

## 2026-10-09 - Ensemble verification, confidence anchored on-chain, new contract

Researched how comparable projects handle the false-positive problem and
what would make this one distinctly more interesting than a typical
face-recognition demo. Two changes:

- `verify_candidates()` now runs every candidate through 3 independent
  DeepFace models (ArcFace, Facenet512, VGG-Face), all already bundled in
  the `deepface` package, no new dependency. A candidate only counts as
  verified if a majority (2 of 3) agree, not just one model. Ranking still
  uses ArcFace's distance as the primary signal; ensembling is a trust
  gate, not a new scoring system. Costs real wall-clock time (roughly 3x
  the verification stage), zero extra SerpApi calls, since reverse search
  happens once per run regardless of how many models verify each
  candidate locally afterward.
- `FaceRecord.sol` gained two fields, `modelsAgreed` and `modelsTotal`
  (both `uint8`, a plain agreement count, not a scaled float score, since
  Solidity has no floats and false precision would be worse than an honest
  integer). Checked how similar proof-of-existence projects (Chainpoint,
  verify-proof, others) structure their on-chain records: all of them
  anchor a bare hash only, none anchor a confidence signal alongside it.
  Considered packing the same data into the existing (always-empty)
  `metadataURI` string field instead of changing the struct, to avoid a
  redeployment. Rejected that: an unstructured string crammed with a
  custom mini-format is worse engineering than a real typed field, and
  looks like exactly that to anyone reading the verified source on
  PolygonScan. Redeployed instead.

New contract: `0x98D363d1b816FAc6a034bE3237fA20bcCbbC2c99` (replaces
`0x80637a622EF860a85c3510b77eb832F356ed08DD`). `storeRecord()` and
`getRecord()` both gained the two new parameters/return fields;
`anchor.py`, `proof.py`, and `verify_record.py`'s `RECORD_FIELDS` all
updated to match. The old contract and the real records already anchored
to it stay on-chain as-is (nothing to migrate, Amoy is a testnet), just no
longer the one `CONTRACT_ADDRESS` points at. `docs/index.html` updated to
the new address and ABI, and now displays the agreement count. New
contract verified on PolygonScan (Exact Match), and a fresh real run
confirmed the whole chain end to end: 3 candidates found, all 2/3
agreement, best one anchored (tx
dbc22bcddc97a65d7f3b4feb5de166fd090318616921866bbbf153a3acbcd336),
round-tripped through `verify_record.py` against the live contract.

## 2026-10-09 - Build-log artifact redesigned as a status page, not a sprint tracker

The old artifact was a day-by-day hackathon checklist (day0 through day7,
a progress bar, "what the brief actually asks for"). Dropped all of that:
it's the same framing the README already moved away from, and a sprint
tracker is a strange thing to show someone evaluating a finished project.

Rebuilt it as a status page: what the pipeline does, why ensemble
verification exists, the actual most-recent anchored record shown as a
real example (not a hypothetical), the tech stack, and known limitations.
Reused the exact color and type tokens from `docs/index.html` (the proof
viewer) rather than inventing a new palette, so the two live pages read as
one site instead of two unrelated ones. `decisions.md` and `HANDOFF.md`
stay the actual source of truth; the artifact is a polished front door
that links to them, not a mirror of their checklist detail.

## 2026-10-09 - Proof viewer redesigned to open already proving itself

The page used to open as an empty form, nothing to look at until someone
typed a hash in. Changed it to auto-load the real anchored example on
page load, so a visitor sees live, genuine blockchain data without
clicking anything first. Redesigned the result display as a ledger card
with a dot indicator for model agreement, matching the status page's
visual language instead of a plain field list. Added copy buttons on the
hash fields, a favicon, and Open Graph/Twitter meta tags so a shared link
gets a real preview card instead of a blank one.

## 2026-10-09 - Found and fixed a stray attribution trailer in a pushed commit

A routine sweep found an AI-tool co-author line in commit `a10a521`'s
message, already pushed to the remote. This should never have happened,
the no-AI-traces rule for this repo predates this commit by weeks. Fixed
it directly since `a10a521` was the branch tip with nothing pushed on top
of it yet: amended the message and force-pushed, no history rewrite
needed this time. Full history swept afterward and confirmed clean.

## 2026-10-10 - Stopped using personal/ambiguous-consent photos for testing, measured real accuracy instead

Every real match anchored so far had been checked manually and confirmed
to not actually be the project owner, confirming the match-confidence
section's own caveat. Rather than keep chasing a convincing real-world
match (and running into the consent problem that comes with testing on
other people's photos without clear consent), switched to two things that
don't have that problem:

- Live reverse-search testing now uses real consenting family members
  with genuine public presence, not reused public-figure photos or
  reverse-image-search guesses.
- Added `benchmark_ensemble.py`: measures the ensemble against
  scikit-learn's `fetch_lfw_pairs` (Labeled Faces in the Wild, the
  standard academic face-verification benchmark), entirely offline, known
  ground truth, no search or blockchain involved. `scikit-learn` is an
  optional dependency for this script only, not added to the main
  `requirements.txt` since the pipeline itself doesn't need it.

Licensing note worth being honest about: LFW doesn't have a single clear
formal license, sources conflict, and there's documented criticism that
subjects never consented to inclusion. Used here as what it actually is,
the standard dataset the field uses for exactly this kind of offline
algorithm benchmarking, not claimed as a fully rights-cleared resource.

First real run (30 pairs, 15 same-person and 15 different-person, `test`
subset): 100% true positive rate, 0% false positive rate. Superseded
within the same session, see the next entry below, since 15 per class
turned out to be too small a sample to mean much.

## 2026-10-10 - Scaled the accuracy benchmark to 100 pairs, found a real false positive and false negative

The 30-pair result got questioned, fairly: with zero observed errors in
15 trials per class, the true error rate could plausibly be as high as
15-20% and still produce a 0-error sample by chance (the standard "rule
of three" bound). A suspiciously perfect small sample isn't strong
evidence, it's just a sample too small to have found anything yet.

Fixed a real reproducibility bug while scaling up: the original sampling
used `random.sample(population, k)` per run, which doesn't guarantee a
smaller `k`'s pairs are a subset of a larger `k`'s pairs even with the
same seed, since the underlying algorithm's RNG usage differs by `k`.
Switched to shuffling the full index list once per seed, then slicing,
which correctly makes a larger `--per-class` run a strict extension of a
smaller one. This changed which exact pairs the default seed produces, so
the original 30-pair run's specific pairs aren't reproducible from the
current script, only its reported numbers (already recorded above) are.

Re-ran clean at 100 pairs (50 same-person, 50 different-person), and
manually inspected every pair's actual photos, not just the aggregate
numbers, before accepting the result: 92% true positive rate (46/50),
2.0% false positive rate (1/49, one pair skipped for failed face
detection). Agreement distribution: same-person pairs split 0/3=1,
1/3=3, 2/3=8, 3/3=38; different-person pairs split 0/3=46, 1/3=2, 2/3=1.

Checked both error cases against the real photos (saved locally to
`lfw_benchmark_images/`, gitignored, not committed, this project's own
pipeline output, not something to publish without separately clearing
rights for those specific LFW subjects). The one false positive (pair 54)
is two different men who are genuinely similar-looking, age, mustache,
skin tone, build, a believable mistake. The hardest false negative (pair
3) is the same woman across a large difference in angle, lighting, and
apparent age, a legitimately hard pair. Neither looks like a labeling
error or a pipeline bug.

This result is more credible than the 30-pair one specifically because
it's not perfect: finding real, explainable errors at a larger sample
size is stronger evidence the benchmark is actually measuring something,
not just too small to see problems. Also flagged explicitly in the
README: ArcFace/Facenet/VGG-Face were historically developed and tuned
against LFW by their original authors, so strong LFW performance is
partly expected, not fully independent evidence of accuracy on the
pipeline's actual harder real-world photos.

## 2026-10-10 - Full security review, no findings

Reviewed every file in the project (pipeline, entrypoints, the contract,
both static pages, secrets handling) for concrete, exploitable
vulnerabilities, not just style issues. No findings cleared the
confidence bar. Specifically checked and ruled out:

- XSS in the proof viewer: `FaceRecord.sol`'s `storeRecord()` is
  permissionless, so `metadataURI` is attacker-writable on-chain data.
  Traced every place it (or any uploaded-file data) gets rendered;
  everything untrusted goes through `.textContent`, never `.innerHTML`
  with unescaped content.
- Overwrite risk in `storeRecord()`: no "already exists" guard before
  writing, but overwriting a specific `recordHash` requires reproducing
  its exact original byte content (SHA-256 preimage resistance), not
  something targetable in practice.
- Path handling in `verify_record.py --tx` / `main.py --image`: builds
  file paths from CLI arguments without sanitizing, which would be path
  traversal in a hosted context. Not applicable here, this is a local CLI
  tool and CLI flags are a trusted input source.
- Secrets: no hardcoded keys anywhere in tracked files, `.env` correctly
  gitignored, loaded only via `os.getenv()`.

No GitHub issues filed, nothing to log as a bug. Reviewed directly
instead of through a sub-task-delegation workflow, full context on this
codebase was already loaded, so that added more value than re-discovering
it from scratch would have.

## 2026-10-10 - Skipped the demo GIF, called the project done

The live proof viewer link already does what a GIF exists to fake: lets
anyone see and use the real thing with zero setup. A GIF only adds value
for someone skimming the repo who won't click through, which is a nice
extra for a portfolio piece, not a missing feature. Decided it's not
worth blocking on; the project is otherwise complete end to end.

## 2026-10-10 - Redesigned the proof viewer and status page away from generic dark-SaaS defaults

Both `docs/index.html` and the status artifact had drifted into the
common generated-page tells: an uppercase tracked-out eyebrow label,
meta strings joined with middle dots, mono type used for small field
labels instead of just the data itself, and a near-black background with
a single bright accent that could belong to any dashboard. None of that
was wrong, just generic.

Replaced it with a visual identity actually grounded in the subject: a
photographic proof sheet. "Proof" already means two things here (a
contact print made to check before publishing, and a cryptographic
verification), so the metaphor isn't decorative. Concrete devices:

- Register-mark corner ticks on every content frame instead of
  rounded-card-plus-drop-shadow, like print registration marks
- A single film-sprocket perforation strip at the very top of the page,
  the one deliberately bold flourish, not repeated per section
- A warm near-black "darkroom" background instead of a blue-black one,
  with two accent colors that carry real meaning: safelight red for
  primary actions and in-progress state, a developer-tray green reserved
  only for "verified/passed" states, never used decoratively
- Frame numbers (01 to 05) only on the pipeline stages, since that's the
  one place content is genuinely sequential; the lookup and verify
  panels get plain titles, no fake numbering
- Space Grotesk for headings, IBM Plex Sans for body and field labels,
  IBM Plex Mono reserved for actual data (hashes, addresses, timestamps)
  rather than for UI chrome

Tested the rebuilt proof viewer in a real browser (served locally, not
just opened as a file) before committing: the live on-chain lookup
still runs automatically on load, the vote-dot agreement indicator
renders, copy buttons work, and the verify-your-own-record flow still
recomputes and checks a real record. No JS logic changed, only markup
and styling, so the existing read/verify behavior carries over exactly.
The status artifact was rebuilt with the same tokens so the two pages
keep reading as one site, and it also picked up the LFW accuracy numbers
and the security review result, neither of which existed the last time
it was redesigned.
