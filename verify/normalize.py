"""Normalize data/raw/ GitHub JSON into evidence chunks.

Usage: python -m verify.normalize
Writes data/evidence/chunks.json: [{id, repo, type, text, url, date}]
"""

import base64
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
OUT = ROOT / "data" / "evidence" / "chunks.json"


def decode_content(obj: dict) -> str:
    return base64.b64decode(obj["content"]).decode("utf-8", errors="replace")


def chunk(repo, type_, text, url, date):
    return {"repo": repo, "type": type_, "text": text.strip(),
            "url": url, "date": date}


def repo_chunks(d: Path) -> list[dict]:
    chunks = []
    meta = json.loads((d / "repo.json").read_text())
    name, url = meta["name"], meta["html_url"]
    date = meta.get("pushed_at")

    desc = meta.get("description") or "no description"
    topics = ", ".join(meta.get("topics", [])) or "none"
    chunks.append(chunk(name, "metadata",
        f"GitHub repository {name}: {desc}. Primary language: "
        f"{meta.get('language')}. Topics: {topics}. Created "
        f"{meta.get('created_at', '?')[:10]}, last pushed {str(date)[:10]}.",
        url, date))

    lang_file = d / "languages.json"
    if lang_file.exists():
        langs = json.loads(lang_file.read_text())
        total = sum(langs.values()) or 1
        parts = ", ".join(f"{k} ({v * 100 // total}%)" for k, v in
                          sorted(langs.items(), key=lambda x: -x[1]))
        if parts:
            chunks.append(chunk(name, "languages",
                f"Languages in repository {name} by bytes of code: {parts}.",
                url, date))

    readme_file = d / "readme.json"
    if readme_file.exists():
        readme = json.loads(readme_file.read_text())
        text = decode_content(readme)
        # Split on markdown headings; keep each section as one chunk.
        sections = re.split(r"\n(?=#{1,3} )", text)
        for sec in sections:
            sec = sec.strip()
            if len(sec) < 40:  # skip bare headings / badges
                continue
            chunks.append(chunk(name, "readme",
                f"From the README of repository {name}:\n{sec[:2000]}",
                readme.get("html_url", url), date))

    for dep_file in d.glob("dep__*.json"):
        obj = json.loads(dep_file.read_text())
        fname = obj.get("name", dep_file.stem.replace("dep__", ""))
        text = decode_content(obj)
        deps = extract_deps(fname, text)
        if deps:
            # One declarative sentence per package: NLI models won't bridge
            # a bare manifest list to a "project uses X" claim, but they
            # will entail it from an explicit usage statement.
            uses = " ".join(f"{name} uses the {d} package." for d in deps)
            c = chunk(name, "dependencies",
                f"The dependency file {fname} in repository {name} shows "
                f"which libraries the project uses. {uses}",
                obj.get("html_url", url), date)
            c["packages"] = deps  # structured list for deterministic matching
            chunks.append(c)

    stats_file = d / "contributors_stats.json"
    if stats_file.exists():
        stats = json.loads(stats_file.read_text())
        if isinstance(stats, list):
            for s in stats:
                author = s.get("author") or {}
                chunks.append(chunk(name, "commits",
                    f"Contributor {author.get('login')} has {s.get('total')} "
                    f"commits in repository {name}.",
                    url, date))
    return chunks


def extract_deps(fname: str, text: str) -> list[str]:
    """Best-effort flat list of declared dependency names (not lockfiles)."""
    if fname == "package.json":
        pkg = json.loads(text)
        return sorted(set(pkg.get("dependencies", {})) |
                      set(pkg.get("devDependencies", {})))
    if fname == "requirements.txt":
        names = []
        for line in text.splitlines():
            line = line.split("#")[0].strip()
            # Tolerate markdown-style "- pkg" bullets; skip pip flags (-r, --x).
            line = re.sub(r"^- +", "", line)
            if line and not line.startswith("-"):
                names.append(re.split(r"[<>=!~\[ ]", line)[0])
        return sorted(set(filter(None, names)))
    if fname == "pyproject.toml":
        # Cheap parse: quoted entries inside dependencies = [...] arrays only.
        deps = []
        for block in re.findall(
                r'dependencies\s*=\s*\[(.*?)\]', text, re.S):
            deps += re.findall(r'"([A-Za-z0-9_.-]+)', block)
        return sorted(set(deps))
    return []


def main():
    chunks = []
    for d in sorted(RAW.iterdir()):
        if d.is_dir() and (d / "repo.json").exists():
            chunks.extend(repo_chunks(d))
    for i, c in enumerate(chunks):
        c["id"] = i
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(chunks, indent=2))
    by_type = {}
    for c in chunks:
        by_type[c["type"]] = by_type.get(c["type"], 0) + 1
    print(f"{len(chunks)} chunks -> {OUT.relative_to(ROOT)}  {by_type}")


if __name__ == "__main__":
    main()
