import hashlib
import json
import time

from web3 import Web3

from . import config
from .contract import compile_contract
from .exceptions import ChainError
from .retry import with_retry
from .verify import Match

SEARCH_ENGINE = "google_lens/serpapi"


def build_record(image_path: str, match: Match) -> dict:
    return {
        "source_image_sha256": _sha256_file(image_path),
        "match_url": match.candidate.url,
        "platform": match.candidate.platform,
        "similarity_score": match.similarity_score,
        "model": match.model,
        "search_engine": SEARCH_ENGINE,
        "timestamp_utc": int(time.time()),
    }


def record_hash(record: dict) -> bytes:
    return hashlib.sha256(json.dumps(record, sort_keys=True).encode()).digest()


def anchor_record(record: dict, metadata_uri: str = "") -> str:
    """Write record's hash on-chain via storeRecord(), return the tx hash."""
    config.require("ALCHEMY_AMOY_RPC_URL", "WALLET_PRIVATE_KEY", "CONTRACT_ADDRESS")

    abi, _ = compile_contract()
    w3 = Web3(Web3.HTTPProvider(config.ALCHEMY_AMOY_RPC_URL))
    account = w3.eth.account.from_key(config.WALLET_PRIVATE_KEY)
    contract = w3.eth.contract(
        address=Web3.to_checksum_address(config.CONTRACT_ADDRESS), abi=abi
    )
    h = record_hash(record)

    def _call():
        tx = contract.functions.storeRecord(h, metadata_uri).build_transaction(
            {
                "from": account.address,
                "nonce": w3.eth.get_transaction_count(account.address),
            }
        )
        signed = account.sign_transaction(tx)
        sent = w3.eth.send_raw_transaction(signed.raw_transaction)
        return w3.eth.wait_for_transaction_receipt(sent)

    try:
        receipt = with_retry(_call)
    except Exception as exc:
        raise ChainError(f"failed to anchor record on-chain: {exc}") from exc

    return receipt.transactionHash.hex()


def _sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()
