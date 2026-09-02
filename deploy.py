"""Deploy contracts/FaceRecord.sol to Polygon Amoy using the burner wallet in .env."""

import argparse
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))

from web3 import Web3  # noqa: E402

from pipeline import config  # noqa: E402
from pipeline.contract import compile_contract  # noqa: E402


def deploy() -> str:
    config.require("ALCHEMY_AMOY_RPC_URL", "WALLET_PRIVATE_KEY")

    abi, bytecode = compile_contract()

    w3 = Web3(Web3.HTTPProvider(config.ALCHEMY_AMOY_RPC_URL))
    account = w3.eth.account.from_key(config.WALLET_PRIVATE_KEY)

    face_record = w3.eth.contract(abi=abi, bytecode=bytecode)
    tx = face_record.constructor().build_transaction(
        {
            "from": account.address,
            "nonce": w3.eth.get_transaction_count(account.address),
        }
    )
    signed = account.sign_transaction(tx)
    tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    return receipt.contractAddress


def main() -> None:
    argparse.ArgumentParser(description=__doc__).parse_args()

    address = deploy()
    print(f"Deployed FaceRecord to {address}")
    print(f"Add this to .env: CONTRACT_ADDRESS={address}")
    print(f"View on PolygonScan: https://amoy.polygonscan.com/address/{address}")


if __name__ == "__main__":
    main()
