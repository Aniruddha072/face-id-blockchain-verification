from pathlib import Path

import solcx
from web3 import Web3
from web3.middleware import ExtraDataToPOAMiddleware

CONTRACT_PATH = Path(__file__).resolve().parents[2] / "contracts" / "FaceRecord.sol"
SOLC_VERSION = "0.8.20"

_cached: tuple[list, str] | None = None


def get_web3(rpc_url: str) -> Web3:
    """Web3 instance for Polygon Amoy, with POA block header support.

    Amoy's block headers carry more than the 32 bytes of extraData web3.py's
    default validation middleware expects, so every caller needs this
    middleware injected or reads/writes fail with ExtraDataLengthError.
    """
    w3 = Web3(Web3.HTTPProvider(rpc_url))
    w3.middleware_onion.inject(ExtraDataToPOAMiddleware, layer=0)
    return w3


def _ensure_solc() -> None:
    installed = solcx.get_installed_solc_versions()
    if not any(str(v) == SOLC_VERSION for v in installed):
        solcx.install_solc(SOLC_VERSION)


def compile_contract() -> tuple[list, str]:
    """Compile contracts/FaceRecord.sol, return (abi, bytecode).

    Cached after the first call so deploy.py, anchor.py, and proof.py all
    compile once per process, not once per call.
    """
    global _cached
    if _cached is not None:
        return _cached

    _ensure_solc()
    source = CONTRACT_PATH.read_text()
    compiled = solcx.compile_source(
        source,
        output_values=["abi", "bin"],
        solc_version=SOLC_VERSION,
    )
    _, contract_interface = next(iter(compiled.items()))
    _cached = (contract_interface["abi"], contract_interface["bin"])
    return _cached
