from web3 import Web3

from . import config
from .contract import compile_contract
from .exceptions import ChainError
from .retry import with_retry


def read_record(record_hash: bytes) -> dict:
    """Read a stored record back from the chain by its hash."""
    config.require("ALCHEMY_AMOY_RPC_URL", "CONTRACT_ADDRESS")

    abi, _ = compile_contract()
    w3 = Web3(Web3.HTTPProvider(config.ALCHEMY_AMOY_RPC_URL))
    contract = w3.eth.contract(
        address=Web3.to_checksum_address(config.CONTRACT_ADDRESS), abi=abi
    )

    def _call():
        return contract.functions.getRecord(record_hash).call()

    try:
        result = with_retry(_call)
    except Exception as exc:
        raise ChainError(f"failed to read record from chain: {exc}") from exc

    return {
        "recordHash": result[0].hex(),
        "metadataURI": result[1],
        "submitter": result[2],
        "timestamp": result[3],
    }
