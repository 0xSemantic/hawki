# --------------------
# File: hawki/core/monitoring/watchers/repo_commit_watcher.py
# --------------------
"""
Watcher that polls a Git repository for new commits.
"""

import logging
from pathlib import Path
from typing import Dict, Any, Optional
import git

from ..watcher_base import Watcher

logger = logging.getLogger(__name__)

class RepoCommitWatcher(Watcher):
    """Monitors a local Git repository for new commits."""

    def __init__(self, name: str, config: Dict[str, Any]):
        super().__init__(name, config)
        self.repo_path = Path(config.get("repo_path", ".")).resolve()
        if not self.repo_path.exists():
            raise ValueError(f"Repository path does not exist: {self.repo_path}")
        self.branch = config.get("branch", "main")
        self._last_commit = None

    def check(self) -> Optional[Dict[str, Any]]:
        """Check for new commits since last check."""
        try:
            repo = git.Repo(self.repo_path)
            # Ensure we have the latest remote info
            origin = repo.remotes.origin if repo.remotes else None
            if origin:
                origin.fetch()

            # Get latest commit hash on the branch
            latest_commit = repo.commit(self.branch).hexsha
            previous = self.state.get("last_commit")

            if previous is None:
                # First run, store current hash but don't alert
                self.state["last_commit"] = latest_commit
                return None

            if latest_commit != previous:
                # New commit detected
                commit = repo.commit(latest_commit)
                event = {
                    "type": "new_commit",
                    "repo": str(self.repo_path),
                    "branch": self.branch,
                    "commit_hash": latest_commit,
                    "message": commit.message.strip(),
                    "author": str(commit.author),
                    "timestamp": commit.committed_datetime.isoformat(),
                    "message": f"New commit in {self.repo_path.name}: {commit.message[:50]}",
                }
                self.state["last_commit"] = latest_commit
                return event
            return None
        except Exception as e:
            logger.error(f"RepoCommitWatcher error: {e}")
            return None

# EOF: hawki/core/monitoring/watchers/repo_commit_watcher.py