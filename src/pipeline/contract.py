from pathlib import Path

import solcx

CONTRACT_PATH = Path(__file__).resolve().parents[2] / "contracts" / "FaceRecord.sol"
SOLC_VERSION = "0.8.20"

_cached: tuple[list, str] | None = None


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
