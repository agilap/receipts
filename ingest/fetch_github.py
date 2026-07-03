"""Fetch raw GitHub evidence for a user and write it to data/raw/.

Usage: python ingest/fetch_github.py <username> [repo ...]

Unauthenticated by default (60 req/hr); set GITHUB_TOKEN to raise the limit.
Every response is cached on disk, so re-runs only fetch what's missing.
"""

import base64
import json
import os
import sys
import time
from pathlib import Path

import requests

API = "https://api.github.com"
RAW_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"

# Dependency manifests worth grabbing from the repo root.
DEP_FILES = [
    "package.json",
    "package-lock.json",
    "requirements.txt",
    "pyproject.toml",
    "poetry.lock",
    "Pipfile",
    "go.mod",
    "Cargo.toml",
    "composer.json",
    "Gemfile",
]

def load_env():
    """Read repo-root .env into os.environ (existing vars win)."""
    env = Path(__file__).resolve().parent.parent / ".env"
    if env.exists():
        for line in env.read_text().splitlines():
            if "=" in line and not line.startswith("#"):
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())


load_env()
session = requests.Session()
session.headers["Accept"] = "application/vnd.github+json"
if os.environ.get("GITHUB_TOKEN"):
    session.headers["Authorization"] = f"Bearer {os.environ['GITHUB_TOKEN']}"


def get(url, ok_404=False):
    """GET with rate-limit awareness. Returns parsed JSON or None on 404."""
    resp = session.get(url, timeout=30)
    remaining = resp.headers.get("X-RateLimit-Remaining")
    if resp.status_code == 404 and ok_404:
        return None
    if resp.status_code == 403 and remaining == "0":
        reset = int(resp.headers.get("X-RateLimit-Reset", 0))
        sys.exit(f"Rate limit exhausted; resets at {time.ctime(reset)}. "
                 "Re-run later — cached files will be skipped.")
    resp.raise_for_status()
    print(f"  GET {url}  (remaining: {remaining})")
    return resp.json()


def fetch_cached(path: Path, url: str, ok_404=False):
    """Fetch url unless path already exists; persist and return the JSON."""
    if path.exists():
        return json.loads(path.read_text())
    data = get(url, ok_404=ok_404)
    if data is None:
        return None
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2))
    return data


def fetch_repo(repo: dict):
    full = repo["full_name"]
    d = RAW_DIR / repo["name"]
    d.mkdir(parents=True, exist_ok=True)
    (d / "repo.json").write_text(json.dumps(repo, indent=2))

    fetch_cached(d / "languages.json", f"{API}/repos/{full}/languages")
    fetch_cached(d / "readme.json", f"{API}/repos/{full}/readme", ok_404=True)

    for dep in DEP_FILES:
        out = d / f"dep__{dep.replace('/', '_')}.json"
        fetch_cached(out, f"{API}/repos/{full}/contents/{dep}", ok_404=True)

    # Contributor stats: GitHub may return 202 while it computes them.
    stats_path = d / "contributors_stats.json"
    if not stats_path.exists():
        url = f"{API}/repos/{full}/stats/contributors"
        for _ in range(3):
            resp = session.get(url, timeout=30)
            if resp.status_code == 202:
                time.sleep(3)
                continue
            if resp.ok and resp.text.strip():
                stats_path.write_text(json.dumps(resp.json(), indent=2))
                print(f"  GET {url}")
            break


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    user = sys.argv[1]
    only = set(sys.argv[2:])

    # With a token, /user/repos also lists private repos; the public
    # /users/{user}/repos endpoint never does.
    if os.environ.get("GITHUB_TOKEN"):
        repos_url = f"{API}/user/repos?per_page=100&sort=updated&affiliation=owner"
    else:
        repos_url = f"{API}/users/{user}/repos?per_page=100&sort=updated"
    repos = fetch_cached(RAW_DIR / "_repos.json", repos_url)

    # Args containing "/" are extra owner/name repos outside the user's list
    # (e.g. a thesis repo you collaborate on).
    for full in [a for a in only if "/" in a]:
        repos.append(get(f"{API}/repos/{full}"))
    only = {a for a in only if "/" not in a}

    for repo in repos:
        if only and repo["name"] not in only and repo["full_name"] not in only:
            continue
        if repo.get("fork"):
            continue
        print(f"repo: {repo['name']}")
        fetch_repo(repo)

    print("done.")


if __name__ == "__main__":
    main()
