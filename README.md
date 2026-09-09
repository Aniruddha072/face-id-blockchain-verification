# Face ID + Blockchain Verification

> HH Goa 2026, Partner Trials, Task #3

A pipeline that detects a face, finds a genuine social media match through
reverse-image search, and anchors that match on-chain as a tamper-evident,
verifiable record.

## Overview

The pipeline runs in five stages. It detects and encodes a face from an
input photo, finds where that face appears on the public web via
reverse-image search, verifies each candidate against the source photo and
ranks up to three genuine matches by confidence instead of forcing a single
guess, hashes the best match's record and writes it to a smart contract on
a public testnet, and finally reads the chain back to prove the record
hasn't been altered.

## Architecture

```
photo -> detect & encode -> reverse-image search -> verify match -> hash + anchor on-chain -> read-back proof
         (DeepFace/ArcFace)   (SerpApi Google Lens)    (DeepFace.verify)   (web3.py, Polygon Amoy)   (verify_record.py)
```

## Requirements mapping

| Brief requirement | How it's met |
|---|---|
| Detect and encode a face from an input image | DeepFace (RetinaFace detector + ArcFace embedding) |
| Find at least one real, matching social media post via genuine reverse-image search | SerpApi Google Lens engine, filtered to social domains, no hardcoded results |
| Upload the match's data to a blockchain for a tamper-evident, verifiable record | SHA-256 hash of the match record written to a Solidity contract on Polygon Amoy testnet, independently checkable on PolygonScan |

## Tech stack

| Layer | Pick | Why |
|---|---|---|
| Face detect + encode | DeepFace (Python), RetinaFace + ArcFace | One-line API, swappable backends, free, self-hosted |
| Reverse image search | SerpApi, Google Lens engine | Genuine Google reverse-image results, 250 free searches/month, no card |
| Match verification | `DeepFace.verify()` on every candidate, top 3 kept and ranked by distance | Surfaces ambiguity instead of one forced guess, runs locally for free |
| Blockchain | Polygon Amoy testnet via Alchemy RPC + web3.py | Free, no card, ~2s finality, PolygonScan lets anyone verify independently |
| Smart contract | Minimal Solidity: `storeRecord()` + event + `getRecord()` | Gives reviewers an on-chain function to point at, not a raw calldata blob |
| Contract deployment | `deploy.py`, compiles via py-solc-x and deploys with web3.py | One command instead of a manual Remix step, same wallet key `main.py` already needs |
| Off-chain storage (optional) | Pinata (IPFS) | Keeps the full record content-addressed; skippable |
| Wallet | Burner MetaMask wallet, testnet POL only | Zero real funds ever touch this project |

## Project layout

```
main.py               run the full pipeline against one image
verify_record.py      given a tx hash, confirm the on-chain record still matches
deploy.py             compile and deploy contracts/FaceRecord.sol
contracts/
  FaceRecord.sol       the on-chain record store
src/pipeline/
  detect.py            face detection + embedding
  search.py             reverse image search (SerpApi)
  verify.py              candidate face verification
  anchor.py               record building + on-chain write
  proof.py                  on-chain read-back
  contract.py                shared Solidity compile step
  config.py                  .env loading
  retry.py                    retry-with-backoff for network calls
  exceptions.py                 typed errors for all of the above
output/                saved record JSON per run (gitignored)
```

## Setup

```bash
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux
pip install -r requirements.txt
cp .env.example .env         # then fill in SERPAPI_KEY, ALCHEMY_AMOY_RPC_URL, WALLET_PRIVATE_KEY
python deploy.py             # deploys FaceRecord.sol, prints the address to add as CONTRACT_ADDRESS
```

## Configuration

See `.env.example`. All values required unless noted optional:

- `SERPAPI_KEY`: SerpApi key (Google Lens engine)
- `SERPER_API_KEY`: optional backup (Serper.dev, 2,500 free one-time queries)
- `ALCHEMY_AMOY_RPC_URL`: Alchemy RPC URL for the Polygon Amoy testnet app
- `WALLET_PRIVATE_KEY`: burner wallet private key, funded only via testnet faucet
- `CONTRACT_ADDRESS`: deployed `FaceRecord` contract address, from `deploy.py`
- `PINATA_JWT`: optional, only if pinning records to IPFS

