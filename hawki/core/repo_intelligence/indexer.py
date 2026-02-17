# --------------------
# File: hawki/core/repo_intelligence/indexer.py
# --------------------
"""
Repository indexer: handles local directories and remote Git repos.
Scans all .sol files, parses them, and builds a unified index.
"""

import logging
import tempfile
from pathlib import Path
from typing import List, Dict, Any, Optional
import git
from urllib.parse import urlparse

from .parser import SolidityParser

logger = logging.getLogger(__name__)

class RepositoryIndexer:
    """Clones/finds repos and indexes Solidity files."""

    def __init__(self, parser: Optional[SolidityParser] = None):
        self.parser = parser or SolidityParser()
        self._temp_dir: Optional[Path] = None

    def index(self, path_or_url: str) -> Dict[str, Any]:
        """
        Main entry point: if path_or_url is a local directory, index it.
        If it's a Git URL, clone it first.
        Returns a dictionary with repository metadata and contract data.
        """
        parsed = urlparse(path_or_url)
        is_remote = parsed.scheme in ("http", "https", "git", "ssh")

        if is_remote:
            return self._index_remote(path_or_url)
        else:
            return self._index_local(Path(path_or_url))

    def _index_local(self, path: Path) -> Dict[str, Any]:
        """Index a local directory."""
        if not path.is_dir():
            raise ValueError(f"Not a directory: {path}")
        contracts = self._scan_directory(path)
        return {
            "type": "local",
            "path": str(path),
            "contracts": contracts,
        }

    def _index_remote(self, url: str) -> Dict[str, Any]:
        """Clone a remote repository and index it."""
        self._temp_dir = Path(tempfile.mkdtemp(prefix="hawki_"))
        logger.info(f"Cloning {url} into {self._temp_dir}")
        try:
            git.Repo.clone_from(url, self._temp_dir)
        except Exception as e:
            raise RuntimeError(f"Failed to clone repository: {e}")

        contracts = self._scan_directory(self._temp_dir)
        return {
            "type": "remote",
            "url": url,
            "path": str(self._temp_dir),
            "contracts": contracts,
        }

    def _scan_directory(self, directory: Path) -> List[Dict[str, Any]]:
        """Recursively find all .sol files and parse them."""
        contracts = []
        for sol_file in directory.rglob("*.sol"):
            logger.debug(f"Parsing {sol_file}")
            parsed = self.parser.parse_file(sol_file)
            if parsed:
                contracts.append(parsed)
        return contracts

    def cleanup(self):
        """Remove temporary clone directory if any."""
        if self._temp_dir and self._temp_dir.exists():
            import shutil
            shutil.rmtree(self._temp_dir, ignore_errors=True)
            self._temp_dir = None

# EOF: hawki/core/repo_intelligence/indexer.py