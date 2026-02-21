# --------------------
# File: hawki/core/telemetry/exporter.py
# --------------------
"""
Exports aggregated metrics to a public endpoint (opt‑in only).
"""

import json
import logging
import os
import requests
from typing import Optional
from .store import MetricsStore

logger = logging.getLogger(__name__)

class MetricsExporter:
    """Sends aggregated metrics to a remote endpoint."""

    DEFAULT_ENDPOINT = "https://api.hawki.security/v1/metrics"

    def __init__(self, store: Optional[MetricsStore] = None, endpoint: Optional[str] = None):
        self.store = store or MetricsStore()
        self.endpoint = endpoint or os.environ.get("HAWKI_TELEMETRY_ENDPOINT", self.DEFAULT_ENDPOINT)

    def export(self) -> bool:
        """
        Read local metrics, aggregate, and send to endpoint.
        Returns True if successful, False otherwise.
        """
        all_metrics = self.store.get_all()
        if not all_metrics:
            logger.debug("No metrics to export")
            return False

        # Aggregate metrics: we can send the whole list or compute totals.
        # For privacy, we send the list of individual records (they are already anonymous).
        # But to reduce size, we could aggregate; however, we'll keep it simple.
        try:
            response = requests.post(
                self.endpoint,
                json=all_metrics,
                headers={"Content-Type": "application/json"},
                timeout=10,
            )
            response.raise_for_status()
            logger.info(f"Exported {len(all_metrics)} metrics records to {self.endpoint}")
            return True
        except requests.RequestException as e:
            logger.warning(f"Failed to export metrics: {e}")
            return False