# Decisions

## 2026-09-02 — Repo name: face-id-blockchain-verification

Went with a descriptive name over the task-number variant (hh-goa-2026-task3)
or the shorter face-verify-chain. Matches the artifact's project title, reads
fine outside hackathon context too.

## 2026-09-02 - Cleaned up the first commit's trailer

The first commit had an extra co-author trailer in the message from a
copy-paste mistake; amended and force-pushed to strip it before anything
else landed on top of it. Local editor/tool state stays out of `.gitignore`
(itself visible on GitHub) and goes in `.git/info/exclude` instead,
untracked and invisible.

## 2026-09-02 — Pipeline module layout: package, one module per stage

`src/pipeline/{detect,search,verify,anchor,proof}.py`, each with one function
per stage, instead of one flat main.py (the spec's own skeleton) or one
script per day. Keeps each stage independently testable and readable in
isolation; matches the Day1-4 build order already laid out in the artifact.

## 2026-09-02 — Error handling: typed exceptions, not result objects

Stage functions raise from `exceptions.py` (NoFaceDetectedError,
NoCandidatesFoundError, NoVerifiedMatchError, ChainError); main.py and
verify_record.py each catch PipelineError once at the top level. Chosen over
(ok, value, error) result objects to avoid boilerplate at every call site for
a 5-day build.

## 2026-09-02 — Retries: network calls only

`with_retry` wraps only the SerpApi/Serper search call and the web3 RPC
calls. DeepFace calls are local/CPU-bound and don't transiently fail the way
a network call does, so they're left unwrapped.

## 2026-09-02 — Two entrypoints, not one CLI with subcommands

`main.py --image <path>` runs the full pipeline; `verify_record.py --tx
<hash>` runs the read-back proof independently, loading the matching record
from `output/*.json` to recompute the hash locally. Matches the spec's own
naming and keeps the proof step usable without re-running the whole
pipeline. CLI parsing is argparse (stdlib), no third-party dependency for a
two-flag surface.

## 2026-09-02 — Docs/artifact sync adopted, mirrored into the published artifact

Decision log (this file) and `docs/HANDOFF.md` are the real source of truth,
maintained every session. In addition, the published build-log artifact's
checkboxes get mirrored via browser automation at the end of each session,
so the artifact's own view stays visually accurate too (its checked state
persists per-browser, this repo's docs are what's actually authoritative).