## How to run

```bash
python main.py --image photo.jpg
```

Runs the full pipeline and saves the result to `output/<tx_hash>.json`. To
independently confirm a past run still matches what's on-chain:

```bash
python verify_record.py --tx <tx_hash>
```

## Match confidence

Reverse-image search can find visually similar strangers, not just the
actual subject, especially when a face isn't heavily reposted or tagged
online. Rather than commit to a single automated guess that might be
confidently wrong, `verify_candidates()` returns up to the 3
highest-confidence verified matches (ranked by embedding distance), and
`main.py` prints all of them. Only the single best match gets hashed and
anchored on-chain, keeping that part of the pipeline unambiguous, but
seeing the runner-up candidates (and how close or far their distances are)
makes it obvious when a match is weak versus genuinely convincing.

## Example output

Real run against a real photo, `python main.py --image photo.jpg`:

```
detected face: confidence=1.000 bbox={'x': 728, 'y': 292, 'w': 398, 'h': 476}
reverse search: 22 social-media candidate(s)
verified 3 candidate(s) as genuine matches:
  [1] https://www.youtube.com/watch?v=_9Jsb54tL9k (platform=youtube.com, distance=0.5720) (anchoring this one)
  [2] https://www.youtube.com/watch?v=gXXKBT4KmWs (platform=youtube.com, distance=0.6224)
  [3] https://www.youtube.com/watch?v=TBr1lSxlNsY (platform=youtube.com, distance=0.6426)
anchored on-chain: tx c1bbec42a8fd7116631c4775dfbbaca03cb58e3a02681ba1807fe8548d6cbccb
view proof: https://amoy.polygonscan.com/tx/c1bbec42a8fd7116631c4775dfbbaca03cb58e3a02681ba1807fe8548d6cbccb
saved record to output/c1bbec42a8fd7116631c4775dfbbaca03cb58e3a02681ba1807fe8548d6cbccb.json
```

[View this transaction on PolygonScan](https://amoy.polygonscan.com/tx/c1bbec42a8fd7116631c4775dfbbaca03cb58e3a02681ba1807fe8548d6cbccb)

## Blockchain choice

Polygon Amoy testnet, accessed via an Alchemy RPC endpoint. Chosen because it
has a genuine no-card free tier, roughly 2 second block finality, full
Solidity support, and PolygonScan gives anyone an independent way to verify
the on-chain record without trusting this repo's output.

The deployed contract's source is verified on PolygonScan (exact match):
[0x80637a622EF860a85c3510b77eb832F356ed08DD](https://amoy.polygonscan.com/address/0x80637a622EF860a85c3510b77eb832F356ed08DD#code).
Anyone can read the actual Solidity source there and call `getRecord()`
directly from the "Read Contract" tab, no wallet required.

## Known limitations

- Search coverage is limited to what the search engine has indexed, it
  won't find everything, especially recent or private posts.
- Match accuracy depends on the embedding model and the input photo's
  quality (angle, lighting, occlusion).
- The blockchain proves the record's hash existed at a specific block and
  time. It's a tamper-evident timestamp of the claim, not proof the matched
  content itself is authentic.
- No liveness or deepfake detection on the input photo.
- Run only with consenting subjects. Face search tools' terms of service
  restrict use for employment, credit, insurance, or tenant-screening
  decisions.
- This project runs on a public **testnet** (Polygon Amoy), not mainnet, so
  no real funds or mainnet gas are involved.
- Subject to the search API's rate limits and free-tier cap (SerpApi: 250
  searches/month; Serper.dev fallback: 2,500 one-time queries).
- SerpApi's image upload caps the source photo at 500 KB; larger files are
  rejected outright rather than silently resized.

## Consent / ethics note

This pipeline is run only against consenting subjects with a real, findable
public social presence. It is not intended, and should not be used, for
employment, credit, insurance, tenant-screening, or any other decision about
a person without their knowledge and consent.

## Demo recording

*(TODO: link to an unedited screen recording of the full pipeline running
end to end)*

## License

[MIT](LICENSE)
