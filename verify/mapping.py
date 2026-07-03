"""Map each claim to the repo its evidence should come from.

Resolution order:
1. Alias table (data/repo_aliases.json): {"project name": "repo-name" | null}.
   null means "known to have no repo in the corpus" -> no_evidence.
2. Direct match: a repo's name appears in the claim text (case-insensitive).
3. No match -> no_evidence.

The alias table is data, not code: edit it when the resume names a project
differently than its repo, or to declare a project repo-less.
"""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ALIASES = ROOT / "data" / "repo_aliases.json"


def load_aliases() -> dict:
    if ALIASES.exists():
        return json.loads(ALIASES.read_text())
    return {}


def resolve_repo(claim_text: str, repo_names: list[str],
                 aliases: dict) -> str | None:
    """Return the repo name for a claim, or None if no evidence exists."""
    low = claim_text.lower()
    # Longest alias first so "Cross-Platform Multimodal ..." beats substrings.
    for name in sorted(aliases, key=len, reverse=True):
        if name.lower() in low:
            return aliases[name]  # may be None (declared repo-less)
    for repo in sorted(repo_names, key=len, reverse=True):
        # Word-boundary match so "Algos" doesn't fire on "algorithms".
        if re.search(rf"\b{re.escape(repo.lower())}\b", low):
            return repo
    return None
