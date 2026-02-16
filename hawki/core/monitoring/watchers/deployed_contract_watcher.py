# --------------------
# File: hawki/core/monitoring/watchers/deployed_contract_watcher.py
# --------------------
"""
Watcher that monitors a deployed contract for code changes (via bytecode).
"""

import logging
from typing import Dict, Any, Optional
from web3 import Web3
from web3.middleware import geth_poa_middleware

from ..watcher_base import Watcher

logger = logging.getLogger(__name__)

class DeployedContractWatcher(Watcher):
    """Monitors a contract on a blockchain for changes in bytecode."""

    def __init__(self, name: str, config: Dict[str, Any]):
        super().__init__(name, config)
        self.rpc_url = config.get("rpc_url", "http://localhost:8545")
        self.contract_address = config.get("contract_address")
        if not self.contract_address:
            raise ValueError("contract_address required for DeployedContractWatcher")
        self.w3 = Web3(Web3.HTTPProvider(self.rpc_url))
        self.w3.middleware_onion.inject(geth_poa_middleware, layer=0)
        if not self.w3.is_connected():
            raise ConnectionError(f"Could not connect to {self.rpc_url}")

    def check(self) -> Optional[Dict[str, Any]]:
        """Check if contract bytecode has changed."""
        try:
            code = self.w3.eth.get_code(Web3.to_checksum_address(self.contract_address))
            code_hex = code.hex()
            previous = self.state.get("code_hash")  # actually store hex for simplicity

            if previous is None:
                self.state["code_hash"] = code_hex
                return None

            if code_hex != previous:
                event = {
                    "type": "contract_code_change",
                    "contract_address": self.contract_address,
                    "rpc_url": self.rpc_url,
                    "previous_code_hash": previous[:10] + "...",
                    "new_code_hash": code_hex[:10] + "...",
                    "message": f"Contract {self.contract_address} bytecode changed",
                }
                self.state["code_hash"] = code_hex
                return event
            return None
        except Exception as e:
            logger.error(f"DeployedContractWatcher error: {e}")
            return None

# EOF: hawki/core/monitoring/watchers/deployed_contract_watcher.py