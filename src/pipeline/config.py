import os

from dotenv import load_dotenv

load_dotenv()

SERPAPI_KEY = os.getenv("SERPAPI_KEY")
SERPER_API_KEY = os.getenv("SERPER_API_KEY")
ALCHEMY_AMOY_RPC_URL = os.getenv("ALCHEMY_AMOY_RPC_URL")
WALLET_PRIVATE_KEY = os.getenv("WALLET_PRIVATE_KEY")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")
PINATA_JWT = os.getenv("PINATA_JWT")


def require(*names: str) -> None:
    """Raise a clear error if any of the named settings are missing from .env."""
    missing = [name for name in names if not globals().get(name)]
    if missing:
        raise RuntimeError(
            f"missing required setting(s): {', '.join(missing)}. "
            "copy .env.example to .env and fill them in."
        )
